"""
One-shot local pipeline for the Vertical Font Conversion skill.

Default behavior:
1. detect glyf vs CFF font
2. generate original preview
3. build vertical font
4. generate vertical preview
5. generate reader test TXT

Usage examples:
    python run_full_pipeline.py input.ttf outdir
    python run_full_pipeline.py input.otf outdir
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

SCRIPT_DIR = Path(__file__).resolve().parent


def run(cmd):
    print('running:', ' '.join(str(x) for x in cmd))
    result = subprocess.run([str(x) for x in cmd], check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def detect_kind(font_path: str) -> str:
    font = TTFont(font_path)
    if 'CFF ' in font:
        return 'cff'
    if 'glyf' in font:
        return 'glyf'
    return 'unknown'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_font')
    parser.add_argument('output_dir')
    args = parser.parse_args()

    input_font = Path(args.input_font).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    stem = input_font.stem
    suffix = input_font.suffix.lower()
    kind = detect_kind(str(input_font))

    horizontal_preview = output_dir / f'{stem}-horizontal-preview.png'
    vertical_font = output_dir / f'{stem}-vertical{suffix}'
    vertical_preview = output_dir / f'{stem}-vertical-preview.png'
    reader_txt = output_dir / f'{stem}-reader-test.txt'

    run([sys.executable, SCRIPT_DIR / 'render_original_preview.py', input_font, horizontal_preview])

    if kind == 'cff':
        run([sys.executable, SCRIPT_DIR / 'make_vertical_font_cff.py', input_font, vertical_font])
    elif kind == 'glyf':
        run([sys.executable, SCRIPT_DIR / 'make_vertical_font.py', input_font, vertical_font])
    else:
        raise SystemExit('unsupported font kind: neither glyf nor CFF')

    run([sys.executable, SCRIPT_DIR / 'render_vertical_preview.py', vertical_font, vertical_preview])
    run([sys.executable, SCRIPT_DIR / 'generate_reader_test_txt.py', reader_txt])

    print('artifacts:')
    print(horizontal_preview)
    print(vertical_font)
    print(vertical_preview)
    print(reader_txt)


if __name__ == '__main__':
    main()
