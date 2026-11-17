#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_chapters.py — Gộp toàn bộ chương trong Chapters/ thành một file Full.md.

Quy tắc mặc định:
  • Chỉ đọc file .md nằm TRỰC TIẾP trong Chapters/ (bỏ qua _old/ và thư mục con)
  • Sắp xếp theo số chương (Chương 1 → Chương 30)
  • Nếu trùng số chương → giữ file có thời gian sửa MỚI NHẤT (bỏ version cũ)

Cách dùng:
  python merge_chapters.py                      # xuất ra Full.md cạnh Chapters/
  python merge_chapters.py --out path/to/x.md   # xuất ra chỗ khác
  python merge_chapters.py --all                # gộp luôn các version trùng số
  python merge_chapters.py --title "Tên"        # đổi tiêu đề file tổng hợp
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

CHAPTER_RE = re.compile(r"Chương\s+(\d+)", re.IGNORECASE)
PAGE_BREAK = '<div style="page-break-after: always;"></div>'


def find_chapter_files(chapters_dir: Path) -> list[Path]:
    """File .md ở cấp cao nhất của Chapters/ — không đệ quy (tự loại _old/)."""
    return sorted(
        p for p in chapters_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".md"
    )


def chapter_number(path: Path) -> int | None:
    m = CHAPTER_RE.search(path.stem)
    return int(m.group(1)) if m else None


def read_text(path: Path) -> str:
    """Đọc file UTF-8, tự bỏ BOM, cắt khoảng trắng thừa 2 đầu."""
    return path.read_text(encoding="utf-8-sig", errors="replace").strip()


def chapter_label(path: Path) -> str:
    """Tên chương: phần sau 'Chương N —' trong tên file."""
    n = chapter_number(path)
    m = re.match(rf"Chương\s+{n}\s*[—\-–:.]?\s*(.*)", path.stem, re.IGNORECASE)
    label = m.group(1).strip() if m and m.group(1).strip() else path.stem
    return label


def build_full_md(chosen: list[Path], title: str) -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# {title}",
        "",
        f"> **Bản tổng hợp {len(chosen)} chương** — sinh lúc {generated} bởi `merge_chapters.py`",
        "",
        "## Mục lục",
        "",
    ]
    for f in chosen:
        n = chapter_number(f)
        lines.append(f"- **Chương {n}** — {chapter_label(f)}")
    lines += ["", "---", ""]

    for i, f in enumerate(chosen):
        lines.append(read_text(f))
        lines.append("")
        if i < len(chosen) - 1:
            lines.append("---")
            lines.append(PAGE_BREAK)
            lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Gộp các chương thành Full.md")
    parser.add_argument("--chapters", type=Path, default=None,
                        help="Thư mục chứa chương (mặc định: Chapters/ cạnh script)")
    parser.add_argument("--out", type=Path, default=None,
                        help="File xuất ra (mặc định: Full.md cạnh Chapters/)")
    parser.add_argument("--title", default=None, help="Tiêu đề file tổng hợp")
    parser.add_argument("--all", action="store_true",
                        help="Gộp luôn các version trùng số chương")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent
    chapters_dir = (args.chapters or base / "Chapters").resolve()
    out_path = (args.out or base / "Full.md").resolve()

    if not chapters_dir.is_dir():
        print(f"[LỖI] Không tìm thấy thư mục: {chapters_dir}", file=sys.stderr)
        return 1

    files = find_chapter_files(chapters_dir)
    if not files:
        print(f"[LỖI] Không có file .md nào trong: {chapters_dir}", file=sys.stderr)
        return 1

    # Gom file theo số chương; file không có số chương thì cảnh báo
    by_number: dict[int, list[Path]] = {}
    unnamed: list[Path] = []
    for f in files:
        n = chapter_number(f)
        if n is None:
            unnamed.append(f)
        else:
            by_number.setdefault(n, []).append(f)

    for f in unnamed:
        print(f"[CẢNH BÁO] Bỏ qua (tên không có số chương): {f.name}")

    # Chọn file: mặc định giữ bản MỚI NHẤT cho mỗi số chương
    chosen: list[Path] = []
    skipped: list[tuple[Path, str]] = []
    for n in sorted(by_number):
        group = sorted(by_number[n], key=lambda p: p.stat().st_mtime)
        if args.all:
            chosen.extend(group)
        else:
            chosen.append(group[-1])  # mtime lớn nhất = mới nhất
            for old in group[:-1]:
                skipped.append((old, f"trùng số Chương {n} — giữ version mới hơn"))

    title = args.title or base.name
    full_md = build_full_md(chosen, title)
    out_path.write_text(full_md, encoding="utf-8")

    # Báo cáo kết quả
    nums = [chapter_number(f) for f in chosen]
    missing = [n for n in range(1, max(nums) + 1) if n not in nums]
    print(f"[OK] Đã gộp {len(chosen)} chương -> {out_path}")
    print(f"     Phạm vi: Chương {min(nums)} → Chương {max(nums)}")
    if missing:
        print(f"     [CẢNH BÁO] Thiếu chương: {missing}")
    for f, reason in skipped:
        print(f"     [BỎ QUA] {f.name} ({reason})")
    if unnamed:
        print(f"     [BỎ QUA] {len(unnamed)} file không xác định được số chương")
    return 0


if __name__ == "__main__":
    sys.exit(main())
