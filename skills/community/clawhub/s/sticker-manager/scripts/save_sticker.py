#!/usr/bin/env python3
"""Save inbound or chat-history media into the sticker library."""
import os
import shutil
from datetime import datetime
import sys

from common import get_target_dir, get_inbound_dir, SUPPORTED_EXTS, t, get_lang, resolve_media_source, list_media_files

TARGET_DIR = get_target_dir()
INBOUND_DIR = get_inbound_dir()
USAGE = """Usage:
  save_sticker.py [--lang=en|zh] [--list-history]
  save_sticker.py [--lang=en|zh] [--source=FILE | --history-index=N] [name]
"""


def save_media_to_library(source_path, name=None, lang=None):
    os.makedirs(TARGET_DIR, exist_ok=True)
    latest_ext = os.path.splitext(source_path)[1].lower() or '.jpg'
    if name:
        name = name.replace('/', '_').replace('\\', '_')
        if os.path.splitext(name)[1].lower() not in SUPPORTED_EXTS:
            name += latest_ext
    else:
        name = f"sticker_{int(datetime.now().timestamp())}{latest_ext}"
    target_path = os.path.join(TARGET_DIR, name)
    if os.path.exists(target_path):
        return None, t('save_exists', lang, name=name)
    shutil.copy2(source_path, target_path)
    size = os.path.getsize(target_path)
    return target_path, t('save_success', lang, name=name, size_kb=size // 1024)


def save_latest_sticker(name=None, lang=None, source=None, history_index=None):
    if not os.path.exists(INBOUND_DIR):
        return None, t('save_missing_inbound', lang)
    chosen_source = resolve_media_source(source=source, history_index=history_index, inbound_dir=INBOUND_DIR)
    if not chosen_source:
        msg_key = 'history_empty' if source or history_index is not None else 'save_no_media'
        return None, t(msg_key, lang)
    return save_media_to_library(chosen_source, name, lang)


def list_recent_media(lang=None):
    media_files = list_media_files(INBOUND_DIR)
    if not media_files:
        return [t('history_empty', lang)]
    lines = [t('history_list_title', lang)]
    for idx, (filepath, _mtime, size) in enumerate(media_files[:10], 1):
        lines.append(f"{idx}. {os.path.basename(filepath)} ({size // 1024}KB)")
    return lines


if __name__ == '__main__':
    lang = get_lang()
    args = []
    source = None
    history_index = None
    list_mode = False
    for arg in sys.argv[1:]:
        if arg in ('-h', '--help'):
            print(USAGE)
            raise SystemExit(0)
        if arg.startswith('--lang='):
            lang = get_lang(arg.split('=', 1)[1])
        elif arg.startswith('--source='):
            source = arg.split('=', 1)[1]
        elif arg.startswith('--history-index='):
            history_index = int(arg.split('=', 1)[1])
        elif arg == '--list-history':
            list_mode = True
        else:
            args.append(arg)
    if list_mode:
        for line in list_recent_media(lang):
            print(line)
        raise SystemExit(0)
    name = args[0] if args else None
    path, msg = save_latest_sticker(name, lang, source=source, history_index=history_index)
    print(msg)
    raise SystemExit(0 if path else 1)
