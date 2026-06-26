"""将 COSMIC 拆解明细的 Markdown 表格转换为 UTF-8 BOM 编码的 CSV 文件。

用法：python md2csv.py <拆解明细.md路径> <输出CSV路径>
"""
import csv
import re
import sys
import pathlib
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def md_table_to_csv(md_path: str, csv_path: str) -> None:
    content = pathlib.Path(md_path).read_text(encoding="utf-8")
    lines = [l.strip() for l in content.splitlines() if l.strip().startswith("|")]

    separator_re = re.compile(r"^\|[\s\-:|]+\|$")
    data_lines = [l for l in lines if not separator_re.match(l)]

    if not data_lines:
        logger.warning("未在 %s 中找到任何表格数据", md_path)
        sys.exit(1)

    row_count = 0
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        for line in data_lines:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            writer.writerow(cells)
            row_count += 1

    logger.info("CSV 已导出: %s（共 %d 行，含表头）", csv_path, row_count)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"用法: python {sys.argv[0]} <拆解明细.md路径> <输出CSV路径>")
        sys.exit(1)
    md_table_to_csv(sys.argv[1], sys.argv[2])
