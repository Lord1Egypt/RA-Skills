#!/usr/bin/env python3
"""
Transcreve áudio usando GROQ Whisper API.
"""
import sys
import os
from groq import Groq


def transcribe_audio(audio_path: str, api_key: str) -> str:
    client = Groq(api_key=api_key)
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audio_path, file.read()),
            model="whisper-large-v3-turbo",
            language="pt",
            response_format="text"
        )
    return transcription.strip()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: transcribe_audio.py <caminho_audio> <groq_api_key>")
        sys.exit(1)

    audio_path = sys.argv[1]
    api_key = sys.argv[2]

    if not os.path.exists(audio_path):
        print(f"Erro: Arquivo não encontrado: {audio_path}", file=sys.stderr)
        sys.exit(1)

    try:
        texto = transcribe_audio(audio_path, api_key)
        print(texto)
    except Exception as e:
        print(f"Erro na transcrição: {e}", file=sys.stderr)
        sys.exit(1)
