"""
批量生成二维码 - 从 Excel/CSV/TXT 读取数据，本地批量生成二维码图片。

用法:
  python scripts/batch_generate.py --input <文件> --output-dir <目录> [选项]

选项:
  --column <列名或索引>     指定数据列（Excel/CSV），不指定时自动检测
  --size                   尺寸，默认 400
  --format                 png|svg，默认 png
  --error-correction       L|M|Q|H，默认 M
  --border                 边框宽度，默认 2
  --zip                    打包为 zip

输出 JSON:
  成功: {"total": N, "success": N, "failed": N, "output_dir": "...", "zip_file": "..."|null, "errors": [...]}
  需要选列: {"need_column": true, "columns": [...], "preview": [...], "message": "..."}
  错误: {"error": "..."}
"""

import sys
import json
import os
import argparse
import csv
from pathlib import Path

ECC_MAP_LOCAL = {"L": 1, "M": 0, "Q": 3, "H": 2}


# ── 文件读取 ──────────────────────────────────────────────

def read_txt(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def read_csv_file(filepath: str, column=None):
    with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        return [], None
    return _extract_column(rows, column)


def read_excel(filepath: str, column=None):
    import openpyxl

    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    ws = wb.active
    rows = []
    for row in ws.iter_rows(values_only=True):
        rows.append([str(c) if c is not None else "" for c in row])
    wb.close()
    if not rows:
        return [], None
    return _extract_column(rows, column)


def _extract_column(rows: list[list[str]], column):
    headers = rows[0]
    data_rows = rows[1:] if len(rows) > 1 else []

    if column is not None:
        col_idx = _resolve_column_index(headers, column)
        if col_idx is None:
            return None, {
                "need_column": True,
                "columns": headers,
                "preview": rows[:6],
                "message": f"找不到列 '{column}'，请从以下列中选择",
            }
        return [r[col_idx] for r in data_rows if col_idx < len(r) and r[col_idx].strip()], None

    col_idx = _auto_detect_column(headers)
    if col_idx is None:
        return None, {
            "need_column": True,
            "columns": headers,
            "preview": rows[:6],
            "message": "无法自动判断数据列，请指定 --column 参数",
        }
    return [r[col_idx] for r in data_rows if col_idx < len(r) and r[col_idx].strip()], None


def _resolve_column_index(headers: list[str], column) -> int | None:
    try:
        idx = int(column)
        return idx if 0 <= idx < len(headers) else None
    except ValueError:
        pass
    col_lower = str(column).lower().strip()
    for i, h in enumerate(headers):
        if h.strip().lower() == col_lower:
            return i
    return None


def _auto_detect_column(headers: list[str]) -> int | None:
    keywords = ["data", "text", "content", "url", "link", "内容", "文本", "数据", "链接", "网址"]
    for i, h in enumerate(headers):
        h_lower = h.strip().lower()
        for kw in keywords:
            if kw in h_lower:
                return i
    if len(headers) == 1:
        return 0
    return None


# ── 本地生成 ──────────────────────────────────────────────

def generate_local(data: str, filepath: str, size: int, fmt: str, ecc: str, border: int):
    import qrcode
    import qrcode.image.svg

    qr = qrcode.QRCode(
        error_correction=ECC_MAP_LOCAL.get(ecc, 0),
        box_size=max(1, size // 41),
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    if fmt == "svg":
        img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
        img.save(filepath)
    else:
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((size, size))
        img.save(filepath)


def _check_local_available() -> bool:
    try:
        import qrcode  # noqa: F401
        return True
    except ImportError:
        return False


# ── 执行 ──────────────────────────────────────────────

def run_image_mode(items: list[str], args):
    if not args.output_dir:
        print(json.dumps({"error": "必须指定 --output-dir"}, ensure_ascii=False))
        sys.exit(1)

    if not _check_local_available():
        print(json.dumps({"error": "本地 qrcode 库未安装，请先执行 pip install qrcode Pillow"}, ensure_ascii=False))
        sys.exit(1)

    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    size_int = int(args.size.split("x")[0])

    success = 0
    failed = 0
    errors = []

    for i, data in enumerate(items):
        filename = f"{i + 1}.{args.fmt}"
        filepath = os.path.join(output_dir, filename)
        try:
            generate_local(data, filepath, size_int, args.fmt, args.ecc, args.border)
            success += 1
        except Exception as e:
            failed += 1
            errors.append({"index": i + 1, "data": data, "error": str(e)})

    result = {
        "total": len(items),
        "success": success,
        "failed": failed,
        "output_dir": output_dir,
        "zip_file": None,
        "errors": errors,
    }

    if args.do_zip and success > 0:
        import shutil
        zip_path = shutil.make_archive(output_dir, "zip", output_dir)
        result["zip_file"] = zip_path

    print(json.dumps(result, ensure_ascii=False))


# ── 入口 ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument("--column", default=None, help="指定数据列（列名或索引）")
    parser.add_argument("--output-dir", required=True, help="图片输出目录")
    parser.add_argument("--zip", action="store_true", dest="do_zip", help="打包为 zip")
    parser.add_argument("--size", default="400")
    parser.add_argument("--format", default="png", dest="fmt", choices=["png", "svg"])
    parser.add_argument("--error-correction", default="M", dest="ecc", choices=["L", "M", "Q", "H"])
    parser.add_argument("--border", type=int, default=2)
    args = parser.parse_args()

    input_path = args.input
    ext = Path(input_path).suffix.lower()

    if ext == ".txt":
        items = read_txt(input_path)
        need_col_info = None
    elif ext == ".csv":
        items, need_col_info = read_csv_file(input_path, args.column)
    elif ext in (".xlsx", ".xls"):
        items, need_col_info = read_excel(input_path, args.column)
    else:
        print(json.dumps({"error": f"不支持的文件格式: {ext}，支持 txt/csv/xlsx"}, ensure_ascii=False))
        sys.exit(1)

    if need_col_info:
        print(json.dumps(need_col_info, ensure_ascii=False))
        sys.exit(0)

    if not items:
        print(json.dumps({"error": "文件中未读取到有效数据"}, ensure_ascii=False))
        sys.exit(1)

    run_image_mode(items, args)


if __name__ == "__main__":
    main()
