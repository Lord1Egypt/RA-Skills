#!/usr/bin/env python3
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

BASE = Path('/root/.picoclaw/workspace/state/telegram-native-audio')
INBOX = BASE / 'inbox'
OUTBOX = BASE / 'outbox'
PROCESSED = BASE / 'processed'
TMP = BASE / 'tmp'
STATE_FILE = BASE / 'state.json'
RUNNER = Path('/root/.picoclaw/workspace/skills/telegram-native-audio/scripts/runner.py')
SUPPORTED = {'.ogg', '.oga', '.mp3', '.wav', '.m4a', '.mp4', '.opus'}
POLL_SECONDS = float(os.environ.get('TELEGRAM_NATIVE_AUDIO_POLL', '2'))


def ensure():
    for p in [INBOX, OUTBOX, PROCESSED, TMP]:
        p.mkdir(parents=True, exist_ok=True)
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
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def stable(path: Path) -> bool:
    try:
        size1 = path.stat().st_size
        time.sleep(0.8)
        size2 = path.stat().st_size
        return size1 > 0 and size1 == size2
    except FileNotFoundError:
        return False


def run_one(path: Path):
    result = subprocess.run(
        ['python3', str(RUNNER), 'process', str(path)],
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or 'erro desconhecido')
    return result.stdout


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


def process_file(path: Path, state: dict):
    if path.suffix.lower() not in SUPPORTED:
        return
    if not stable(path):
        return
    digest = file_hash(path)
    if digest in state.get('processed', {}):
        return

    stdout = run_one(path)
    parsed = parse_sections(stdout)
    ts = int(time.time())
    stem = path.stem
    out_audio_src = Path(parsed['audio_file'])
    out_audio_dst = OUTBOX / f'{stem}-{ts}.mp3'
    if out_audio_src.exists():
        shutil.copy2(out_audio_src, out_audio_dst)

    meta = {
        'input_file': str(path),
        'hash': digest,
        'processed_at': ts,
        'transcription': parsed['transcription'],
        'reply': parsed['reply'],
        'output_audio': str(out_audio_dst),
    }
    meta_path = OUTBOX / f'{stem}-{ts}.json'
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))

    archived = PROCESSED / f'{stem}-{ts}{path.suffix.lower()}'
    shutil.move(str(path), str(archived))
    state.setdefault('processed', {})[digest] = meta
    save_state(state)
    print(json.dumps({'status': 'ok', 'file': str(archived), 'out_audio': str(out_audio_dst)}, ensure_ascii=False), flush=True)


def main():
    ensure()
    print(f'[telegram-native-audio] watching {INBOX}', flush=True)
    while True:
        state = load_state()
        files = sorted([p for p in INBOX.iterdir() if p.is_file()])
        for p in files:
            try:
                process_file(p, state)
            except Exception as e:
                err = {'file': str(p), 'error': str(e), 'time': int(time.time())}
                print(json.dumps({'status': 'error', **err}, ensure_ascii=False), file=sys.stderr, flush=True)
        time.sleep(POLL_SECONDS)


if __name__ == '__main__':
    main()
