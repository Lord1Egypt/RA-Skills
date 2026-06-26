#!usr/bin/env python3
import pathlib
import sys

# Script để quét thư mục, đọc các file .py và trích xuất summary 
# (phần sau dòng '# -----') để tạo tài liệu py_docs.md tự động.

def extract_summary(file_path):
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        if '# -----' not in content:
            return None
        
        parts = content.split('# -----')
        summary_part = parts[-1]
        
        # Chỉ lấy các dòng bắt đầu bằng #
        summary_lines = [line for line in summary_part.splitlines() if line.strip().startswith('#')]
        return '\n'.join(summary_lines).strip() or None
    except Exception as e:
        return None

def main():
    target_dir = pathlib.Path.cwd()
    py_files = sorted(target_dir.glob('*.py'))
    # Loại bỏ chính script này nếu tồn tại trong thư mục
    py_files = [f for f in py_files if f.name != 'summary.py']

    docs = []
    for py_file in py_files:
        summary = extract_summary(py_file)
        if summary:
            docs.append(f"## {py_file.name}\n\n{summary}\n")

    if not docs:
        print("⚠️ Không có file .py nào chứa summary hợp lệ.")
        return

    output_path = target_dir / 'py_docs.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Python Scripts Documentation\n\n")
        f.write("Tự động tổng hợp từ các file `.py`.\n\n")
        f.write("\n---\n\n".join(docs))

    print(f"✅ Đã tạo {output_path} với {len(docs)} mục.")

if __name__ == "__main__":
    main()
