# -*- coding: utf-8 -*-
"""
OCR批处理：对纯图片PDF（无文字层）用RapidOCR识别并提取条文。
自动检测哪些PDF提取结果为0，仅处理这些。

用法:
  # 批量处理目录下所有提取失败的PDF
  python scripts/ocr_batch.py <pdf_dir> <output_dir>

  # 单个文件OCR
  python scripts/ocr_batch.py <pdf_path> -o <output.json>
"""

import fitz, re, json, sys, os, argparse
import numpy as np
from pathlib import Path
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

sys.path.insert(0, os.path.dirname(__file__))
from extract_regulation import parse_articles, postprocess, validate, DEFAULT_CHAPTERS

DPI = 200


def is_empty_json(json_path):
    """检查JSON提取结果是否为空"""
    if not os.path.exists(json_path):
        return True
    try:
        d = json.load(open(json_path, encoding='utf-8'))
        return d.get('report', {}).get('total', 0) == 0
    except:
        return True


def ocr_pdf(pdf_path, ocr_engine, dpi=DPI):
    """逐页OCR，自动跳过有文字层的页面"""
    doc = fitz.open(str(pdf_path))
    all_lines = []

    for pi in range(len(doc)):
        page = doc[pi]
        text = page.get_text("text").strip()

        # 有文字层的页面直接用
        if len(text) > 50:
            for line in text.split('\n'):
                line = line.strip()
                if line and len(line) >= 2:
                    all_lines.append({"page": pi + 1, "text": line})
            continue

        # 无文字层 → OCR
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        arr = np.array(img)
        results, _ = ocr_engine(arr)

        if results:
            results.sort(key=lambda x: (x[0][0][1], x[0][0][0]))
            for r in results:
                t = r[1].strip()
                if t and len(t) >= 2 and r[2] > 0.3:
                    all_lines.append({"page": pi + 1, "text": t})

        if (pi + 1) % 10 == 0 or pi == len(doc) - 1:
            print(f"  Page {pi+1}/{len(doc)}")

    doc.close()
    return all_lines


def process_one(pdf_path, ocr_engine, output_path, chapters):
    """处理单个PDF"""
    print(f"  OCR: {Path(pdf_path).name}")
    lines = ocr_pdf(pdf_path, ocr_engine)
    print(f"  Lines: {len(lines)}")

    articles = parse_articles(lines, chapters)
    articles = postprocess(articles)
    report = validate(articles)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"articles": articles, "report": report}, f, ensure_ascii=False, indent=2)

    print(f"  Articles: {report['total']} (clean={report['clean']}, ocr_error={report['ocr_error']})")
    return report


def main():
    parser = argparse.ArgumentParser(description="OCR batch extract image-only PDFs")
    parser.add_argument("input", help="PDF file or directory")
    parser.add_argument("output_dir", nargs='?', help="Output directory (for batch mode)")
    parser.add_argument("-o", "--output", help="Output JSON (for single file mode)")
    parser.add_argument("--chapters", help="Chapter mapping JSON", default=None)
    args = parser.parse_args()

    chapters = DEFAULT_CHAPTERS
    if args.chapters:
        with open(args.chapters, 'r', encoding='utf-8') as f:
            chapters = json.load(f)

    input_path = Path(args.input)

    # 单文件模式
    if input_path.is_file():
        if not args.output:
            args.output = str(input_path.with_suffix('.json'))
        print("Initializing RapidOCR...")
        ocr = RapidOCR()
        process_one(str(input_path), ocr, args.output, chapters)
        return

    # 批量模式
    if not args.output_dir:
        print("Error: output_dir required for batch mode")
        sys.exit(1)

    pdf_dir = Path(args.input)
    out_dir = Path(args.output_dir)

    # 找出提取失败的PDF
    failed = []
    for pdf in sorted(pdf_dir.glob("*.pdf")):
        json_out = out_dir / (pdf.stem + ".json")
        if is_empty_json(str(json_out)):
            failed.append(pdf)

    print(f"PDFs needing OCR: {len(failed)}")
    if not failed:
        print("All done!")
        return

    print("Initializing RapidOCR...")
    ocr = RapidOCR()

    total = 0
    for i, pdf in enumerate(failed):
        print(f"\n[{i+1}/{len(failed)}] {pdf.name}")
        out = str(out_dir / (pdf.stem + ".json"))
        report = process_one(str(pdf), ocr, out, chapters)
        total += report['total']

    print(f"\nDone! {len(failed)} PDFs, {total} articles")


if __name__ == '__main__':
    main()
