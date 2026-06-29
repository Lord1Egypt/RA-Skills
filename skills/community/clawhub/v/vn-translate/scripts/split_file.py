"""
split_file.py — Cắt file .md thành raw/part_xxx.md, mỗi file ~12KB, chỉ cắt tại \n
Usage: python split_file.py <input.md> [output_dir]
"""
import sys
from pathlib import Path

input_file = Path(sys.argv[1])
out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('raw')
out_dir.mkdir(parents=True, exist_ok=True)

target_size = 12 * 1024  # ~12KB
text = input_file.read_text(encoding='utf-8')

lines = text.split('\n')
chunks = []
current_lines = []
current_size = 0

for line in lines:
    line_size = len(line.encode('utf-8')) + 1  # +1 for newline
    if current_size + line_size > target_size and current_lines:
        chunks.append('\n'.join(current_lines))
        current_lines = [line]
        current_size = line_size
    else:
        current_lines.append(line)
        current_size += line_size

if current_lines:
    chunks.append('\n'.join(current_lines))

total_parts = len(chunks)
pad = len(str(total_parts))

for i, chunk in enumerate(chunks, 1):
    part_file = out_dir / f"part_{i:0{pad}d}.md"
    part_file.write_text(chunk, encoding='utf-8')

print(f"Split {input_file} into {total_parts} parts in {out_dir}/")
for p in sorted(out_dir.iterdir()):
    size_kb = len(p.read_bytes()) / 1024
    print(f"  {p.name}: {size_kb:.1f} KB")
