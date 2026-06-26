#!/usr/bin/env python3
"""
extract_text.py — 从本地文件提取文本内容
支持格式：TXT, DOCX, PDF
用法：python3 extract_text.py <文件路径或目录路径>
"""
import sys
import os

def extract_txt(path):
    for enc in ['utf-8', 'gbk', 'utf-16']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except:
            continue
    return ""

def extract_docx(path):
    try:
        import docx
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except ImportError:
        return f"[需要安装 python-docx：pip install python-docx]"

def extract_pdf(path):
    try:
        import pdfplumber
        text = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text.append(t)
        return "\n".join(text)
    except ImportError:
        return f"[需要安装 pdfplumber：pip install pdfplumber]"

def extract_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.txt':
        return extract_txt(path)
    elif ext == '.docx':
        return extract_docx(path)
    elif ext == '.pdf':
        return extract_pdf(path)
    else:
        return f"[不支持的格式: {ext}]"

def main():
    if len(sys.argv) < 2:
        print("用法：python3 extract_text.py <文件路径或目录路径>")
        sys.exit(1)

    target = os.path.expanduser(sys.argv[1])
    files = []

    if os.path.isdir(target):
        for f in sorted(os.listdir(target)):
            if f.lower().endswith(('.txt', '.docx', '.pdf')):
                files.append(os.path.join(target, f))
    elif os.path.isfile(target):
        files = [target]
    else:
        print(f"路径不存在：{target}")
        sys.exit(1)

    if not files:
        print("未找到支持的文件（.txt / .docx / .pdf）")
        sys.exit(1)

    print(f"找到 {len(files)} 个文件：")
    all_text = []
    for f in files:
        print(f"  ▶ {os.path.basename(f)}")
        content = extract_file(f)
        all_text.append(f"\n\n{'='*60}\n【文件】{os.path.basename(f)}\n{'='*60}\n{content}")

    combined = "\n".join(all_text)
    print(f"\n总字符数：{len(combined)}")
    print(combined[:3000] + "\n...[截断显示前3000字符]" if len(combined) > 3000 else combined)

if __name__ == "__main__":
    main()
