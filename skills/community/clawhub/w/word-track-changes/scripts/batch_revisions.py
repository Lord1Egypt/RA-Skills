#!/usr/bin/env python3
"""CLI: 批量处理修订"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from track_changes import batch_revisions

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python batch_revisions.py <input.docx> <output.docx> <author>")
        print("  Revisions read from stdin as JSON array, e.g.")
        print('  [{"type":"replace","old":"...","new":"..."},{"type":"insert_after","search":"...","new":"..."}]')
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    author = sys.argv[3]
    
    import json
    revisions = json.load(sys.stdin)
    batch_revisions(input_path, revisions, author, output_path)
    print(f"✓ Batch revisions applied: {output_path}")
