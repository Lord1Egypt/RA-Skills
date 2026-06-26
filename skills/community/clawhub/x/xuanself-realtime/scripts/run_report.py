#!/usr/bin/env python3
"""run_report.py — xuanself-realtime v3.0 快捷执行入口"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_generator import build_report
from data_parser import clean_bom

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='xuanself_raw.json')
    ap.add_argument('--output', default='output/report.md')
    ap.add_argument('--category', default='血糖检测设备')
    ap.add_argument('--country', default='俄罗斯联邦')
    args = ap.parse_args()
    clean_bom(args.input)
    with open(args.input, encoding='utf-8', errors='replace') as f:
        raw = json.load(f)
    md = build_report(raw, category=args.category, country=args.country)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(md)
    print('OK: {} ({} lines)'.format(args.output, md.count('\n')))
    docx = args.output.replace('.md', '.docx')
    try:
        from word_exporter import markdown_to_docx
        markdown_to_docx(md, docx)
        print('OK: {}'.format(docx))
    except Exception as e:
        print('WARN: docx export skipped ({})'.format(e))

if __name__ == '__main__':
    main()
