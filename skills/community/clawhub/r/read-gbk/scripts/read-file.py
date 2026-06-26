#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
read-file.py - 读取本地文件，支持 GBK/UTF-8 编码自动检测

用法:
    python read-file.py <文件路径>

支持:
    - .txt, .md, .csv, .log, .json, .xml, .ini, .cfg 等文本文件
    - .docx Word 文档（需要 python-docx 库）
    - 编码自动检测：优先 GBK，失败则尝试 UTF-8
"""

import sys
import os
from pathlib import Path

# Windows 下设置控制台和 stdout 为 UTF-8 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
        # 设置控制台输出编码
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    except Exception:
        pass


def detect_and_read_text(file_path: str) -> str:
    """读取文本文件，自动检测编码"""
    encodings = ['gbk', 'utf-8', 'gb2312', 'utf-8-sig']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                if encoding != 'utf-8':
                    print(f"[编码检测：{encoding}]", file=sys.stderr)
                return content
        except UnicodeDecodeError:
            continue
        except Exception as e:
            raise e
    
    raise UnicodeDecodeError(
        'unknown', b'', 0, 1, 
        f'无法用 GBK/UTF-8/GB2312/UTF-8-SIG 解码文件：{file_path}'
    )


def read_docx(file_path: str) -> str:
    """读取 .docx 文件，自动安装 python-docx 如果缺失"""
    try:
        from docx import Document
    except ImportError:
        print(f"[自动安装] 检测到 python-docx 未安装，正在安装...", file=sys.stderr)
        import subprocess
        
        # 获取当前 Python 的 pip 路径
        pip_cmd = [sys.executable, '-m', 'pip', 'install', 'python-docx', '-q']
        
        try:
            subprocess.run(pip_cmd, check=True, capture_output=True)
            print(f"[自动安装] python-docx 安装成功", file=sys.stderr)
            from docx import Document
        except subprocess.CalledProcessError as e:
            raise ImportError(
                f"python-docx 安装失败：{e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)}\n"
                f"请手动安装：{sys.executable} -m pip install python-docx"
            )
    
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    
    if not paragraphs:
        return "[文档内容为空]"
    
    return '\n'.join(paragraphs)


def read_pdf(file_path: str) -> str:
    """读取 .pdf 文件，自动安装 pypdf 如果缺失"""
    try:
        from pypdf import PdfReader
    except ImportError:
        print(f"[自动安装] 检测到 pypdf 未安装，正在安装...", file=sys.stderr)
        import subprocess
        
        # 获取当前 Python 的 pip 路径
        pip_cmd = [sys.executable, '-m', 'pip', 'install', 'pypdf', '-q']
        
        try:
            subprocess.run(pip_cmd, check=True, capture_output=True)
            print(f"[自动安装] pypdf 安装成功", file=sys.stderr)
            from pypdf import PdfReader
        except subprocess.CalledProcessError as e:
            raise ImportError(
                f"pypdf 安装失败：{e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)}\n"
                f"请手动安装：{sys.executable} -m pip install pypdf"
            )
    
    try:
        reader = PdfReader(file_path)
        pages = []
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text and text.strip():
                pages.append(f"[第{i}页]\n{text.strip()}")
        
        if not pages:
            return "[PDF 内容为空或为扫描版图片]"
        
        return '\n\n'.join(pages)
    except Exception as e:
        raise RuntimeError(f"PDF 读取失败：{e}")


def main():
    if len(sys.argv) < 2:
        print("用法：python read-file.py <文件路径>", file=sys.stderr)
        print("示例：python read-file.py \"D:\\文档\\笔记.txt\"", file=sys.stderr)
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：文件不存在：{file_path}", file=sys.stderr)
        sys.exit(1)
    
    # 检查是否是文件
    if not os.path.isfile(file_path):
        print(f"错误：不是文件：{file_path}", file=sys.stderr)
        sys.exit(1)
    
    # 获取文件扩展名
    ext = Path(file_path).suffix.lower()
    
    try:
        if ext == '.docx':
            content = read_docx(file_path)
        elif ext == '.pdf':
            content = read_pdf(file_path)
        elif ext in ['.txt', '.md', '.csv', '.log', '.json', '.xml', '.ini', '.cfg', '.py', '.js', '.ts', '.html', '.htm', '.css']:
            content = detect_and_read_text(file_path)
        else:
            # 尝试作为文本读取
            content = detect_and_read_text(file_path)
        
        print(content)
        
    except ImportError as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"错误：编码检测失败 - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误：{type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
