#!/usr/bin/env python3
"""Sticker lookup and inventory listing."""
import os
import glob
import sys

from common import get_target_dir, SUPPORTED_GLOBS, t, get_lang

TARGET_DIR = get_target_dir()
SUPPORTED_EXTS = SUPPORTED_GLOBS


def list_all_stickers():
    all_stickers = []
    for pattern in SUPPORTED_EXTS:
        all_stickers.extend(glob.glob(os.path.join(TARGET_DIR, pattern)))
    return sorted(set(all_stickers))


def find_sticker(keyword, lang=None):
    if not os.path.exists(TARGET_DIR):
        return None, t("library_not_found", lang, path=TARGET_DIR)

    all_stickers = list_all_stickers()
    if not all_stickers:
        return None, t("library_empty", lang)

    keyword_lower = keyword.lower()
    for sticker in all_stickers:
        basename = os.path.basename(sticker)
        name_without_ext = os.path.splitext(basename)[0].lower()
        if keyword_lower == name_without_ext:
            return sticker, basename
        if keyword_lower in name_without_ext:
            return sticker, basename

    for sticker in all_stickers:
        basename = os.path.basename(sticker).lower()
        if keyword_lower in basename:
            return sticker, os.path.basename(sticker)

    available = ', '.join(os.path.basename(s) for s in all_stickers[:10])
    return None, t("sticker_not_found", lang, keyword=keyword, available=available)


def list_stickers():
    if not os.path.exists(TARGET_DIR):
        return []
    return sorted(os.path.basename(s) for s in list_all_stickers())


if __name__ == "__main__":
    lang = get_lang()
    args = [a for a in sys.argv[1:] if not a.startswith('--lang=')]
    for arg in sys.argv[1:]:
        if arg.startswith('--lang='):
            lang = get_lang(arg.split('=', 1)[1])

    if len(args) < 1:
        stickers = list_stickers()
        if stickers:
            print(t("inventory_title", lang))
            for i, s in enumerate(stickers, 1):
                print(f"{i}. {s}")
        else:
            print(t("library_empty", lang))
        raise SystemExit(0)

    keyword = args[0]
    path, result = find_sticker(keyword, lang)
    if path:
        print(path)
        raise SystemExit(0)
    print(result)
    raise SystemExit(1)
