#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SAVE_ROOT = Path.home() / 'clawd' / 'memory' / 'yumfu' / 'saves'
WORLD_DIR = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'worlds'


def normalize_lang(value: str | None) -> str | None:
    if not value:
        return None
    v = str(value).strip().lower()
    if v in {'zh', 'zh-cn', 'zh-hans', 'zh-tw', 'zh-hant', 'cn', 'chinese', '中文'}:
        return 'zh'
    if v in {'en', 'en-us', 'en-gb', 'english'}:
        return 'en'
    return None


def load_world_language(universe: str) -> str | None:
    direct = WORLD_DIR / f'{universe}.json'
    nested = WORLD_DIR / universe / 'world.json'
    path = direct if direct.exists() else nested
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        return normalize_lang(data.get('language'))
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description='Repair YumFu save.language values to match canonical world language when requested')
    parser.add_argument('--user-id')
    parser.add_argument('--universes', nargs='*')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()

    universes = args.universes or [p.name for p in SAVE_ROOT.iterdir() if p.is_dir()]
    report = []

    for universe in universes:
        world_lang = load_world_language(universe)
        if not world_lang:
            continue
        save_dir = SAVE_ROOT / universe
        if not save_dir.exists():
            continue
        candidates = [save_dir / f'user-{args.user_id}.json'] if args.user_id else sorted(save_dir.glob('user-*.json'))
        for path in candidates:
            if not path.exists():
                continue
            try:
                data = json.loads(path.read_text(encoding='utf-8'))
            except Exception as e:
                report.append({'path': str(path), 'status': 'error', 'error': str(e)})
                continue
            current = normalize_lang(data.get('language'))
            if current == world_lang:
                report.append({'path': str(path), 'status': 'ok', 'language': current})
                continue
            entry = {'path': str(path), 'status': 'repair_candidate', 'current': current, 'target': world_lang}
            if args.apply:
                data['language'] = world_lang
                path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
                entry['status'] = 'repaired'
            report.append(entry)

    print(json.dumps({'success': True, 'report': report}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
