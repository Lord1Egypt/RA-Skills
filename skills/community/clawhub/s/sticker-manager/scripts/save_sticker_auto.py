#!/usr/bin/env python3
"""Save inbound or chat-history media with quality checks."""
import json
import os
import shutil
import sys
from datetime import datetime

from common import get_target_dir, get_inbound_dir, SUPPORTED_EXTS, t, get_lang, resolve_media_source

TARGET_DIR = get_target_dir()
INBOUND_DIR = get_inbound_dir()
QUALITY_LOG = os.path.join(TARGET_DIR, '.quality_log.json')
SUPPORTED_EXTS = list(SUPPORTED_EXTS)
USAGE = """Usage:
  save_sticker_auto.py [--lang=en|zh] [--force]
  save_sticker_auto.py [--lang=en|zh] [--force] [--source=FILE | --history-index=N] [suggested_name]
"""


def get_selected_image(source=None, history_index=None):
    filepath = resolve_media_source(source=source, history_index=history_index, inbound_dir=INBOUND_DIR)
    if not filepath:
        return None
    return filepath, os.path.getmtime(filepath), os.path.getsize(filepath)


def check_quality(filepath, lang=None):
    size = os.path.getsize(filepath)
    if size < 2048:
        return False, t('quality_reason_too_small', lang, size=size), 20
    if size < 5120:
        return False, t('quality_reason_small', lang, size_kb=size // 1024), 40
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in SUPPORTED_EXTS:
        return False, t('unsupported_format', lang, ext=ext), 0
    if size >= 51200:
        return True, f'high ({size // 1024}KB)', 90
    if size >= 20480:
        return True, f'good ({size // 1024}KB)', 75
    if size >= 10240:
        return True, f'medium ({size // 1024}KB)', 60
    return True, f'usable ({size // 1024}KB)', 50


def log_quality_check(filepath, quality_score, reason, saved=False):
    log = {}
    if os.path.exists(QUALITY_LOG):
        with open(QUALITY_LOG, 'r', encoding='utf-8') as f:
            log = json.load(f)
    filename = os.path.basename(filepath)
    log[filename] = {
        'timestamp': datetime.now().isoformat(),
        'quality_score': quality_score,
        'reason': reason,
        'saved': saved,
    }
    with open(QUALITY_LOG, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def save_sticker_auto(suggested_name=None, force_save=False, lang=None, source=None, history_index=None):
    os.makedirs(TARGET_DIR, exist_ok=True)
    latest = get_selected_image(source=source, history_index=history_index)
    if not latest:
        msg_key = 'history_empty' if source or history_index is not None else 'save_no_media'
        return False, t(msg_key, lang), None
    filepath, _mtime, size = latest
    is_acceptable, reason, quality_score = check_quality(filepath, lang)
    quality_info = {'score': quality_score, 'reason': reason, 'size': size}
    if not is_acceptable and not force_save:
        log_quality_check(filepath, quality_score, reason, saved=False)
        return False, t('quality_reject', lang, reason=reason), quality_info
    if not suggested_name:
        return True, '__NEED_ANALYSIS__', quality_info
    clean_name = suggested_name.replace('/', '_').replace('\\', '_').replace(' ', '_')
    source_ext = os.path.splitext(filepath)[1].lower() or '.jpg'
    if os.path.splitext(clean_name)[1].lower() not in SUPPORTED_EXTS:
        clean_name += source_ext
    target_path = os.path.join(TARGET_DIR, clean_name)
    if os.path.exists(target_path):
        base, ext = os.path.splitext(clean_name)
        counter = 1
        while os.path.exists(target_path):
            target_path = os.path.join(TARGET_DIR, f'{base}_{counter}{ext}')
            counter += 1
        clean_name = os.path.basename(target_path)
    shutil.copy2(filepath, target_path)
    final_size = os.path.getsize(target_path)
    log_quality_check(filepath, quality_score, reason, saved=True)
    badge = '🌟' if quality_score >= 75 else '✅' if quality_score >= 50 else '⚠️'
    return True, t('save_auto_success', lang, badge=badge, name=clean_name, size_kb=final_size // 1024, score=quality_score), quality_info


if __name__ == '__main__':
    lang = get_lang()
    args = sys.argv[1:]
    if any(arg in ('-h', '--help') for arg in args):
        print(USAGE)
        raise SystemExit(0)
    force_save = '--force' in args
    args = [a for a in args if a != '--force']
    source = None
    history_index = None
    cleaned = []
    for arg in list(args):
        if arg.startswith('--lang='):
            lang = get_lang(arg.split('=', 1)[1])
        elif arg.startswith('--source='):
            source = arg.split('=', 1)[1]
        elif arg.startswith('--history-index='):
            history_index = int(arg.split('=', 1)[1])
        else:
            cleaned.append(arg)
    suggested_name = cleaned[0] if cleaned else None
    success, msg, quality_info = save_sticker_auto(suggested_name, force_save, lang, source=source, history_index=history_index)
    if msg == '__NEED_ANALYSIS__':
        selected = get_selected_image(source=source, history_index=history_index)
        print(f"__ANALYZE__:{selected[0]}")
        print(f"__QUALITY__:{quality_info['score']}")
        raise SystemExit(2)
    print(msg)
    raise SystemExit(0 if success else 1)
