#!/usr/bin/env python3
"""
Launch ZW3D CAD software
"""

import os
import sys
import subprocess
import glob
from pathlib import Path

def find_zw3d_executable():
    """Search for ZW3D executable in common installation paths"""
    
    # Common installation paths
    search_paths = [
        r"C:\Program Files\ZWSoft\ZW3D",
        r"C:\Program Files (x86)\ZWSoft\ZW3D",
        r"D:\Program Files\ZWSOFT\ZW3D 2026",
        r"D:\Program Files\ZWSOFT\ZW3D WuKong 2027",
    ]
    
    # Search for zw3d.exe in these paths
    for base_path in search_paths:
        if os.path.exists(base_path):
            # Look for version subdirectories
            for version_dir in glob.glob(os.path.join(base_path, "*")):
                if os.path.isdir(version_dir):
                    exe_path = os.path.join(version_dir, "zw3d.exe")
                    if os.path.exists(exe_path):
                        return exe_path
            # Also check directly in base path
            exe_path = os.path.join(base_path, "zw3d.exe")
            if os.path.exists(exe_path):
                return exe_path
    
    # Try to find via registry or environment variable
    if "ZW3D_PATH" in os.environ:
        env_path = os.environ["ZW3D_PATH"]
        if os.path.exists(env_path):
            return env_path
    
    return None

def launch_zw3d(file_path=None):
    """Launch ZW3D, optionally with a file"""
    
    exe_path = find_zw3d_executable()
    
    if not exe_path:
        print("Error: Could not find ZW3D installation.")
        print("Please ensure ZW3D is installed in one of these locations:")
        print("  - C:\\Program Files\\ZWSoft\\ZW3D\\")
        print("  - C:\\Program Files (x86)\\ZWSoft\\ZW3D\\")
        print("\nOr set ZW3D_PATH environment variable to the zw3d.exe location.")
        return False
    
    print(f"Found ZW3D at: {exe_path}")
    
    try:
        if file_path and os.path.exists(file_path):
            # Launch with file
            subprocess.Popen([exe_path, file_path], shell=False)
            print(f"Launching ZW3D with file: {file_path}")
        else:
            # Launch without file
            subprocess.Popen([exe_path], shell=False)
            print("Launching ZW3D...")
        
        return True
    except Exception as e:
        print(f"Error launching ZW3D: {e}")
        return False

if __name__ == "__main__":
    file_to_open = sys.argv[1] if len(sys.argv) > 1 else None
    success = launch_zw3d(file_to_open)
    sys.exit(0 if success else 1)
