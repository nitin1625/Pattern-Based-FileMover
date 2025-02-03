import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import shutil
import fnmatch
from datetime import datetime

class FileMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Mover Pro")
        self.root.geometry("750x700")
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#ccc")
        self.style.configure("Title.TLabel", font=('Helvetica', 12, 'bold'))
        
        # Variables
        self.source_path = tk.StringVar()
        self.dest_path = tk.StringVar()
        self.exclude_patterns = tk.StringVar()
        self.preserve_structure = tk.BooleanVar(value=True)
        self.transfer_method = tk.StringVar(value="copy")
        self.rename_duplicates = tk.BooleanVar(value=False)
        self.config_history = []
        
        self.create_ui()


    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Source Section
        source_frame = ttk.LabelFrame(main_frame, text=" Source Directory ", padding=10)
        source_frame.grid(row=0, column=0, sticky="ew", pady=5)
        
        ttk.Entry(source_frame, textvariable=self.source_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(source_frame, text="Browse", command=self.browse_source).pack(side=tk.LEFT)
        
        # Destination Section
        dest_frame = ttk.LabelFrame(main_frame, text=" Destination Directory ", padding=10)
        dest_frame.grid(row=1, column=0, sticky="ew", pady=5)
        
        ttk.Entry(dest_frame, textvariable=self.dest_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(dest_frame, text="Browse", command=self.browse_dest).pack(side=tk.LEFT)

        # Exclusion Patterns
        exclude_frame = ttk.LabelFrame(main_frame, text=" Exclusion Patterns (comma-separated) ", padding=10)
        exclude_frame.grid(row=4, column=0, sticky="ew", pady=5)
        
        ttk.Entry(exclude_frame, textvariable=self.exclude_patterns, width=60).pack(side=tk.LEFT, padx=5)
        ttk.Button(exclude_frame, text="?", width=3, command=self.show_pattern_help).pack(side=tk.LEFT)

        
        # Configuration Management
        config_frame = ttk.LabelFrame(main_frame, text=" Configuration Management ", padding=10)
        config_frame.grid(row=2, column=0, sticky="ew", pady=5)
        
        ttk.Button(config_frame, text="💾 Save Config", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_frame, text="📂 Load Config", command=self.browse_configs).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_frame, text="🔄 Reset", command=self.reset_config).pack(side=tk.LEFT, padx=5)
        
        # Transfer Options
        options_frame = ttk.LabelFrame(main_frame, text=" Transfer Options ", padding=10)
        options_frame.grid(row=3, column=0, sticky="ew", pady=5)
        
        ttk.Radiobutton(options_frame, text="Copy Files", variable=self.transfer_method, 
                       value="copy").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(options_frame, text="Move Files", variable=self.transfer_method, 
                       value="move").pack(side=tk.LEFT, padx=10)
        
        ttk.Checkbutton(options_frame, text="Preserve directory structure", 
                       variable=self.preserve_structure).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(options_frame, text="Rename duplicates", 
                       variable=self.rename_duplicates).pack(side=tk.LEFT, padx=10)
                
        # Progress and Results
        results_frame = ttk.LabelFrame(main_frame, text=" Progress & Results ", padding=10)
        results_frame.grid(row=5, column=0, sticky="nsew", pady=5)
        
        self.progress = ttk.Progressbar(results_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        self.results_text = tk.Text(results_frame, height=12, width=80, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, pady=10)
        
        ttk.Button(button_frame, text="▶️ Start Transfer", 
                  command=self.move_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔍 Preview", 
                  command=self.preview_operation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Clean Empty Folders", 
                  command=self.delete_empty_directories).pack(side=tk.LEFT, padx=5)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)

    def delete_empty_directories(self):
        source = self.source_path.get()
        if not source:
            messagebox.showerror("Error", "Please select source directory")
            return
        
        deleted_count = 0
        for root, dirs, files in os.walk(source, topdown=False):
            for dir_name in dirs:
                try:
                    dir_path = os.path.join(root, dir_name)
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        deleted_count += 1
                except OSError:
                    continue
        
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", f"Deleted {deleted_count} empty directories\n")
        if deleted_count > 0:
            messagebox.showinfo("Success", f"Deleted {deleted_count} empty directories")
 

    def get_destination_path(self, source_root, file_path, dest_root):
        if self.preserve_structure.get():
            rel_path = os.path.relpath(file_path, source_root)
            dest_path = os.path.join(dest_root, rel_path)
        else:
            dest_path = os.path.join(dest_root, os.path.basename(file_path))

        if self.rename_duplicates.get():
            dir_name = os.path.dirname(dest_path)
            file_name = os.path.basename(dest_path)
            base, ext = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(dest_path):
                new_name = f"{base}_{counter}{ext}"
                dest_path = os.path.join(dir_name, new_name)
                counter += 1
        
        return dest_path
 
    def show_pattern_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Search Pattern Help")
        help_window.geometry("500x400")
        help_window.configure(bg='#F4DEB3')
        
        help_text = """
Wildcards & special characters:
* - Zero or more characters
? - Exactly one character
| - Use to combine search patterns

Sample search patterns:
*.* - Gets all files with any extension
*.doc - Gets all files that start with a .doc extension
*.doc|*.xls - Gets all files that start with a .doc or an .xls extension
s?.do - Gets all files which name begin with the letter s and have exactly a .do extension
???.doc - Gets all files which name is at most 3 characters long and have exactly a .doc extension
list?.txt - files that start with 'list', are followed by 1 character and have exactly a .txt extension
        """
        
        text_widget = tk.Text(help_window, wrap='word', bg='#F4DEB3')
        text_widget.pack(padx=10, pady=10, fill='both', expand=True)
        text_widget.insert('1.0', help_text)
        text_widget.configure(state='disabled')

    def browse_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_path.set(path)
    
    def browse_dest(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_path.set(path)

    def browse_configs(self):
        source_dir = self.source_path.get()
        if not source_dir:
            messagebox.showerror("Error", "Please select source directory first")
            return
        
        config_dir = os.path.join(source_dir, "config_file_mover")
        if not os.path.exists(config_dir):
            messagebox.showinfo("Info", "No configurations found")
            return
        
        config_files = sorted(
            [f for f in os.listdir(config_dir) if f.endswith(".json")],
            key=lambda x: os.path.getmtime(os.path.join(config_dir, x)),
            reverse=True
        )
        
        if not config_files:
            messagebox.showinfo("Info", "No configurations found")
            return
        
        config_window = tk.Toplevel(self.root)
        config_window.title("Select Configuration")
        config_window.geometry("800x400")
        
        tree = ttk.Treeview(config_window, columns=("Date", "Source", "Destination", "Exclusions"), show="headings")
        vsb = ttk.Scrollbar(config_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        tree.heading("Date", text="Date Created")
        tree.heading("Source", text="Source Directory")
        tree.heading("Destination", text="Destination Directory")
        tree.heading("Exclusions", text="Exclusion Patterns")
        
        tree.column("Date", width=150)
        tree.column("Source", width=200)
        tree.column("Destination", width=200)
        tree.column("Exclusions", width=250)
        
        for cfg_file in config_files:
            cfg_path = os.path.join(config_dir, cfg_file)
            try:
                with open(cfg_path, "r") as f:
                    config = json.load(f)
                    tree.insert("", "end", values=(
                        datetime.fromtimestamp(os.path.getctime(cfg_path)).strftime('%Y-%m-%d %H:%M'),
                        config.get("source_path", ""),
                        config.get("dest_path", ""),
                        config.get("exclude_patterns", "")
                    ), tags=(cfg_path,))
            except Exception:
                continue
        
        tree.bind("<Double-1>", lambda e: self.load_config(tree.item(tree.focus())['tags'][0]))
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_config(self, config_path):

        try:
            self.source_path.trace_remove('write', self.trace_id)
        except AttributeError:
            pass

        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                self.source_path.set(config.get("source_path", ""))
                self.dest_path.set(config.get("dest_path", ""))
                self.exclude_patterns.set(config.get("exclude_patterns", ""))
                self.preserve_structure.set(config.get("preserve_structure", True))
                self.transfer_method.set(config.get("transfer_method", "copy"))
                self.rename_duplicates.set(config.get("rename_duplicates", False))
                
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, f"Loaded configuration: {os.path.basename(config_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config: {str(e)}")

    def reset_config(self):
        self.source_path.set("")
        self.dest_path.set("")
        self.exclude_patterns.set("")
        self.preserve_structure.set(True)
        self.transfer_method.set("copy")
        self.rename_duplicates.set(False)
        self.results_text.delete(1.0, tk.END)
        self.progress["value"] = 0
    
    def save_settings(self):
        if not self.validate_paths():
            return
        
        settings = {
            "source_path": self.source_path.get(),
            "dest_path": self.dest_path.get(),
            "exclude_patterns": self.exclude_patterns.get(),
            "preserve_structure": self.preserve_structure.get(),
            "transfer_method": self.transfer_method.get(),
            "rename_duplicates": self.rename_duplicates.get(),
            "created_at": datetime.now().isoformat()
        }
        
        config_dir = os.path.join(self.source_path.get(), "config_file_mover")
        os.makedirs(config_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        config_path = os.path.join(config_dir, f"config_{timestamp}.json")
        
        try:
            with open(config_path, "w") as f:
                json.dump(settings, f, indent=2)
            messagebox.showinfo("Success", f"Configuration saved:\n{config_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {str(e)}")
    
    def validate_paths(self):
        if not os.path.exists(self.source_path.get()):
            messagebox.showerror("Error", "Source directory does not exist")
            return False
        if not os.path.exists(self.dest_path.get()):
            messagebox.showerror("Error", "Destination directory does not exist")
            return False
        return True

    def should_exclude(self, filepath):
        patterns = [p.strip() for p in self.exclude_patterns.get().split(',') if p.strip()]
        filename = os.path.basename(filepath)
        return any(fnmatch.fnmatch(filename, pattern) for pattern in patterns)
    
    def get_all_files(self, directory):
        file_paths = []
        try:
            for root, dirs, files in os.walk(directory):
                if "config_file_mover" in dirs:
                    dirs.remove("config_file_mover") 

                for file in files:
                        full_path = os.path.join(root, file)
                        file_paths.append(full_path)
            return file_paths
        except Exception as e:
            messagebox.showerror("Error", f"Error walking directory: {e}")
            return []  
           
    def preview_operation(self):
        source = self.source_path.get()
        dest = self.dest_path.get()
        
        if not source or not dest:
            messagebox.showerror("Error", "Please select both source and destination directories")
            return
        
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", f"Preview of files to be {self.transfer_method.get()}ed:\n\n")
        
        try:
            files = self.get_all_files(source)
            for src_path in files:
                if not self.should_exclude(src_path):
                    dest_path = self.get_destination_path(source, src_path, dest)
                    rel_src = os.path.relpath(src_path, source)
                    rel_dest = os.path.relpath(dest_path, dest)
                    self.results_text.insert(tk.END, f"Will {self.transfer_method.get()}: {rel_src} -> {rel_dest}\n")
                else:
                    rel_src = os.path.relpath(src_path, source)
                    self.results_text.insert(tk.END, f"Will skip: {rel_src} (excluded)\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error during preview: {str(e)}")
    
    def move_files(self):
        source = self.source_path.get()
        dest = self.dest_path.get()
        
        if not source or not dest:
            messagebox.showerror("Error", "Please select both source and destination directories")
            return
        
        if source ==dest:
            messagebox.showerror("Error", "Source and destination directories are the same.")
            return
        
        try:
            files = self.get_all_files(source)
            total_files = len(files)
            self.progress["maximum"] = total_files
            self.progress["value"] = 0
            
            moved = 0
            skipped = 0
            
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert("1.0", f"{'Moving' if self.transfer_method.get() == 'move' else 'Copying'} files:\n\n")
            
            for i, src_path in enumerate(files, 1):
                if not self.should_exclude(src_path):
                    dest_path = self.get_destination_path(source, src_path, dest)
                    
                    # Create destination directory if it doesn't exist
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    
                    # Move or copy the file based on transfer method
                    if self.transfer_method.get() == "move":
                        shutil.move(src_path, dest_path)
                    else:
                        shutil.copy2(src_path, dest_path)
                    
                    rel_path = os.path.relpath(src_path, source)
                    self.results_text.insert(tk.END, f"{self.transfer_method.get().capitalize()}ed: {rel_path}\n")
                    moved += 1
                else:
                    rel_path = os.path.relpath(src_path, source)
                    self.results_text.insert(tk.END, f"Skipped: {rel_path}\n")
                    skipped += 1
                
                # Update progress bar
                self.progress["value"] = i
                self.root.update_idletasks()
            
            # Clean up empty directories if moving files
            if self.transfer_method.get() == "move":
                self.delete_empty_directories()
            
            # Save settings after successful operation
            self.save_settings()
            
            summary = f"\nOperation complete!\n{self.transfer_method.get().capitalize()}ed: {moved} files\nSkipped: {skipped} files"
            self.results_text.insert(tk.END, summary)
            messagebox.showinfo("Success", summary)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error during operation: {str(e)}")

    


def main():
    root = tk.Tk()
    FileMoverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()