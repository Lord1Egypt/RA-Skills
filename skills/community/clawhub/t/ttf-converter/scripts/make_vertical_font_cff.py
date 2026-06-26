"""
CFF builder for the Vertical Font Conversion skill.

This keeps the CFF executable path inside the skill so other agents do not need
separate old experiment scripts.

Current scope:
- rotates CJK body glyphs
- preserves / repositions grouped punctuation with the skill's default logic
- preserves CharString private/globalSubrs metadata to avoid save-time failures

Usage:
    python make_vertical_font_cff.py input.otf output.otf [config.json]
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

SINGLE_CODES = [
    0xFF0C, 0x3002, 0x3001, 0xFF01, 0xFF1F, 0xFF1A, 0xFF1B,
    0x002C, 0x002E, 0x0021, 0x003F, 0x003A, 0x003B,
]
PAIRED_CODES = [
    0x3008, 0x3009, 0x300A, 0x300B,
    0x3010, 0x3011, 0x3014, 0x3015,
    0xFF08, 0xFF09, 0xFF3B, 0xFF3D, 0xFF5B, 0xFF5D,
    0x005B, 0x005D, 0x007B, 0x007D, 0x0028, 0x0029,
]
ELLIPSIS_DASH = [0x2026, 0x2014, 0x2015]
QUOTE_MAP = {0x201C: 0x300C, 0x201D: 0x300D, 0x2018: 0x300E, 0x2019: 0x300F}
ASCII_CODES = list(range(0x30, 0x3A)) + list(range(0x41, 0x5B)) + list(range(0x61, 0x7B))
RIGHT_QUOTES = {0x300C, 0x300E}
LEFT_QUOTES = {0x300D, 0x300F}
DEFAULT_CONFIG = {
    'target_center': [500, 700],
    'single_punct': {'tx': 620, 'ty': 40, 'scale': 0.80, 'question_tx': 560},
    'paired': {'scale': 0.90},
    'corner_quotes': {'scale': 0.90, 'left_bound': 80, 'right_bound': 920, 'target_cy': 700},
    'dash': {'scale': 0.90},
    'ellipsis': {'scale': 0.90},
    'latin_digits': {'scale': 0.92},
}
CONFIG = json.loads(json.dumps(DEFAULT_CONFIG))
TARGET_CENTER = tuple(CONFIG['target_center'])


def deep_update(base, override):
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_update(base[key], value)
        else:
            base[key] = value
    return base


def load_config(path: str | None):
    global CONFIG, TARGET_CENTER
    CONFIG = json.loads(json.dumps(DEFAULT_CONFIG))
    if path:
        with open(path, 'r', encoding='utf-8') as f:
            override = json.load(f)
        deep_update(CONFIG, override)
    TARGET_CENTER = tuple(CONFIG['target_center'])


def compose(A, B):
    a, b, c, d, e, f = A
    g, h, i, j, k, l = B
    return (
        a * g + c * h,
        b * g + d * h,
        a * i + c * j,
        b * i + d * j,
        a * k + c * l + e,
        b * k + d * l + f,
    )


def rotate_about(cx, cy, deg):
    a = math.radians(deg)
    ca = math.cos(a)
    sa = math.sin(a)
    return (ca, sa, -sa, ca, cx - ca * cx + sa * cy, cy - sa * cx - ca * cy)


def translate(dx, dy):
    return (1, 0, 0, 1, dx, dy)


def scale_about(cx, cy, sx, sy):
    return (sx, 0, 0, sy, cx - sx * cx, cy - sy * cy)


def is_cjk(code: int):
    return (
        0x3400 <= code <= 0x4DBF or
        0x4E00 <= code <= 0x9FFF or
        0xF900 <= code <= 0xFAFF or
        0x20000 <= code <= 0x3134F
    )


def charstring_bbox(glyphset, glyph_name: str):
    pen = glyphset[glyph_name]._glyph
    bounds = pen.calcBounds(glyphset)
    if not bounds:
        return (0, 0, 1000, 1000)
    return bounds


def bbox_center(glyphset, glyph_name: str):
    x0, y0, x1, y1 = charstring_bbox(glyphset, glyph_name)
    return (x0 + x1) / 2, (y0 + y1) / 2


def fit_quote_to_side(glyphset, glyph_name: str, side: str, scale: float = 0.90,
                      left_bound: int = 80, right_bound: int = 920, target_cy: int = 700):
    x0, y0, x1, y1 = charstring_bbox(glyphset, glyph_name)
    gcx = (x0 + x1) / 2
    gcy = (y0 + y1) / 2
    scaled_x0 = gcx + scale * (x0 - gcx)
    scaled_x1 = gcx + scale * (x1 - gcx)
    scaled_y0 = gcy + scale * (y0 - gcy)
    scaled_y1 = gcy + scale * (y1 - gcy)
    dy = target_cy - (scaled_y0 + scaled_y1) / 2
    if side == 'right':
        dx = right_bound - scaled_x1
    elif side == 'left':
        dx = left_bound - scaled_x0
    else:
        raise ValueError(side)
    return compose(translate(dx, dy), scale_about(gcx, gcy, scale, scale))


def centered_transform(glyphset, glyph_name: str, target_center=(500, 700), scale=0.90):
    gcx, gcy = bbox_center(glyphset, glyph_name)
    dx = target_center[0] - gcx
    dy = target_center[1] - gcy
    return compose(translate(dx, dy), scale_about(gcx, gcy, scale, scale))


def transform_glyph(dst_font: TTFont, src_font: TTFont, dst_name: str, matrix, src_name: str | None = None):
    src_name = src_name or dst_name
    src_glyphset = src_font.getGlyphSet()
    dst_top = dst_font['CFF '].cff[dst_font['CFF '].cff.fontNames[0]]
    src_top = src_font['CFF '].cff[src_font['CFF '].cff.fontNames[0]]

    width = dst_font['hmtx'].metrics.get(dst_name, (dst_font['head'].unitsPerEm, 0))[0]
    pen = T2CharStringPen(width, src_glyphset)
    tpen = TransformPen(pen, matrix)
    src_glyphset[src_name].draw(tpen)
    cs = pen.getCharString()

    old_cs = src_top.CharStrings[src_name]
    cs.private = getattr(old_cs, 'private', None)
    cs.globalSubrs = getattr(old_cs, 'globalSubrs', None)
    dst_top.CharStrings[dst_name] = cs

    if dst_name in dst_font['hmtx'].metrics and src_name in src_font['hmtx'].metrics:
        dst_font['hmtx'].metrics[dst_name] = src_font['hmtx'].metrics[src_name]
    if 'vmtx' in dst_font and 'vmtx' in src_font and dst_name in dst_font['vmtx'].metrics and src_name in src_font['vmtx'].metrics:
        dst_font['vmtx'].metrics[dst_name] = src_font['vmtx'].metrics[src_name]


def preprocess_specials_horizontal(dst_font: TTFont, src_font: TTFont):
    cmap = dst_font.getBestCmap()
    srcmap = src_font.getBestCmap()
    src_glyphset = src_font.getGlyphSet()
    upem = dst_font['head'].unitsPerEm
    cx = upem / 2
    cy = upem / 2 - dst_font['hhea'].descent

    for code in SINGLE_CODES:
        dst_name = cmap.get(code)
        src_name = srcmap.get(code)
        if not (dst_name and src_name):
            continue
        gcx, gcy = bbox_center(src_glyphset, src_name)
        sp = CONFIG['single_punct']
        tx, ty, sc = sp['tx'], sp['ty'], sp['scale']
        if code in (0xFF1F, 0x003F):
            tx = sp.get('question_tx', tx)
        M = compose(
            rotate_about(cx, cy, 90),
            compose(translate(tx, ty), scale_about(gcx, gcy, sc, sc)),
        )
        transform_glyph(dst_font, src_font, dst_name, M, src_name=src_name)

    for code in PAIRED_CODES:
        dst_name = cmap.get(code)
        src_name = srcmap.get(code)
        if not (dst_name and src_name):
            continue
        M = centered_transform(src_glyphset, src_name, target_center=TARGET_CENTER, scale=CONFIG['paired']['scale'])
        transform_glyph(dst_font, src_font, dst_name, M, src_name=src_name)

    for code in RIGHT_QUOTES | LEFT_QUOTES:
        dst_name = cmap.get(code)
        src_name = srcmap.get(code)
        if not (dst_name and src_name):
            continue
        side = 'right' if code in RIGHT_QUOTES else 'left'
        cq = CONFIG['corner_quotes']
        M = fit_quote_to_side(src_glyphset, src_name, side=side, scale=cq['scale'], left_bound=cq['left_bound'], right_bound=cq['right_bound'], target_cy=cq['target_cy'])
        transform_glyph(dst_font, src_font, dst_name, M, src_name=src_name)

    for dst_code, src_code in QUOTE_MAP.items():
        dst_name = cmap.get(dst_code)
        src_name = srcmap.get(src_code)
        if not (dst_name and src_name):
            continue
        side = 'right' if src_code in RIGHT_QUOTES else 'left'
        cq = CONFIG['corner_quotes']
        M = fit_quote_to_side(src_glyphset, src_name, side=side, scale=cq['scale'], left_bound=cq['left_bound'], right_bound=cq['right_bound'], target_cy=cq['target_cy'])
        transform_glyph(dst_font, src_font, dst_name, M, src_name=src_name)

    for code in ELLIPSIS_DASH:
        dst_name = cmap.get(code)
        src_name = srcmap.get(code)
        if not (dst_name and src_name):
            continue
        if code in (0x2014, 0x2015):
            M = centered_transform(src_glyphset, src_name, target_center=TARGET_CENTER, scale=CONFIG['dash']['scale'])
        else:
            gcx, gcy = bbox_center(src_glyphset, src_name)
            scale = CONFIG['ellipsis']['scale']
            dx = TARGET_CENTER[0] - gcx
            dy = TARGET_CENTER[1] - gcy
            M = compose(translate(dx, dy), scale_about(gcx, gcy, scale, scale))
        transform_glyph(dst_font, src_font, dst_name, M, src_name=src_name)

    for code in ASCII_CODES:
        dst_name = cmap.get(code)
        src_name = srcmap.get(code)
        if not (dst_name and src_name):
            continue
        gcx, gcy = bbox_center(src_glyphset, src_name)
        dx = TARGET_CENTER[0] - gcx
        dy = TARGET_CENTER[1] - gcy
        sc = CONFIG['latin_digits']['scale']
        M = compose(translate(dx, dy), scale_about(gcx, gcy, sc, sc))
        transform_glyph(dst_font, src_font, dst_name, M, src_name=src_name)


def rotate_cjk_body(dst_font: TTFont, src_font: TTFont):
    cmap = dst_font.getBestCmap()
    src_glyphset = src_font.getGlyphSet()
    upem = dst_font['head'].unitsPerEm
    cx = upem / 2
    cy = upem / 2 - dst_font['hhea'].descent
    rot_cjk = rotate_about(cx, cy, 90)
    done = set()

    for code, glyph_name in cmap.items():
        if glyph_name in done:
            continue
        if is_cjk(code) and glyph_name in src_glyphset:
            transform_glyph(dst_font, src_font, glyph_name, rot_cjk, src_name=glyph_name)
            done.add(glyph_name)


def rename_font(font: TTFont, suffix: str):
    for rec in font['name'].names:
        try:
            s = rec.toUnicode()
            enc = rec.getEncoding()
        except Exception:
            continue
        if suffix not in s:
            rec.string = (s + suffix).encode(enc, errors='ignore')


def main(inp: str, outp: str, config_path: str | None = None):
    load_config(config_path)
    font = TTFont(inp)
    src = TTFont(inp)
    if 'CFF ' not in font:
        raise SystemExit('input is not a CFF font')

    preprocess_specials_horizontal(font, src)
    rotate_cjk_body(font, src)
    rename_font(font, '-vertical-font-conversion-cff')

    Path(outp).parent.mkdir(parents=True, exist_ok=True)
    font.save(outp)
    print(outp)


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        print('usage: python make_vertical_font_cff.py input.otf output.otf [config.json]')
        raise SystemExit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None)
