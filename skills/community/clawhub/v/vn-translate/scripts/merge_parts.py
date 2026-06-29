"""
merge_parts.py — Nối tất cả file trong out/ thành full.md
Usage: python merge_parts.py [out_dir] [output_file]
"""
import sys
from pathlib import Path

out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('out')
output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('full.md')

parts = sorted(out_dir.glob('part_*.md'))
if not parts:
    print("ERROR: No part_*.md files found in", out_dir)
    sys.exit(1)

with open(output_file, 'w', encoding='utf-8') as out:
    for i, part in enumerate(parts):
        text = part.read_text(encoding='utf-8').strip()
        if text:
            if i > 0:
                out.write('\n\n')
            out.write(text)

print(f"Merged {len(parts)} parts into {output_file}")
print(f"File size: {len(output_file.read_bytes()) / 1024:.1f} KB")
