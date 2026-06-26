#!/usr/bin/env python3
"""
Gera áudio a partir de texto usando EDGE TTS.
"""
import sys
import asyncio
import edge_tts

VOICE = "pt-BR-FranciscaNeural"


async def generate_audio(text: str, output_path: str):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: generate_audio.py <texto> <caminho_saida>")
        sys.exit(1)

    text = sys.argv[1]
    output_path = sys.argv[2]

    try:
        asyncio.run(generate_audio(text, output_path))
        print(f"Áudio gerado: {output_path}")
    except Exception as e:
        print(f"Erro ao gerar áudio: {e}", file=sys.stderr)
        sys.exit(1)
