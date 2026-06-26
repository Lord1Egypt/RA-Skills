#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time
from pathlib import Path

BASE = Path('/root/.picoclaw/workspace/state/telegram-native-audio')
PENDING = BASE / 'pending'
SENT = BASE / 'sent'
GENERATE = Path('/root/.picoclaw/workspace/skills/telegram-native-audio/scripts/generate_audio.py')


def fail(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def main():
    if len(sys.argv) < 3:
        fail('Uso: finalize_reply.py <meta.json> <texto da resposta>')
    meta_path = Path(sys.argv[1])
    reply = ' '.join(sys.argv[2:]).strip()
    if not meta_path.exists():
        fail(f'Meta não encontrado: {meta_path}')
    if not reply:
        fail('Resposta vazia')
    meta = json.loads(meta_path.read_text())
    SENT.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    out = SENT / f"{meta_path.stem}-{ts}.mp3"
    r = subprocess.run(['python3', str(GENERATE), reply, str(out)], capture_output=True, text=True, env=os.environ.copy())
    if r.returncode != 0:
        fail(r.stderr.strip() or r.stdout.strip() or 'falha ao gerar áudio')
    meta['reply'] = reply
    meta['reply_audio'] = str(out)
    meta['status'] = 'ready_to_send'
    meta['finalized_at'] = ts
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print(json.dumps({'status': 'ready_to_send', 'meta_file': str(meta_path), 'audio_file': str(out), 'chat_id': meta.get('chat_id')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
