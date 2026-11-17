"""ref-manager pipeline entry point.

Usage:
  python main.py --urls URL [URL ...] --pdfs FILE [FILE ...]
                 --folder DIR --apa "raw apa text" [--out DIR]
"""
import argparse
import json
import os
import sys

from common import find_doi
from extract_web import extract_web_metadata
from extract_pdf import extract_pdf_metadata
from crossref import crosscheck
from apa import format_apa
from ris_writer import records_to_ris, records_to_endnote_xml
from excel_writer import records_to_excel

EXCEL_NAME = "文献对账表.xlsx"
RIS_NAME = "references.ris"
XML_NAME = "references.xml"
JSON_NAME = "refs.json"


def collect_pdfs(folder):
    pdfs = []
    for root, _dirs, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".pdf"):
                pdfs.append(os.path.join(root, f))
    return sorted(pdfs)


def new_record(source_type, i):
    return {
        "id": i, "source_type": source_type,
        "original_url": None, "original_filename": None, "original_apa": None,
        "title": "", "authors": [], "year": "", "month": "", "day": "",
        "journal": "", "publisher": "", "volume": "", "issue": "", "pages": "",
        "doi": None, "url": None,
        "ref_type_ris": "ELEC", "ref_type_name": "Web Page",
        "apa": "", "check_result": "", "notes": [],
    }


def build_records(urls, pdfs, folder, apa_texts):
    records = []
    i = 0

    for url in urls:
        i += 1
        rec = new_record("web", i)
        try:
            rec.update(extract_web_metadata(url))
            rec = crosscheck(rec)
        except Exception as e:  # noqa: BLE001
            rec["check_result"] = "待人工确认"
            rec["notes"] = [f"网页提取失败：{e}"]
        rec["apa"] = format_apa(rec)
        records.append(rec)

    for path in pdfs:
        i += 1
        rec = new_record("pdf", i)
        try:
            extracted, _text = extract_pdf_metadata(path)
            rec.update(extracted)
            rec = crosscheck(rec)
        except Exception as e:  # noqa: BLE001
            rec["check_result"] = "待人工确认"
            rec["notes"] = [f"PDF 提取失败：{e}"]
        rec["apa"] = format_apa(rec)
        records.append(rec)

    if folder:
        for path in collect_pdfs(folder):
            i += 1
            rec = new_record("folder_pdf", i)
            try:
                extracted, _text = extract_pdf_metadata(path)
                rec.update(extracted)
                rec = crosscheck(rec)
            except Exception as e:  # noqa: BLE001
                rec["check_result"] = "待人工确认"
                rec["notes"] = [f"PDF 提取失败：{e}"]
            rec["apa"] = format_apa(rec)
            records.append(rec)

    for apa_text in apa_texts:
        i += 1
        rec = new_record("apa_text", i)
        rec["original_apa"] = apa_text
        doi = find_doi(apa_text)
        if doi:
            rec["doi"] = doi
            rec = crosscheck(rec)
            if rec.get("title"):
                rec["apa"] = format_apa(rec)
        else:
            rec["check_result"] = "待人工确认"
            rec["notes"] = ["原始 APA 文本中未找到 DOI，无法权威核对"]
        if not rec.get("apa"):
            rec["apa"] = apa_text
        records.append(rec)

    return records


def main():
    p = argparse.ArgumentParser(description="Extract references and build EndNote/APA/Excel outputs.")
    p.add_argument("--urls", nargs="*", default=[], help="web page URLs")
    p.add_argument("--pdfs", nargs="*", default=[], help="PDF file paths")
    p.add_argument("--folder", default=None, help="folder to scan for PDFs")
    p.add_argument("--apa", nargs="*", default=[], help="raw APA strings")
    p.add_argument("--out", default="./ref-manager-output", help="output directory")
    args = p.parse_args()

    if not (args.urls or args.pdfs or args.folder or args.apa):
        p.error("至少提供一种输入：--urls / --pdfs / --folder / --apa")

    records = build_records(args.urls, args.pdfs, args.folder, args.apa)
    os.makedirs(args.out, exist_ok=True)

    with open(os.path.join(args.out, JSON_NAME), "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    with open(os.path.join(args.out, RIS_NAME), "w", encoding="utf-8") as f:
        f.write(records_to_ris(records))

    with open(os.path.join(args.out, XML_NAME), "w", encoding="utf-8") as f:
        f.write(records_to_endnote_xml(records))

    xlsx_path = records_to_excel(records, os.path.join(args.out, EXCEL_NAME))

    n_total = len(records)
    n_fixed = sum(1 for r in records if r["check_result"] == "已修正")
    n_ok = sum(1 for r in records if r["check_result"] == "原样正确")
    n_manual = sum(1 for r in records if r["check_result"] == "待人工确认")

    print(f"[ref-manager] 处理 {n_total} 条：已修正 {n_fixed} / 原样正确 {n_ok} / 待人工确认 {n_manual}")
    print(f"[ref-manager] 输出目录：{os.path.abspath(args.out)}")
    print(f"[ref-manager] 生成：{RIS_NAME}、{XML_NAME}、{EXCEL_NAME}、{JSON_NAME}")
    for r in records:
        flag = {"已修正": "[修正]", "原样正确": "[OK]", "待人工确认": "[待确认]"}[r["check_result"]]
        note = f"  备注：{'；'.join(r['notes'])}" if r["notes"] else ""
        print(f"  {flag} #{r['id']} {r['apa'] or r.get('title') or '(无标题)'}{note}")


if __name__ == "__main__":
    sys.exit(main())
