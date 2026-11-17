"""
format_output.py — Định dạng lại các file đã dịch trong out/ theo yêu cầu của người dùng:
  1. Bỏ ký tự thụt đầu dòng to-width \u3000\u3000 ở đầu mỗi dòng.
  2. Chuyển marker chương (第NN章 / Chương NN / 间章 / 简介 / 介绍) thành heading:
       # Chương N: [tiêu đề]      (mặc định chỉ "# Chương N" nếu không có bản đồ tiêu đề)
       # Ngoại truyện: [tiêu đề]  (cho 间章)
       # Giới thiệu               (cho 简介)
       ## Tóm tắt                 (cho 介绍)
  3. Gộp marker kép "第NN章" + "Chương NN" thành MỘT heading duy nhất.
  4. Dọn các dòng trống lặp liên tiếp (giữ tối đa 1 dòng trống).

Usage:
  python format_output.py [out_dir] [titles_json]

  out_dir     : thư mục chứa out/part_*.md (mặc định 'out')
  titles_json : file JSON tùy chọn ánh xạ số chương -> tiêu đề, VD:
                {"1": "Phát hiện bí mật của bố mẹ", "7": "Ổ cứng bí mật của bố"}
  Ngoại truyện (间章) lấy tiêu đề từ key "ngoai_truyen" nếu có.

Ví dụ:
  python format_output.py out/ titles.json
"""
import json
import re
import sys
from pathlib import Path


def load_titles(path):
    if path and Path(path).exists():
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return {}


def clean_line(line: str) -> str:
    return line.lstrip("\u3000").rstrip("\r\n ")


def transform(text: str, titles: dict) -> str:
    interlude_title = titles.get("ngoai_truyen", "Ngoại truyện")
    lines = text.split("\n")
    out_lines = []
    i, n = 0, len(lines)
    while i < n:
        s = clean_line(lines[i])
        m_cn = re.fullmatch(r"第(\d+)章", s)
        m_vn = re.fullmatch(r"Chương\s*(\d+)", s)
        if m_cn:
            num = int(m_cn.group(1))
            if i + 1 < n and re.fullmatch(r"Chương\s*\d+", clean_line(lines[i + 1])):
                i += 1  # bỏ dòng "Chương NN" đi kèm
            title = titles.get(str(num), "")
            out_lines.append(f"# Chương {num}: {title}" if title else f"# Chương {num}")
            i += 1
            continue
        if m_vn:
            num = int(m_vn.group(1))
            title = titles.get(str(num), "")
            out_lines.append(f"# Chương {num}: {title}" if title else f"# Chương {num}")
            i += 1
            continue
        if s == "简介":
            out_lines.append("# Giới thiệu")
            i += 1
            continue
        if s == "介绍":
            out_lines.append("## Tóm tắt")
            i += 1
            continue
        if s == "间章":
            out_lines.append(f"# {interlude_title}")
            i += 1
            continue
        out_lines.append(s)
        i += 1
    # gộp dòng trống liên tiếp
    result, prev_empty = [], False
    for line in out_lines:
        is_empty = line.strip() == ""
        if is_empty and prev_empty:
            continue
        result.append(line)
        prev_empty = is_empty
    return "\n".join(result) + "\n"


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("out")
    titles = load_titles(sys.argv[2]) if len(sys.argv) > 2 else {}
    for f in sorted(out_dir.glob("part_*.md")):
        text = f.read_text(encoding="utf-8")
        new = transform(text, titles)
        f.write_text(new, encoding="utf-8")
        print(f"{f.name}: {len(text)} -> {len(new)} chars")
    # kiểm tra không còn \u3000
    total = sum(f.read_text(encoding="utf-8").count("\u3000")
                for f in out_dir.glob("part_*.md"))
    print(f"TOTAL \\u3000 remaining: {total}")


if __name__ == "__main__":
    main()
