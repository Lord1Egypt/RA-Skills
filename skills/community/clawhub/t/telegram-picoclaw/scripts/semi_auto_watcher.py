#!/usr/bin/env python3
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

# Direct imports to avoid subprocesses
from transcribe_audio import transcribe_audio
from cleanup_old_files import main as cleanup_main

BASE = Path('/root/.picoclaw/workspace/state/telegram-native-audio')
PENDING = BASE / 'pending'
DONE = BASE / 'done'
TMP = BASE / 'tmp'
STATE = BASE / 'semi-auto-state.json'
MEDIA_DIR = Path('/tmp/picoclaw_media')
SUPPORTED = {'.ogg', '.oga', '.mp3', '.wav', '.m4a', '.mp4', '.opus'}
CHAT_ID = os.environ.get('PICOLAW_CHAT_ID') or os.environ.get('TELEGRAM_CHAT_ID') or ''
POLL = 2.0
CLEANUP_INTERVAL = 24 * 60 * 60


def ensure():
    for p in [PENDING, DONE, TMP]:
        p.mkdir(parents=True, exist_ok=True)
    if not STATE.exists():
        STATE.write_text(json.dumps({'processed': {}, 'last_cleanup_at': 0}, ensure_ascii=False, indent=2))


def load_state():
    try:
        state = json.loads(STATE.read_text())
        state.setdefault('processed', {})
        state.setdefault('last_cleanup_at', 0)
        return state
    except Exception:
        return {'processed': {}, 'last_cleanup_at': 0}


def save_state(state):
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def maybe_run_cleanup(state: dict):
    now = int(time.time())
    last_cleanup = int(state.get('last_cleanup_at', 0) or 0)
    if now - last_cleanup < CLEANUP_INTERVAL:
        return state
    try:
        cleanup_main()
        state['last_cleanup_at'] = now
        save_state(state)
        print(json.dumps({'status': 'cleanup_ok', 'ran_at': now}, ensure_ascii=False), flush=True)
    except Exception as e:
        print(json.dumps({'status': 'cleanup_error', 'error': str(e)}, ensure_ascii=False), file=sys.stderr, flush=True)
    return state


def stable(path: Path) -> bool:
    try:
        a = path.stat().st_size
        time.sleep(0.8)
        b = path.stat().st_size
        return a > 0 and a == b
    except FileNotFoundError:
        return False


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def transcribe(path: Path) -> str:
    api_key = os.environ.get('GROQ_API_KEY', '')
    if not api_key:
        raise RuntimeError('GROQ_API_KEY não configurada')
    try:
        return transcribe_audio(str(path), api_key)
    except Exception as e:
        raise RuntimeError(f'falha na transcrição: {e}')


def process(path: Path, state: dict):
    if path.suffix.lower() not in SUPPORTED:
        return
    if not stable(path):
        return
    digest = file_hash(path)
    if digest in state.get('processed', {}):
        return

    ts = int(time.time())
    transcription = transcribe(path)
    stem = f'{path.stem}-{ts}'
    archived = DONE / f'{stem}{path.suffix.lower()}'
    shutil.copy2(path, archived)

    meta = {
        'hash': digest,
        'chat_id': CHAT_ID,
        'source_file': str(path),
        'archived_audio': str(archived),
        'transcription': transcription,
        'created_at': ts,
        'status': 'pending_reply'
    }
    meta_path = PENDING / f'{stem}.json'
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    state.setdefault('processed', {})[digest] = {'meta_file': str(meta_path), 'created_at': ts}
    save_state(state)
    print(json.dumps({'status': 'pending_reply', 'meta_file': str(meta_path), 'transcription': transcription}, ensure_ascii=False), flush=True)


def main():
    ensure()
    print('[semi-auto-watcher] watching /tmp/picoclaw_media', flush=True)
    while True:
        state = load_state()
        state = maybe_run_cleanup(state)
        for p in sorted(MEDIA_DIR.glob('*')):
            if not p.is_file():
                continue
            try:
                process(p, state)
            except Exception as e:
                print(json.dumps({'status': 'error', 'file': str(p), 'error': str(e)}, ensure_ascii=False), file=sys.stderr, flush=True)
        time.sleep(POLL)


if __name__ == '__main__':
    main()
