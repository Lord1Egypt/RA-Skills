#!/usr/bin/env python3
"""
build-srt.py - Ghép subtitles đã dịch thành file SRT chuẩn
Usage: python build-srt.py <original.srt> <translated.json> <output.srt>
"""

import sys
import json
import os
import importlib.util


def parse_timecodes(filepath):
    """Đọc timecodes từ file SRT gốc bằng parse-srt.py"""
    spec = importlib.util.spec_from_file_location(
        "parse_srt",
        os.path.join(os.path.dirname(__file__), "parse-srt.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    subtitles = mod.parse_srt(filepath)
    return {s['id']: s['timecode'] for s in subtitles}


def build_srt(original_path, translated_json_path, output_path):
    timecodes = parse_timecodes(original_path)

    with open(translated_json_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    translations_sorted = sorted(translations, key=lambda x: x['id'])

    srt_lines = []
    for item in translations_sorted:
        sub_id = item['id']
        text = item['text']
        timecode = timecodes.get(sub_id, '')

        if not timecode:
            print(f"[build-srt] Warning: no timecode for id {sub_id}, skipping", file=sys.stderr)
            continue

        srt_lines.append(str(sub_id))
        srt_lines.append(timecode)
        srt_lines.append(text)
        srt_lines.append('')

    srt_content = '\n'.join(srt_lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)

    return len(translations_sorted)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python build-srt.py <original.srt> <translated.json> <output.srt>', file=sys.stderr)
        sys.exit(1)

    sys.stdout.reconfigure(encoding='utf-8')

    original_path = sys.argv[1]
    translated_json_path = sys.argv[2]
    output_path = sys.argv[3]

    try:
        count = build_srt(original_path, translated_json_path, output_path)
        print(f'OK: {count} subtitles written to {output_path}')
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)
