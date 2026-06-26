#!/usr/bin/env python3
import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

try:
    import ur_rtde
    print(f"[OK] ur_rtde imported successfully")
    print(f"ur_rtde location: {ur_rtde.__file__}")
except ImportError as e:
    print(f"[FAIL] Cannot import ur_rtde: {e}")
    print("\nTrying to install...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ur_rtde"])
