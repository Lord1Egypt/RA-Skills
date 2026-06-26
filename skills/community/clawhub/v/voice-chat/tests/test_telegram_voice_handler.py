import os
import shutil
from pathlib import Path

import pytest

from telegram_voice_handler import (
    download_telegram_voice,
    send_telegram_voice,
    process_telegram_voice_message,
    TelegramError,
)


def _env_has_token_and_chat():
    return bool(os.environ.get("TELEGRAM_BOT_TOKEN")) and bool(os.environ.get("TELEGRAM_CHAT_ID"))


def _have_ffmpeg():
    return shutil.which("ffmpeg") is not None


def _have_edge_tts():
    bin_path = os.environ.get('EDGE_TTS_BIN') or shutil.which('edge-tts')
    return bin_path is not None and Path(bin_path).exists()


def _have_vosk_model():
    model_dir = os.environ.get("VOSK_MODEL_DIR", "/tmp/vosk-model/vosk-model-small-cn-0.22")
    return Path(model_dir).exists()


@pytest.mark.skipif(not _env_has_token_and_chat(), reason="TELEGRAM_BOT_TOKEN/CHAT_ID not set")
@pytest.mark.skip("network-required: requires real Telegram file_id and network access")
def test_download_telegram_voice_smoke():
    # Provide a valid file_id via env for manual smoke test
    file_id = os.environ.get("TELEGRAM_TEST_FILE_ID")
    if not file_id:
        pytest.skip("TELEGRAM_TEST_FILE_ID not provided")
    local = download_telegram_voice(file_id)
    assert Path(local).exists()


@pytest.mark.skipif(not _env_has_token_and_chat(), reason="TELEGRAM_BOT_TOKEN/CHAT_ID not set")
@pytest.mark.skipif(not _have_ffmpeg(), reason="ffmpeg not installed")
@pytest.mark.skipif(not _have_edge_tts(), reason="edge-tts not installed")
@pytest.mark.skipif(not _have_vosk_model(), reason="Vosk model not available")
@pytest.mark.skip("network-required: sends a message to Telegram chat")
def test_full_flow_with_send(monkeypatch, tmp_path):
    # This test requires a real voice file_id. If provided, it will process and send back a voice.
    file_id = os.environ.get("TELEGRAM_TEST_FILE_ID")
    if not file_id:
        pytest.skip("TELEGRAM_TEST_FILE_ID not provided")
    transcript, reply, voice = process_telegram_voice_message(file_id, reply_template="您说：{transcript}")
    assert isinstance(transcript, str)
    assert reply.startswith("您说：")
    assert Path(voice).exists()
    resp = send_telegram_voice(voice, caption=reply)
    assert resp.get("ok") is True
