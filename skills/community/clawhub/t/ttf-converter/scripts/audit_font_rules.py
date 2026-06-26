from __future__ import annotations

import json
import sys
from fontTools.ttLib import TTFont

SAMPLES = {
    'single_punct': ['，', '。', '！', '？', ',', '.', '!', '?'],
    'paired': ['《', '》', '〈', '〉', '（', '）', '【', '】'],
    'corner_quotes': ['「', '」', '『', '』'],
    'curly_quotes': ['“', '”', '‘', '’'],
    'dash_ellipsis': ['—', '…'],
    'latin_digits': ['A', 'a', '1', '9'],
}


def ensure_bounds(font: TTFont, glyph_name: str):
    g = font['glyf'][glyph_name]
    if not hasattr(g, 'xMin'):
        g.recalcBounds(font['glyf'])
    return g


def glyph_info(font: TTFont, ch: str):
    cmap = font.getBestCmap()
    code = ord(ch)
    glyph_name = cmap.get(code)
    if not glyph_name:
        return {'char': ch, 'codepoint': hex(code), 'present': False}
    g = ensure_bounds(font, glyph_name)
    return {
        'char': ch,
        'codepoint': hex(code),
        'present': True,
        'glyph': glyph_name,
        'bbox': [g.xMin, g.yMin, g.xMax, g.yMax],
        'center': [(g.xMin + g.xMax) / 2, (g.yMin + g.yMax) / 2],
    }


def main(font_path: str):
    font = TTFont(font_path)
    if 'glyf' not in font:
        raise SystemExit('audit_font_rules.py currently expects a glyf-based TTF')

    report = {
        'font': font_path,
        'groups': {
            name: [glyph_info(font, ch) for ch in chars]
            for name, chars in SAMPLES.items()
        }
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python audit_font_rules.py font.ttf')
        raise SystemExit(1)
    main(sys.argv[1])
