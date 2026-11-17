#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RawReader.py — Đọc một đoạn ~12KB từ raw.md theo byte offset.

Cắt sạch tại ký tự xuống dòng (\\n) để không cắt giữa câu/đoạn.

Cách dùng:
  python RawReader.py <raw.md> <skip_bytes> <read_bytes>
  python RawReader.py raw.md 0 12288
  python RawReader.py raw.md $(python scripts/progress.py get) 12288

Tham số:
  skip_bytes  : số byte bỏ qua từ đầu file (offset hiện tại)
  read_bytes  : số byte muốn đọc (mục tiêu ~12KB = 12288)

Output:
  - In nội dung đoạn ra stdout (UTF-8)
  - In metadata ra stderr:
      SKIP=...
      READ=...          (số byte thực tế đã đọc, sau khi cắt tại \\n)
      NEXT_OFFSET=...   (offset cho lần đọc tiếp theo)
      EOF=0|1
      TOTAL=...         (kích thước file)
"""

from __future__ import annotations

import sys
from pathlib import Path


def read_chunk(path: Path, skip: int, read_size: int) -> tuple[str, int, int, bool]:
    """
    Đọc chunk từ file.
    Trả về: (text, bytes_actually_read, next_offset, is_eof)
    """
    data = path.read_bytes()
    total = len(data)

    if skip >= total:
        return "", 0, total, True

    end = min(skip + read_size, total)
    chunk = data[skip:end]

    # Cắt sạch tại \\n cuối cùng trong chunk (trừ khi đã tới EOF)
    is_eof = end >= total
    if not is_eof and b"\n" in chunk:
        # Tìm vị trí \\n cuối cùng
        last_nl = chunk.rfind(b"\n")
        if last_nl != -1:
            chunk = chunk[: last_nl + 1]  # giữ luôn \\n
            end = skip + last_nl + 1

    # Decode an toàn
    try:
        text = chunk.decode("utf-8")
    except UnicodeDecodeError:
        # Fallback: bỏ vài byte cuối nếu bị cắt giữa multi-byte char
        for i in range(1, 5):
            try:
                text = chunk[:-i].decode("utf-8")
                end = skip + len(chunk) - i
                break
            except UnicodeDecodeError:
                continue
        else:
            text = chunk.decode("utf-8", errors="replace")

    next_offset = end
    return text, end - skip, next_offset, is_eof


def main() -> int:
    if len(sys.argv) < 4:
        print(
            "Usage: python RawReader.py <raw.md> <skip_bytes> <read_bytes>",
            file=sys.stderr,
        )
        print("Example: python RawReader.py raw.md 0 12288", file=sys.stderr)
        return 1

    path = Path(sys.argv[1])
    try:
        skip = int(sys.argv[2])
        read_size = int(sys.argv[3])
    except ValueError:
        print("[LỖI] skip_bytes và read_bytes phải là số nguyên", file=sys.stderr)
        return 1

    if not path.exists():
        print(f"[LỖI] Không tìm thấy file: {path}", file=sys.stderr)
        return 1

    if skip < 0 or read_size <= 0:
        print("[LỖI] skip_bytes >= 0 và read_bytes > 0", file=sys.stderr)
        return 1

    text, actual_read, next_offset, is_eof = read_chunk(path, skip, read_size)
    total = path.stat().st_size

    # Metadata ra stderr
    print(f"SKIP={skip}", file=sys.stderr)
    print(f"READ={actual_read}", file=sys.stderr)
    print(f"NEXT_OFFSET={next_offset}", file=sys.stderr)
    print(f"EOF={1 if is_eof else 0}", file=sys.stderr)
    print(f"TOTAL={total}", file=sys.stderr)

    # Nội dung ra stdout
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
