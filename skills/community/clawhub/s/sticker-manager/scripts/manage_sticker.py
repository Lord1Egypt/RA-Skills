#!/usr/bin/env python3
"""Manage sticker files."""
import os
import shutil
import sys

from common import get_target_dir, SUPPORTED_EXTS, t, get_lang

TARGET_DIR = get_target_dir()


def resolve_name(name: str) -> str:
    ext = os.path.splitext(name)[1].lower()
    if ext in SUPPORTED_EXTS:
        return name
    for candidate_ext in SUPPORTED_EXTS:
        candidate = name + candidate_ext
        if os.path.exists(os.path.join(TARGET_DIR, candidate)):
            return candidate
    return name + '.jpg'


def delete_sticker(name, lang=None):
    name = resolve_name(name)
    filepath = os.path.join(TARGET_DIR, name)
    if not os.path.exists(filepath):
        return False, t('delete_missing', lang, name=name)
    os.remove(filepath)
    return True, t('delete_success', lang, name=name)


def rename_sticker(old_name, new_name, lang=None):
    old_name = resolve_name(old_name)
    old_ext = os.path.splitext(old_name)[1].lower() or '.jpg'
    if os.path.splitext(new_name)[1].lower() not in SUPPORTED_EXTS:
        new_name += old_ext
    old_path = os.path.join(TARGET_DIR, old_name)
    new_path = os.path.join(TARGET_DIR, new_name)
    if not os.path.exists(old_path):
        return False, t('rename_missing', lang, name=old_name)
    if os.path.exists(new_path):
        return False, t('rename_exists', lang, name=new_name)
    shutil.move(old_path, new_path)
    return True, t('rename_success', lang, old=old_name, new=new_name)


def clean_low_quality(lang=None):
    deleted = []
    for f in os.listdir(TARGET_DIR):
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTS:
            filepath = os.path.join(TARGET_DIR, f)
            size = os.path.getsize(filepath)
            if size < 3072:
                os.remove(filepath)
                deleted.append(f"{f} ({size}B)")
    if deleted:
        return [t('clean_summary', lang, count=len(deleted)), *[f'  - {d}' for d in deleted]]
    return [t('clean_none', lang)]


if __name__ == '__main__':
    lang = get_lang()
    args = [a for a in sys.argv[1:] if not a.startswith('--lang=')]
    for arg in sys.argv[1:]:
        if arg.startswith('--lang='):
            lang = get_lang(arg.split('=', 1)[1])

    if len(args) < 1:
        print('Usage: manage_sticker.py delete <name> | rename <old> <new> | clean')
        raise SystemExit(1)
    action = args[0]
    if action == 'delete' and len(args) >= 2:
        ok, msg = delete_sticker(args[1], lang)
        print(msg)
        raise SystemExit(0 if ok else 1)
    if action == 'rename' and len(args) >= 3:
        ok, msg = rename_sticker(args[1], args[2], lang)
        print(msg)
        raise SystemExit(0 if ok else 1)
    if action == 'clean':
        for line in clean_low_quality(lang):
            print(line)
        raise SystemExit(0)
    print(t('unknown_action', lang))
    raise SystemExit(1)
