import os
import shutil
from pathlib import Path

import pytest

from reply_with_tts import synthesize_to_feishu_voice, TTSGenerationError, list_available_voices


def _have_ffmpeg():
    return shutil.which("ffmpeg") is not None


def _have_edge_tts():
    bin_path = os.environ.get('EDGE_TTS_BIN') or shutil.which('edge-tts')
    return bin_path is not None and Path(bin_path).exists()


@pytest.mark.skipif(not _have_ffmpeg(), reason="ffmpeg not installed")
@pytest.mark.skipif(not _have_edge_tts(), reason="edge-tts not installed")
def test_tts_basic(tmp_path):
    # Pick a valid voice if available
    voices = list_available_voices()
    voice = voices[0] if voices else None
    out = synthesize_to_feishu_voice("测试语音", voice=voice, output_dir=str(tmp_path))
    assert Path(out).exists()
    assert out.endswith('.ogg')


def test_tts_empty_text():
    with pytest.raises(ValueError):
        synthesize_to_feishu_voice("   ")
