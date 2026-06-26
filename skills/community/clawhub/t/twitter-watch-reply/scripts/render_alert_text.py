#!/usr/bin/env python3
from __future__ import annotations
import json
from common import CONFIG_PATH, load_json
from render_alert import build_candidates


def main():
    cfg = load_json(CONFIG_PATH, {})
    import subprocess
    raw = subprocess.check_output(['python3', 'skills/twitter-watch-reply/scripts/render_alert.py'], text=True)
    data = json.loads(raw)
    alert = data.get('alert')
    if not alert:
        print('NO_ALERT')
        return
    lines = [
        '发现新推：',
        f"- 作者：@{alert.get('author','')}",
        f"- 链接：{alert.get('url','')}",
        f"- 内容：{(alert.get('text','') or '').strip()}",
        '',
        '候选回复：',
    ]
    for i, c in enumerate(alert.get('candidates', [])[: int(cfg.get('candidateCount', 3) or 3)], 1):
        lines.append(f'{i}. {c}')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
