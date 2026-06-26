#!/usr/bin/env python3
import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

MEDIA_DIR = Path('/tmp/picoclaw_media')
BASE = Path('/root/.picoclaw/workspace/state/telegram-native-audio')
STATE_FILE = BASE / 'media-watcher-state.json'
INBOX = BASE / 'inbox'
PROCESSED = BASE / 'processed'
RUNNER = Path('/root/.picoclaw/workspace/skills/telegram-native-audio/scripts/runner.py')
CHAT_ID = os.environ.get('PICOLAW_CHAT_ID') or os.environ.get('TELEGRAM_CHAT_ID') or ''
SUPPORTED = {'.ogg', '.oga', '.mp3', '.wav', '.m4a', '.mp4', '.opus'}
POLL = 2.0


def ensure():
    BASE.mkdir(parents=True, exist_ok=True)
    INBOX.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        STATE_FILE.write_text(json.dumps({'processed': {}}, ensure_ascii=False, indent=2))


def load_state():
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {'processed': {}}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def stable(path: Path) -> bool:
    try:
        s1 = path.stat().st_size
        time.sleep(0.8)
        s2 = path.stat().st_size
        return s1 > 0 and s1 == s2
    except FileNotFoundError:
        return False


def process(path: Path):
    result = subprocess.run(
        ['python3', str(RUNNER), 'process', str(path), '--chat-id', CHAT_ID],
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    return result.returncode, result.stdout, result.stderr


def parse_sections(text: str):
    markers = ['=== TRANSCRIÇÃO ===', '=== RESPOSTA ===', '=== AUDIO_FILE ===', '=== SEND_REQUESTED ===', '=== CHAT_ID ===']
    data = {}
    current = None
    lines = []
    for line in text.splitlines():
        if line in markers:
            if current is not None:
                data[current] = '\n'.join(lines).strip()
            current = line
            lines = []
        else:
            lines.append(line)
    if current is not None:
        data[current] = '\n'.join(lines).strip()
    return {
        'transcription': data.get('=== TRANSCRIÇÃO ===', ''),
        'reply': data.get('=== RESPOSTA ===', ''),
        'audio_file': data.get('=== AUDIO_FILE ===', ''),
    }


def main():
    ensure()
    print('[telegram-media-watcher] watching /tmp/picoclaw_media', flush=True)
    while True:
        state = load_state()
        for path in sorted(MEDIA_DIR.glob('*')):
            if not path.is_file():
                continue
            if path.suffix.lower() not in SUPPORTED:
                continue
            if not stable(path):
                continue
            digest = file_hash(path)
            if digest in state.get('processed', {}):
                continue
            code, out, err = process(path)
            meta = {'file': str(path), 'hash': digest, 'time': int(time.time()), 'code': code, 'stdout': out, 'stderr': err}
            if code == 0:
                parsed = parse_sections(out)
                meta.update(parsed)
            state.setdefault('processed', {})[digest] = meta
            save_state(state)
            print(json.dumps(meta, ensure_ascii=False), flush=True)
        time.sleep(POLL)


if __name__ == '__main__':
    main()
