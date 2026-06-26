#!/usr/bin/env python3
"""Telegram Transcription Bot - direkt Whisper API, kein LLM."""

import os
import sys
import logging
import tempfile
from pathlib import Path

from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from openai import OpenAI

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("transcribe-bot")

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sprachnachricht oder Audio transkribieren."""
    msg = update.message
    audio = msg.voice or msg.audio or msg.video_note
    if not audio:
        return

    log.info("Audio empfangen von %s (%d bytes)", msg.from_user.first_name, audio.file_size or 0)

    try:
        # Datei von Telegram herunterladen
        tg_file = await audio.get_file()
        suffix = ".ogg"
        if msg.audio and msg.audio.file_name:
            suffix = Path(msg.audio.file_name).suffix or ".ogg"

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp_path = tmp.name
            await tg_file.download_to_drive(tmp_path)

        log.info("Transkribiere %s ...", tmp_path)

        # Whisper API aufrufen
        with open(tmp_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text",
            )

        # Aufräumen
        os.unlink(tmp_path)

        text = transcript.strip() if isinstance(transcript, str) else transcript.text.strip()

        if text:
            await msg.reply_text(text)
            log.info("Transkription gesendet (%d Zeichen)", len(text))
        else:
            await msg.reply_text("(Keine Sprache erkannt)")

    except Exception as e:
        log.error("Fehler: %s", e)
        await msg.reply_text(f"Fehler bei der Transkription: {e}")
        # Temp-Datei aufräumen falls noch vorhanden
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Textnachrichten abweisen."""
    await update.message.reply_text("Schick mir eine Sprachnachricht — ich transkribiere sie für dich. 🎙️")


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Ich bin ein Transkriptions-Bot.\n\n"
        "Schick mir eine Sprachnachricht und ich gebe dir den Text zurück.\n"
        "Schnell, direkt, ohne Umwege."
    )


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO | filters.VIDEO_NOTE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    log.info("Transcribe Bot gestartet")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
