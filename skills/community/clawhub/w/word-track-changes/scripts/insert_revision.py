#!/usr/bin/env python3
"""CLI: 插入带修订标记的文本"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from track_changes import TrackChangesProcessor

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python insert_revision.py <input.docx> <search_text> <new_text> <output.docx> [author]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    search_text = sys.argv[2]
    new_text = sys.argv[3]
    output_path = sys.argv[4]
    author = sys.argv[5] if len(sys.argv) > 5 else "Agent"
    
    p = TrackChangesProcessor(input_path)
    p.set_author(author)
    p.replace_text_with_revision(search_text, new_text)
    p.save(output_path)
    p.cleanup()
    print(f"✓ Revision inserted: {output_path}")
