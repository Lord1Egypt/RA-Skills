#!/usr/bin/env python3
"""Cleanup script before GitHub upload"""
import os
import shutil

base = os.path.dirname(os.path.abspath(__file__))

# Files and directories to remove
to_remove = [
    os.path.join(base, 'scripts', '__pycache__'),
    os.path.join(base, 'scripts', '_drafts'),
    os.path.join(base, 'nul'),
]

removed = []
for path in to_remove:
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            removed.append(f"[DIR]  {path}")
        else:
            os.remove(path)
            removed.append(f"[FILE] {path}")

print("=" * 50)
print("Cleanup Complete!")
print("=" * 50)
if removed:
    print("Removed:")
    for r in removed:
        print(f"  - {r}")
else:
    print("Nothing to remove (already clean)")
print("=" * 50)