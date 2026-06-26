#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path('/root/.openclaw/skills/pywebtop-skill/webtop_homework_fetcher.py')


def main():
    proc = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, timeout=180)
    text = (proc.stdout or '').strip()
    err = (proc.stderr or '').strip()
    out = {
        'success': proc.returncode == 0 and bool(text),
        'source': 'webtop',
        'raw_text': text,
        'error': err or None,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
