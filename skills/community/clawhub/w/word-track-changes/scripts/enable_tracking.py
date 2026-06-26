#!/usr/bin/env python3
"""CLI: 在Word文档中启用修订追踪"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from track_changes import enable_track_changes

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python enable_tracking.py <input.docx> <output.docx>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    enable_track_changes(input_path, output_path)
    print(f"✓ Track changes enabled: {output_path}")
