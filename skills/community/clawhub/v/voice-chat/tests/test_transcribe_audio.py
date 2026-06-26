import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from transcribe_audio import transcribe, TranscriptionError


def _have_ffmpeg():
    return shutil.which("ffmpeg") is not None


def _have_vosk_model():
    model_dir = os.environ.get("VOSK_MODEL_DIR", "/tmp/vosk-model/vosk-model-small-cn-0.22")
    return Path(model_dir).exists()


@pytest.mark.skipif(not _have_ffmpeg(), reason="ffmpeg not installed")
@pytest.mark.skipif(not _have_vosk_model(), reason="Vosk model not available")
def test_transcribe_empty_audio(tmp_path):
    # create 1s of silence wav via ffmpeg then encode ogg
    wav = tmp_path / "silence.wav"
    ogg = tmp_path / "silence.ogg"

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "anullsrc=r=16000:cl=mono",
        "-t", "1",
        str(wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(wav),
        "-c:a", "libopus",
        str(ogg)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    text = transcribe(str(ogg))
    assert isinstance(text, str)


@pytest.mark.skipif(not _have_ffmpeg(), reason="ffmpeg not installed")
@pytest.mark.skipif(not _have_vosk_model(), reason="Vosk model not available")
def test_transcribe_missing_file():
    with pytest.raises(FileNotFoundError):
        transcribe("/non/existent/file.ogg")
