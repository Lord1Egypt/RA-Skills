"""Faster-Whisper ASR engine implementation."""
import sys
from pathlib import Path
from typing import Dict, Optional

# Add whisper venv to sys.path if available
WHISPER_VENV_SITE = Path.home() / ".whisper-venv" / "lib" / "python3.12" / "site-packages"
if WHISPER_VENV_SITE.exists() and str(WHISPER_VENV_SITE) not in sys.path:
    sys.path.insert(0, str(WHISPER_VENV_SITE))

from engines.base import ASREngine


class FasterWhisperEngine(ASREngine):
    """ASR engine using faster-whisper (preferred)."""

    MODEL_SIZE = "medium"

    def __init__(self) -> None:
        self.model = None

    def load_model(self) -> None:
        """Load the faster-whisper model."""
        if self.model is None:
            try:
                from faster_whisper import WhisperModel
            except ImportError as e:
                raise ImportError(
                    "faster-whisper not installed. "
                    "Install with: pip install faster-whisper"
                ) from e

            print(f"正在加载 Faster-Whisper 模型 ({self.MODEL_SIZE})...")
            self.model = WhisperModel(
                self.MODEL_SIZE,
                device="auto",
                compute_type="auto",
            )

    def transcribe(self, audio_path: str, language: Optional[str]) -> Dict:
        """Transcribe audio using faster-whisper."""
        self.load_model()

        print("正在进行语音识别 (Faster-Whisper)...")
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            vad_filter=True,
        )

        # Convert generator to list
        segment_list = []
        for seg in segments:
            segment_list.append({
                "text": seg.text,
                "start": seg.start,
                "end": seg.end,
            })

        return {
            "segments": segment_list,
            "language": info.language,
        }

    def get_name(self) -> str:
        return "Faster-Whisper"
