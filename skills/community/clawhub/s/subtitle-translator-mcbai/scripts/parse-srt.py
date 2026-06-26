#!/usr/bin/env python3
"""
parse-srt.py - Parse SRT file thành JSON array
Tự động detect encoding: UTF-8, UTF-16, UTF-8 BOM, GB2312, Big5, Shift-JIS, EUC-KR, Windows-125x...

Usage: python parse-srt.py <file.srt>
Output: JSON array ra stdout (UTF-8)
"""

import sys
import json
import re

def detect_and_decode(filepath):
    """Đọc file và tự detect encoding, trả về string"""
    with open(filepath, 'rb') as f:
        raw = f.read()

    # 1. Check BOM trước
    bom_encodings = [
        (b'\xff\xfe\x00\x00', 'utf-32-le'),
        (b'\x00\x00\xfe\xff', 'utf-32-be'),
        (b'\xff\xfe',         'utf-16-le'),
        (b'\xfe\xff',         'utf-16-be'),
        (b'\xef\xbb\xbf',    'utf-8-sig'),
    ]
    for bom, enc in bom_encodings:
        if raw.startswith(bom):
            return raw.decode(enc), enc

    # 2. Thử chardet nếu có
    try:
        import chardet
        detected = chardet.detect(raw)
        enc = detected.get('encoding') or 'utf-8'
        confidence = detected.get('confidence', 0)
        if confidence > 0.7:
            try:
                return raw.decode(enc), enc
            except:
                pass
    except ImportError:
        pass

    # 3. Fallback: thử lần lượt các encoding phổ biến
    encodings_to_try = [
        'utf-8',
        'utf-8-sig',
        'utf-16',
        'utf-16-le',
        'utf-16-be',
        'gb18030',    # Chinese Simplified (superset of GB2312/GBK)
        'big5',       # Chinese Traditional
        'shift_jis',  # Japanese
        'euc-jp',     # Japanese
        'euc-kr',     # Korean
        'cp949',      # Korean Windows
        'windows-1252',  # Western European
        'windows-1250',  # Central European
        'windows-1251',  # Cyrillic
        'latin-1',    # Last resort (never fails)
    ]

    for enc in encodings_to_try:
        try:
            text = raw.decode(enc)
            # Sanity check: SRT phải có timecode pattern
            if re.search(r'\d{2}:\d{2}:\d{2}[,\.]\d{3}\s*-->', text):
                return text, enc
        except (UnicodeDecodeError, LookupError):
            continue

    # Absolute last resort
    return raw.decode('latin-1'), 'latin-1'


def parse_srt(filepath):
    """Parse SRT file, return list of subtitle dicts"""
    content, detected_enc = detect_and_decode(filepath)

    # Log encoding detected (to stderr, không ảnh hưởng JSON stdout)
    print(f"[parse-srt] Detected encoding: {detected_enc}", file=sys.stderr)

    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')

    # Split thành blocks
    blocks = re.split(r'\n{2,}', content.strip())

    subtitles = []
    skipped = 0

    for block in blocks:
        lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
        if len(lines) < 3:
            skipped += 1
            continue

        # Line 1: ID (số nguyên)
        try:
            sub_id = int(lines[0])
        except ValueError:
            skipped += 1
            continue

        # Line 2: Timecode (hỗ trợ cả , và . làm separator milliseconds)
        timecode_line = lines[1]
        if '-->' not in timecode_line:
            skipped += 1
            continue

        # Normalize timecode: đảm bảo dùng dấu phẩy (,) theo chuẩn SRT
        timecode_line = re.sub(r'(\d{2}:\d{2}:\d{2})\.(\d{3})', r'\1,\2', timecode_line)

        # Lines 3+: Text (join nhiều dòng bằng \n)
        text_lines = lines[2:]

        # Strip HTML tags nếu cần (giữ nguyên để translator xử lý)
        text = '\n'.join(text_lines)

        if not text.strip():
            skipped += 1
            continue

        subtitles.append({
            'id': sub_id,
            'timecode': timecode_line,
            'text': text
        })

    if skipped > 0:
        print(f"[parse-srt] Skipped {skipped} malformed blocks", file=sys.stderr)

    print(f"[parse-srt] Parsed {len(subtitles)} subtitle blocks", file=sys.stderr)
    return subtitles


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python parse-srt.py <file.srt>', file=sys.stderr)
        sys.exit(1)

    # Force UTF-8 stdout
    sys.stdout.reconfigure(encoding='utf-8')

    filepath = sys.argv[1]
    try:
        result = parse_srt(filepath)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except FileNotFoundError:
        print(f'Error: File not found: {filepath}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)
