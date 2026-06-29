"""
convert_to_md.py — Chuyển đổi file truyện sang .md
Supports: .txt, .epub, .docx, .html, .pdf
Usage: python convert_to_md.py <input_path>
"""
import sys, subprocess, os, shutil
from pathlib import Path

input_path = Path(sys.argv[1])
out = input_path.with_suffix('.md')

ext = input_path.suffix.lower()

if ext == '.txt':
    shutil.copy2(input_path, out)
    print(f"Copied {input_path} -> {out}")

elif ext == '.md':
    print(f"Already .md: {input_path}")

elif ext in ('.epub', '.docx', '.html'):
    try:
        subprocess.run(['pandoc', str(input_path), '-f', ext[1:], '-t', 'markdown', '-o', str(out)], check=True)
        print(f"Converted {input_path} -> {out}")
    except FileNotFoundError:
        print("ERROR: pandoc not found. Install with: winget install pandoc")
        sys.exit(1)

elif ext == '.pdf':
    try:
        import fitz
        doc = fitz.open(input_path)
        text = ""
        for page in doc:
            text += page.get_text()
        out.write_text(text, encoding='utf-8')
        print(f"Extracted PDF text -> {out}")
    except ImportError:
        print("ERROR: pymupdf not installed. Run: pip install pymupdf")
        sys.exit(1)
else:
    print(f"Unsupported format: {ext}")
    sys.exit(1)
