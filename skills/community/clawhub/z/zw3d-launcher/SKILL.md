---
name: zw3d-launcher
description: Launch ZW3D CAD software. Use when the user wants to open, start, or launch ZW3D CAD application. Handles finding the ZW3D executable and launching it with optional file opening.
---

# ZW3D Launcher

Launch ZW3D CAD software on Windows systems.

## Usage

When the user asks to open ZW3D:

1. Run the launch script: `python scripts/launch_zw3d.py`
2. If the user wants to open a specific file, pass the file path as argument: `python scripts/launch_zw3d.py "path/to/file.z3"

## How It Works

The script will:
1. Search common installation paths for ZW3D executable
2. Launch the application
3. Optionally open a specified file

## Common Installation Paths Checked

- `C:\Program Files\ZWSoft\ZW3D\*\zw3d.exe`
- `C:\Program Files (x86)\ZWSoft\ZW3D\*\zw3d.exe`
- Custom paths can be added to the script

## Notes

- ZW3D may take a few seconds to fully load
- If ZW3D is already running, a new instance may be launched depending on ZW3D's settings
