#!/usr/bin/env python3
"""
Profanity removal script - replaces with ****
"""

import json
import re
import sys
from pathlib import Path

def load_profanity_patterns():
    """Load patterns from data/profanity-patterns.json"""
    data_path = Path(__file__).parent.parent / "data" / "profanity-patterns.json"
    if data_path.exists():
        with open(data_path, "r", encoding="utf-8") as f:
            entries = json.load(f)
        return [(e["pattern"], e["replacement"]) for e in entries]
    # Fallback if data file missing (\b avoids matching "ass" inside "assistant", etc.)
    return [(r'\b(fuck|shit|damn|bitch|ass)\b', '****')]

PROFANITY_PATTERNS = load_profanity_patterns()

def clean_text(text: str) -> tuple[str, bool]:
    """
    Remove profanity from text
    Returns: (cleaned_text, was_modified)
    """
    if not text:
        return text, False

    original = text
    modified = False

    for pattern, replacement in PROFANITY_PATTERNS:
        if re.search(pattern, text):
            # Replace standalone occurrences with XX
            text = re.sub(pattern, replacement, text)
            modified = True

    return text, modified

def clean_value(obj):
    """
    Recursively remove profanity from JSON values
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
            # Process value
            cleaned, was_modified = clean_value(obj[key])
            if was_modified:
                obj[key] = cleaned
                modified = True
            # Process key
            if isinstance(key, str):
                cleaned_key, key_modified = clean_text(key)
                if key_modified:
                    keys_to_rename.append((key, cleaned_key))
        for old_key, new_key in keys_to_rename:
            if new_key in obj and new_key != old_key:
                continue  # skip if cleaned key already exists
            obj[new_key] = obj.pop(old_key)
            modified = True
        return obj, modified
    return obj, False


def process_jsonl_file(file_path: Path) -> int:
    """
    Process a JSONL file
    Returns: number of modified lines
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

    # Create backup (stored in ~/.claude/projects/.bak/ central directory)
    if modified_count > 0:
        bak_dir = Path.home() / '.claude' / 'projects' / '.bak'
        bak_dir.mkdir(exist_ok=True)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stem = file_path.stem
        backup_path = bak_dir / f"{stem}.{timestamp}{file_path.suffix}"
        file_path.rename(backup_path)

        # Save modified content
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
