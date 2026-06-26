#!/usr/bin/env python3
from __future__ import annotations
import json
import os
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = Path(os.environ.get('OPENCLAW_WORKSPACE', SKILL_DIR.parent.parent)).resolve()
DATA_DIR = Path(os.environ.get('TWITTER_WATCH_REPLY_DATA_DIR', WORKSPACE_ROOT / 'data' / 'twitter-watch-reply')).resolve()
CONFIG_PATH = DATA_DIR / 'config.json'
STATE_PATH = DATA_DIR / 'state.json'
EXAMPLE_PATH = SKILL_DIR / 'references' / 'config-example.json'


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


def save_json(path: Path, data) -> None:
    ensure_data_dir()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
