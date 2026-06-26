import os
import shutil
from pathlib import Path

import pytest

from feishu_voice_handler import process_feishu_voice_message, VoiceHandlerError


def _have_ffmpeg():
    return shutil.which("ffmpeg") is not None


def _have_edge_tts():
    bin_path = os.environ.get('EDGE_TTS_BIN') or shutil.which('edge-tts')
    return bin_path is not None and Path(bin_path).exists()


def _have_vosk_model():
    model_dir = os.environ.get("VOSK_MODEL_DIR", "/tmp/vosk-model/vosk-model-small-cn-0.22")
    return Path(model_dir).exists()


@pytest.mark.skipif(not _have_ffmpeg(), reason="ffmpeg not installed")
@pytest.mark.skipif(not _have_edge_tts(), reason="edge-tts not installed")
@pytest.mark.skipif(not _have_vosk_model(), reason="Vosk model not available")
def test_full_flow(tmp_path):
    # generate a short sine tone (not Chinese speech, but should still flow)
    ogg = tmp_path / "tone.ogg"
    # 0.5s sine tone then transcode to ogg/opus
    import subprocess
    wav = tmp_path / "tone.wav"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "sine=frequency=1000:duration=0.5",
        str(wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(wav),
        "-c:a", "libopus",
        str(ogg)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    transcript, reply, voice = process_feishu_voice_message(str(ogg), reply_template="您说：{transcript}")
    assert isinstance(transcript, str)
    assert reply.startswith("您说：")
    assert Path(voice).exists()
