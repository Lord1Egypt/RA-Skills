#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""诊断 ur_rtde 导入问题"""

import sys
import os

print("=" * 50)
print("Python Import Diagnostics")
print("=" * 50)

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"\nsys.path:")
for i, p in enumerate(sys.path):
    print(f"  [{i}] {p}")

print("\n" + "=" * 50)
print("Checking ur_rtde...")
print("=" * 50)

# Try to import
try:
    import ur_rtde
    print(f"\n[OK] ur_rtde imported successfully!")
    print(f"Location: {ur_rtde.__file__}")
    print(f"Version: {ur_rtde.__version__ if hasattr(ur_rtde, '__version__') else 'unknown'}")
except ImportError as e:
    print(f"\n[FAIL] ImportError: {e}")
    
    # Check if ur_rtde exists in site-packages
    for path in sys.path:
        if 'site-packages' in path:
            ur_rtde_path = os.path.join(path, 'ur_rtde')
            if os.path.exists(ur_rtde_path):
                print(f"  Found ur_rtde folder at: {ur_rtde_path}")
                print(f"  Files: {os.listdir(ur_rtde_path) if os.path.isdir(ur_rtde_path) else 'N/A'}")
            else:
                print(f"  Not found at: {ur_rtde_path}")

print("\n" + "=" * 50)
print("Done")
print("=" * 50)