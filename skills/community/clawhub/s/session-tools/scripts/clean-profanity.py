#!/usr/bin/env python3
"""
욕설 제거 스크립트 - XX 처리
"""

import json
import re
import sys
from pathlib import Path

# 욕설 패턴 (접두사 포함: 개병신→XX, 개새끼→XX)
PROFANITY_PATTERNS = [
    (r'개?(씨발)?(병신)?(새끼)', 'XX'),
    (r'존나', 'XX'),
    (r'좆', 'XX'),
    (r'개?지랄', 'XX'),
]

def clean_text(text: str) -> tuple[str, bool]:
    """
    텍스트에서 욕설 제거
    Returns: (cleaned_text, was_modified)
    """
    if not text:
        return text, False

    original = text
    modified = False

    for pattern, replacement in PROFANITY_PATTERNS:
        if re.search(pattern, text):
            # 단독으로 사용된 경우 XX 처리
            text = re.sub(pattern, replacement, text)
            modified = True

    return text, modified

def clean_value(obj):
    """
    재귀적으로 JSON 값에서 욕설 제거
    Returns: (cleaned_obj, was_modified)
    """
    if isinstance(obj, str):
        return clean_text(obj)
    elif isinstance(obj, list):
        modified = False
        for i, item in enumerate(obj):
            cleaned, was_modified = clean_value(item)
            if was_modified:
                obj[i] = cleaned
                modified = True
        return obj, modified
    elif isinstance(obj, dict):
        modified = False
        keys_to_rename = []
        for key in obj:
            # 값 처리
            cleaned, was_modified = clean_value(obj[key])
            if was_modified:
                obj[key] = cleaned
                modified = True
            # 키 처리
            if isinstance(key, str):
                cleaned_key, key_modified = clean_text(key)
                if key_modified:
                    keys_to_rename.append((key, cleaned_key))
        for old_key, new_key in keys_to_rename:
            obj[new_key] = obj.pop(old_key)
            modified = True
        return obj, modified
    return obj, False


def process_jsonl_file(file_path: Path) -> int:
    """
    JSONL 파일 처리
    Returns: 수정된 줄 수
    """
    lines = []
    modified_count = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    lines.append(line)
                    continue

                try:
                    data = json.loads(line)
                    _, line_modified = clean_value(data)

                    if line_modified:
                        modified_count += 1
                        lines.append(json.dumps(data, ensure_ascii=False) + '\n')
                    else:
                        lines.append(line)

                except json.JSONDecodeError:
                    lines.append(line)

    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return 0

    # 백업 생성 (~/.claude/projects/.bak/ 중앙 디렉토리에 저장)
    if modified_count > 0:
        bak_dir = Path.home() / '.claude' / 'projects' / '.bak'
        bak_dir.mkdir(exist_ok=True)
        backup_path = bak_dir / file_path.name
        if backup_path.exists():
            # 충돌 시 .orig 접미사
            stem = file_path.stem
            backup_path = bak_dir / f"{stem}.orig{file_path.suffix}"
        file_path.rename(backup_path)

        # 수정된 내용 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print(f"✓ {file_path.name}: {modified_count} lines modified")

    return modified_count

def main():
    if len(sys.argv) < 2:
        print("Usage: clean-profanity.py <file1> [file2] ...", file=sys.stderr)
        sys.exit(1)

    total_files = 0
    total_lines = 0

    for file_arg in sys.argv[1:]:
        file_path = Path(file_arg)
        if not file_path.exists():
            print(f"File not found: {file_path}", file=sys.stderr)
            continue

        count = process_jsonl_file(file_path)
        if count > 0:
            total_files += 1
            total_lines += count

    print(f"\nTotal: {total_files} files, {total_lines} lines modified")

if __name__ == '__main__':
    main()
