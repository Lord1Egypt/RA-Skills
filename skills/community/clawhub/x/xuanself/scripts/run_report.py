# -*- coding: utf-8 -*-
"""
Xuanself — Word报告导出快捷脚本
用法: python run_report.py <markdown文件> [输出docx文件]
"""
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR  = os.path.dirname(SCRIPT_DIR)
REPORT_GAMA = os.path.join(os.path.dirname(SKILL_DIR), "report-gama", "scripts")

sys.path.insert(0, REPORT_GAMA)

from word_exporter import WordExporter

def main():
    if len(sys.argv) < 2:
        print("用法: python run_report.py <markdown文件> [输出docx文件]")
        sys.exit(1)

    md_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else md_path.replace(".md", "_v5.docx")

    if not os.path.exists(md_path):
        print(f"文件不存在: {md_path}")
        sys.exit(1)

    exporter = WordExporter()
    result = exporter.markdown_to_docx(md_path, out_path)
    size_kb = os.path.getsize(result) / 1024
    print(f"OK: {result} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()
