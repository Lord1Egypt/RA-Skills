#!/usr/bin/env python3
"""CLI: 标记文本为删除"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from track_changes import TrackChangesProcessor

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python delete_revision.py <input.docx> <target_text> <output.docx> [author]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    target_text = sys.argv[2]
    output_path = sys.argv[3]
    author = sys.argv[4] if len(sys.argv) > 4 else "Agent"
    
    p = TrackChangesProcessor(input_path)
    p.set_author(author)
    p.replace_text_with_revision(target_text, "")
    p.save(output_path)
    p.cleanup()
    print(f"✓ Deletion marked: {output_path}")
