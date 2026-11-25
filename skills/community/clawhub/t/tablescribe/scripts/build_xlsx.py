# -*- coding: utf-8 -*-
"""Export a reconstructed table to a four-sheet workbook (requires openpyxl).

Sheets
  主表      one record per row, numeric cells stored as real numbers
  列字典    column name / type / unit / group / confidence / inferred / source
  校验报告   flattened checks from verify_table.py --report
  还原说明   review queue, inferred names, skipped items

Formatting rules enforced here
  explicit font on every cell (no theme fallback)
  frozen header, bold white header on a dark fill
  column width from content, row height computed from the bottleneck cell
  empty cells stay empty (never 0, never "N/A")
  atomic write + read-back verification

Usage
  python build_xlsx.py rows.csv --columns cols.json --out out.xlsx \
         [--report verify.json] [--notes notes.json] [--font "Microsoft YaHei"]

Exit codes
  0  written and read-back verified
  1  written but read-back mismatch
  2  input error
  3  openpyxl missing
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError:  # pragma: no cover
    print("openpyxl is required: pip install openpyxl", file=sys.stderr)
    sys.exit(3)

NUM_RE = re.compile(r"-?\d+(?:[.,]\d+)?")
FULLWIDTH = str.maketrans("０１２３４５６７８９．－，％", "0123456789.-,%")
HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
MIN_ROW_HEIGHT = 18.0

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        pass


def norm(text) -> str:
    return (text or "").translate(FULLWIDTH).strip()


def to_number(text):
    raw = norm(text).replace(",", "")
    if not raw:
        return None
    match = NUM_RE.search(raw)
    if not match:
        return None
    try:
        return float(match.group())
    except ValueError:
        return None


def display_width(text) -> float:
    """Approximate width in Excel character units (CJK counts double)."""
    width = 0.0
    for char in str(text or ""):
        width += 2.0 if ord(char) > 0x2E80 else 1.0
    return width


def needed_lines(text, column_width) -> int:
    cap = max(column_width - 1.0, 4.0)
    total = 0
    for segment in str(text or "").split("\n"):
        total += max(1, math.ceil(display_width(segment) / cap))
    return total


def style_sheet(sheet, widths, header_row=1, font_name="Microsoft YaHei"):
    for index, width in enumerate(widths, start=1):
        sheet.column_dimensions[get_column_letter(index)].width = max(10.0, min(width + 2.0, 80.0))
    for cell in sheet[header_row]:
        cell.font = Font(name=font_name, size=11, bold=True, color="FFFFFF")
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    sheet.row_dimensions[header_row].height = 24
    sheet.freeze_panes = sheet.cell(row=header_row + 1, column=1)
    for row_index in range(header_row + 1, sheet.max_row + 1):
        lines = 1
        for col_index, width in enumerate(widths, start=1):
            cell = sheet.cell(row=row_index, column=col_index)
            cell.font = Font(name=font_name, size=11)
            horizontal = "right" if isinstance(cell.value, (int, float)) else "left"
            cell.alignment = Alignment(horizontal=horizontal, vertical="top", wrap_text=True)
            if cell.value is not None:
                lines = max(lines, needed_lines(cell.value, max(10.0, min(width + 2.0, 80.0))))
        sheet.row_dimensions[row_index].height = max(MIN_ROW_HEIGHT, lines * 15.5 + 4)


def write_main(book, rows, columns, font_name):
    sheet = book.active
    sheet.title = "主表"
    names = [item["name"] for item in columns]
    sheet.append(names)
    kinds = {item["name"]: item.get("type", "text") for item in columns}
    decimals = {item["name"]: int(item.get("decimals", 2)) for item in columns}

    for row in rows:
        values = []
        for name in names:
            raw = row.get(name, "")
            if kinds.get(name) in ("number", "int") and norm(raw):
                number = to_number(raw)
                if number is not None:
                    values.append(round(number, 6))
                    continue
            values.append(norm(raw) or None)
        sheet.append(values)

    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            name = names[cell.column - 1]
            kind = kinds.get(name)
            if kind in ("number", "int") and isinstance(cell.value, (int, float)):
                if kind == "number":
                    cell.number_format = "0." + "0" * max(decimals.get(name, 2), 0)
                else:
                    cell.number_format = "0"
                cell.alignment = Alignment(horizontal="right", vertical="top")

    widths = [max([display_width(name)] + [display_width(row.get(name, "")) for row in rows])
              for name in names]
    style_sheet(sheet, widths, font_name=font_name)
    return len(names)


def write_columns(book, columns, font_name):
    sheet = book.create_sheet("列字典")
    headers = ["列名", "类型", "单位", "父列", "小数位", "置信度", "是否推定", "来源"]
    sheet.append(headers)
    for item in columns:
        sheet.append([
            item["name"], item.get("type", "text"), item.get("unit") or "",
            item.get("group") or "", item.get("decimals", ""),
            item.get("confidence", ""), "是" if item.get("inferred") else "否",
            item.get("source", ""),
        ])
    widths = [22, 10, 10, 14, 8, 10, 10, 28]
    style_sheet(sheet, widths, font_name=font_name)


def write_report(book, report, font_name):
    sheet = book.create_sheet("校验报告")
    headers = ["校验项", "作用范围", "期望值", "实测值", "差额", "容差", "结论", "说明", "样本数"]
    sheet.append(headers)
    for check in (report or {}).get("checks", []):
        sheet.append([check.get("check"), check.get("target"), check.get("expected"),
                      check.get("actual"), check.get("diff"), check.get("tolerance"),
                      check.get("level"), check.get("note"), check.get("checked")])
    if not sheet.max_row > 1:
        sheet.append(["未提供校验报告", "", "", "", "", "", "open",
                      "必须先运行 verify_table.py 再导出", ""])
    widths = [30, 16, 14, 14, 12, 10, 10, 34, 10]
    style_sheet(sheet, widths, font_name=font_name)


def write_notes(book, notes, font_name):
    sheet = book.create_sheet("还原说明")
    headers = ["页", "行", "列", "问题", "候选值 A", "候选值 B", "结论", "备注"]
    sheet.append(headers)
    for item in (notes or {}).get("items", []):
        sheet.append([item.get("page"), item.get("row"), item.get("col"), item.get("issue"),
                      item.get("candidate_a"), item.get("candidate_b"),
                      item.get("decision"), item.get("note")])
    if not sheet.max_row > 1:
        sheet.append(["", "", "", "无未决疑点", "", "", "已复核", ""])
    widths = [6, 8, 16, 30, 14, 14, 16, 30]
    style_sheet(sheet, widths, font_name=font_name)


def read_back(path, expected_sheets, font_name):
    problems = []
    book = load_workbook(path)
    for name in expected_sheets:
        if name not in book.sheetnames:
            problems.append(f"missing sheet: {name}")
    for sheet in book.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value is None:
                    continue
                if not cell.font or cell.font.name != font_name:
                    problems.append(f"{sheet.title}!{cell.coordinate}: font "
                                    f"{cell.font.name if cell.font else None}")
                if isinstance(cell.value, str) and cell.value.startswith("#"):
                    problems.append(f"{sheet.title}!{cell.coordinate}: error text {cell.value}")
    book.close()
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Export a reconstructed table to xlsx.")
    parser.add_argument("csv_path")
    parser.add_argument("--columns", required=True, help="column model JSON")
    parser.add_argument("--out", required=True, help="target .xlsx path")
    parser.add_argument("--report", help="verify_table.py JSON report")
    parser.add_argument("--notes", help="review-queue JSON")
    parser.add_argument("--font", default="Microsoft YaHei")
    parser.add_argument("--total-labels", default="",
                        help="comma-separated labels; matching rows stay out of the main sheet")
    parser.add_argument("--encoding", default="utf-8-sig")
    args = parser.parse_args(argv)

    try:
        with open(args.csv_path, "r", encoding=args.encoding, newline="") as handle:
            rows = list(csv.DictReader(handle))
        with open(args.columns, "r", encoding="utf-8-sig") as handle:
            model = json.load(handle)
    except (OSError, json.JSONDecodeError, csv.Error) as exc:
        print(f"cannot read input: {exc}", file=sys.stderr)
        return 2

    columns = model["columns"] if isinstance(model, dict) else model
    if not columns:
        print("column model is empty", file=sys.stderr)
        return 2
    names = {item["name"] for item in columns}
    extra = [name for name in (rows[0].keys() if rows else []) if name not in names]
    if extra:
        print(f"warning: CSV columns missing from the model: {extra}", file=sys.stderr)

    report = {}
    if args.report:
        try:
            with open(args.report, "r", encoding="utf-8-sig") as handle:
                report = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"warning: cannot read report: {exc}", file=sys.stderr)

    notes = {}
    if args.notes:
        try:
            with open(args.notes, "r", encoding="utf-8-sig") as handle:
                notes = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"warning: cannot read notes: {exc}", file=sys.stderr)

    book = Workbook()
    total_labels = [item.strip() for item in args.total_labels.split(",") if item.strip()]
    dropped_totals = 0
    if total_labels:
        kept = []
        for row in rows:
            cells = [str(value or "").strip() for value in row.values()]
            if any(cell == label for cell in cells for label in total_labels):
                dropped_totals += 1
                continue
            kept.append(row)
        rows = kept
    column_count = write_main(book, rows, columns, args.font)
    write_columns(book, columns, args.font)
    write_report(book, report, args.font)
    write_notes(book, notes, args.font)

    target = os.path.abspath(args.out)
    temp = target + ".tmp.xlsx"
    try:
        book.save(temp)
        os.replace(temp, target)
    except OSError as exc:
        fallback = os.path.splitext(target)[0] + "_v2.xlsx"
        try:
            book.save(fallback)
            target = fallback
            print(f"target busy ({exc}); wrote {fallback}", file=sys.stderr)
        except OSError as exc2:
            print(f"cannot write workbook: {exc2}", file=sys.stderr)
            return 2
    finally:
        if os.path.exists(temp):
            try:
                os.remove(temp)
            except OSError:
                pass

    problems = read_back(target, ["主表", "列字典", "校验报告", "还原说明"], args.font)
    print(f"wrote {target}: rows={len(rows)} columns={column_count} sheets=4 "
          f"total_rows_skipped={dropped_totals}")
    print(f"read-back: {'ok' if not problems else str(len(problems)) + ' problem(s)'}")
    for item in problems[:10]:
        print(f"  - {item}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
