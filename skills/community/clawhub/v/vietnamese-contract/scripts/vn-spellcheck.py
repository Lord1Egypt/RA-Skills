#!/usr/bin/env python3
"""
Kiểm tra chính tả tiếng Việt trong file .docx
Chuyên dụng cho văn bản pháp lý.

Cách dùng:
    python vn-spellcheck.py <file.docx>
"""

import sys
import os
import subprocess


# Các từ CHẮC CHẮN SAI nếu tìm thấy
FORBIDDEN = [
    ("THUẮN", "THUẬN"),
    ("NHUẮN", "NHUẬN"),
    ("LỬI", "LỢI"),
    ("vình viễn", "vĩnh viễn"),
    ("nghìa vụ", "nghĩa vụ"),
    ("khắt phục", "khắc phục"),
    ("thương lương", "thương lượng"),
    ("bất khã kháng", "bất khả kháng"),
    ("chuyễn khoản", "chuyển khoản"),
    ("quyết tóan", "quyết toán"),
    ("thiêt hại", "thiệt hại"),
    ("phạm vị", "phạm vi"),
    ("hoạt \u0111\u00f4ng", "hoạt động"),
    ("h\u01a1p \u0111\u1ed3ng", "hợp đồng"),
    ("h\u1ee3p \u0111\u00f4ng", "hợp đồng"),
    ("thanh t\u00f3an", "thanh toán"),
    ("thu\u1eaen", "thuận"),
    ("nhu\u1eaen", "nhuận"),
    ("l\u1eedi", "lợi"),
    ("nh\u1eafn \u0111\u1ea7u", "nhận đầu"),
]

# Quốc hiệu phải có
REQUIRED = [
    ("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM", "Quốc hiệu"),
    ("Độc lập", "Tiêu ngữ (phần 1)"),
    ("Tự do", "Tiêu ngữ (phần 2)"),
    ("Hạnh phúc", "Tiêu ngữ (phần 3)"),
]


def extract_text(docx_path):
    """Xuất text từ .docx bằng pandoc"""
    try:
        result = subprocess.run(
            ["pandoc", docx_path, "-t", "plain", "--wrap=none"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            result = subprocess.run(
                ["pandoc", docx_path, "-o", "-"],
                capture_output=True, text=True, timeout=30
            )
        return result.stdout
    except FileNotFoundError:
        print("LỖI: Không tìm thấy pandoc.")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python vn-spellcheck.py <file.docx>")
        sys.exit(1)

    docx_path = sys.argv[1]
    if not os.path.exists(docx_path):
        print(f"LỖI: Không tìm thấy file: {docx_path}")
        sys.exit(1)

    print(f"🔍 Kiểm tra chính tả: {docx_path}")
    print("=" * 60)

    text = extract_text(docx_path)
    if not text.strip():
        print("⚠️  Không xuất được text từ file.")
        sys.exit(1)

    total_errors = 0
    total_warnings = 0

    # 1. Kiểm tra từ sai
    errors = []
    for wrong, correct in FORBIDDEN:
        start = 0
        while True:
            idx = text.find(wrong, start)
            if idx == -1:
                break
            line_num = text[:idx].count("\n") + 1
            line_start = text.rfind("\n", 0, idx) + 1
            line_end = text.find("\n", idx)
            if line_end == -1:
                line_end = len(text)
            context = text[line_start:line_end].strip()[:80]
            errors.append((line_num, wrong, correct, context))
            start = idx + len(wrong)

    if errors:
        print(f"\n❌ LỖI CHÍNH TẢ ({len(errors)} lỗi):")
        print("-" * 60)
        for line, wrong, correct, ctx in errors:
            print(f"  Dòng {line}: \"{wrong}\" → {correct}")
            print(f"    → {ctx}")
        total_errors += len(errors)

    # 2. Kiểm tra nội dung bắt buộc
    missing = []
    for phrase, label in REQUIRED:
        if phrase not in text:
            missing.append((label, phrase))

    if missing:
        print(f"\n⚠️  THIẾU NỘI DUNG ({len(missing)} mục):")
        print("-" * 60)
        for label, phrase in missing:
            print(f"  {label}: thiếu \"{phrase}\"")
        total_warnings += len(missing)

    # Tổng kết
    print("\n" + "=" * 60)
    if total_errors == 0 and total_warnings == 0:
        print("✅ KHÔNG PHÁT HIỆN LỖI CHÍNH TẢ!")
        print(f"   Đã kiểm tra {len(text.split())} từ, {len(FORBIDDEN)} mẫu lỗi,")
        print(f"   {len(REQUIRED)} nội dung bắt buộc.")
    else:
        print(f"📊 Kết quả: {total_errors} lỗi, {total_warnings} cảnh báo")
        if total_errors > 0:
            print("   → Cần sửa các LỖI trước khi giao file!")

    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
