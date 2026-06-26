#!/usr/bin/env python3
"""
Runner fim a fim para Telegram Native Audio.

Objetivo:
- executar teste ponta a ponta local (B);
- servir como base do modo automático por áudio recebido (C).

Fluxo:
1. recebe um arquivo de áudio local;
2. transcreve com GROQ Whisper;
3. gera uma resposta textual simples;
4. sintetiza a resposta com EDGE TTS;
5. opcionalmente envia o áudio de volta pelo canal atual do Picoclaw.

Uso:
  python3 runner.py process /tmp/audio.ogg
  python3 runner.py process /tmp/audio.ogg --reply-text "Texto fixo"
  python3 runner.py process /tmp/audio.ogg --send --chat-id SEU_CHAT_ID
"""
import sys
import os
import asyncio
import tempfile
from pathlib import Path

# Import direct functions to avoid subprocesses
from transcribe_audio import transcribe_audio
from generate_audio import generate_audio

VOICE = "pt-BR-FranciscaNeural"
BASE_DIR = Path(__file__).resolve().parent

def fail(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)

def transcribe(audio_path: str) -> str:
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        fail("GROQ_API_KEY não configurada")
    try:
        return transcribe_audio(audio_path, api_key)
    except Exception as e:
        fail(f"Falha na transcrição: {e}")

def build_reply(transcription: str, forced_reply: str | None = None) -> str:
    if forced_reply:
        return forced_reply.strip()
    text = transcription.strip()
    if not text:
        return "Recebi seu áudio, mas não consegui entender o conteúdo com clareza. Pode repetir, por favor?"
    return (
        "Recebi seu áudio. "
        f"Você disse: {text}. "
        "Se quiser, agora eu posso transformar isso em fluxo automático dentro da skill."
    )

async def generate(reply_text: str, output_path: str):
    try:
        await generate_audio(reply_text, output_path)
    except Exception as e:
        fail(f"Falha na geração de áudio: {e}")

def parse_args(argv: list[str]) -> dict:
    if len(argv) < 3 or argv[1] != "process":
        fail(
            "Uso: python3 runner.py process <audio_path> [--reply-text TEXTO] [--send] [--chat-id ID]",
            2,
        )

    audio_path = argv[2]
    send = False
    chat_id = os.environ.get("PICOLAW_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID") or ""
    reply_text = None

    i = 3
    while i < len(argv):
        token = argv[i]
        if token == "--send":
            send = True
            i += 1
        elif token == "--chat-id":
            if i + 1 >= len(argv):
                fail("--chat-id exige um valor")
            chat_id = argv[i + 1]
            i += 2
        elif token == "--reply-text":
            if i + 1 >= len(argv):
                fail("--reply-text exige um valor")
            reply_text = argv[i + 1]
            i += 2
        else:
            fail(f"Argumento desconhecido: {token}")

    return {
        "audio_path": audio_path,
        "send": send,
        "chat_id": chat_id,
        "reply_text": reply_text,
    }

async def main():
    args = parse_args(sys.argv)
    audio_path = args["audio_path"]
    if not os.path.exists(audio_path):
        fail(f"Arquivo não encontrado: {audio_path}")

    transcription = transcribe(audio_path)
    reply = build_reply(transcription, args["reply_text"])

    with tempfile.NamedTemporaryFile(prefix="telegram-native-audio-", suffix=".mp3", delete=False) as tmp:
        output_path = tmp.name

    await generate(reply, output_path)

    print("=== TRANSCRIÇÃO ===")
    print(transcription)
    print("=== RESPOSTA ===")
    print(reply)
    print("=== AUDIO_FILE ===")
    print(output_path)
    print("=== SEND_REQUESTED ===")
    print("yes" if args["send"] else "no")
    print("=== CHAT_ID ===")
    print(args["chat_id"])

if __name__ == "__main__":
    asyncio.run(main())
