"""DOCX → HTML

用法:
    python docx_to_html.py input.docx [output.html]

参数:
    input.docx  - DOCX 文件路径
    output.html - 输出文件路径 (默认: output.html)
"""
from docx import Document
import sys
import os


def main():
    if len(sys.argv) < 2:
        print("用法: python docx_to_html.py input.docx [output.html]")
        sys.exit(1)

    docx_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "output.html"

    if not os.path.isfile(docx_path):
        print(f"错误: 文件不存在 - {docx_path}")
        sys.exit(1)

    doc = Document(docx_path)

    def para_to_html(para):
        text = para.text
        style = para.style.name.lower()
        if "heading 1" in style or "title" in style:
            return f"<h1>{text}</h1>"
        elif "heading 2" in style:
            return f"<h2>{text}</h2>"
        elif "heading 3" in style:
            return f"<h3>{text}</h3>"
        elif "list" in style:
            return f"<li>{text}</li>"
        else:
            return f"<p>{text}</p>"

    parts = [
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        '<style>body{font-family:sans-serif;max-width:800px;margin:2em auto;padding:0 1em;}'
        'h1{color:#333;}h2{color:#555;border-bottom:1px solid #eee;}</style></head><body>'
    ]
    for para in doc.paragraphs:
        if para.text.strip():
            parts.append(para_to_html(para))
    parts.append("</body></html>")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"完成: {docx_path} -> {out_path}")


if __name__ == "__main__":
    main()