# Pattern-Based FileMover

Pattern-Based FileMover is a Python application that automates file transfers (copy/move) between directories with highly customizable rules.  It features an intuitive graphical user interface (GUI) built with Tkinter, enabling users to easily manage complex file transfer tasks.

## Features

*   **Source and Destination Directory Selection:** Easily select source and destination directories using the browse buttons.
*   **Configuration Management:** Save, load, and reset configurations using JSON files for persistent rule management.
*   **Transfer Options:** Choose between copying or moving files, preserving directory structure, and renaming duplicates.
*   **Pattern-based Inclusions/Exclusions:** Define file inclusion and exclusion patterns using comma-separated wildcards (e.g., "*.txt, *.pdf" or "temp_*").  A help icon provides guidance on pattern syntax.
*   **Real-time Progress and Results:** Monitor the progress of file transfers and view results in the dedicated panel.
*   **Clean Empty Folders:**  Option to automatically remove empty folders after the transfer process.
*   **Preview Functionality:** Preview the effects of the transfer rules before execution to ensure desired outcomes.

## Technologies Used

*   Python
*   Tkinter
*   OS

## Installation

1.  **Prerequisites:** Python must be installed. Tkinter is typically included with standard Python installations.
2.  **Clone Repository:** 
    ```
    git clone https://github.com/nitin1625/Pattern-Based-FileMover.git
    ```
3.  **Run:**
    ```
    python exclude.py  # Transfer Files with Exclusion Patterns
    python include.py  # Transfer files with inclusion patterns

    ```

## Usage

1.  **Select Directories:** Use the "Browse" buttons to choose the source and destination directories.
2.  **Configuration:**  Use "Save Config" to save your settings to a JSON file and "Load Config" to load existing settings.
3.  **Transfer Options:** Select "Copy Files" or "Move Files," and check the boxes for "Preserve directory structure" and/or "Rename duplicates" as needed.
4.  **Exclusion Patterns:** Enter comma-separated file patterns in the "Exclusion Patterns" field.
5.  **Start Transfer:** Click "Start Transfer" to begin the process.  Use "Preview" to see the results beforehand.
6.  **Clean Empty Folders:**  Click "Clean Empty Folders" after the transfer to remove any remaining empty directories in the destination.

## Configuration (config.json Example)

```json
{
  "source_directory": "/path/to/source",
  "destination_directory": "/path/to/destination",
  "copy_files": true,  # or false for Move Files
  "preserve_directory_structure": true,
  "rename_duplicates": false,
  "exclude_patterns": ["temp_*", "*.bak"]
}

```

## Test and Run 

* Direct to dist folder and run .exe file as per requirement .
* exclude.exe for tasks related to File Mover with Exclusion patterns .
* include.exe for tasks related to File Mover With Inclusion Patterns.
