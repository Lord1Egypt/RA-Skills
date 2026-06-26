"""OpenAI Whisper ASR engine implementation."""
import sys
from pathlib import Path
from typing import Dict, Optional

# Add whisper venv to sys.path if available
WHISPER_VENV_SITE = Path.home() / ".whisper-venv" / "lib" / "python3.12" / "site-packages"
if WHISPER_VENV_SITE.exists() and str(WHISPER_VENV_SITE) not in sys.path:
    sys.path.insert(0, str(WHISPER_VENV_SITE))

from engines.base import ASREngine


class OpenAIWhisperEngine(ASREngine):
    """ASR engine using openai-whisper (fallback)."""

    MODEL_SIZE = "medium"

    def __init__(self) -> None:
        self.model = None

    def load_model(self) -> None:
        """Load the openai-whisper model."""
        if self.model is None:
            try:
                import whisper
            except ImportError as e:
                raise ImportError(
                    "openai-whisper not installed. "
                    "Install with: pip install openai-whisper"
                ) from e

            print(f"正在加载 OpenAI Whisper 模型 ({self.MODEL_SIZE})...")
            self.model = whisper.load_model(self.MODEL_SIZE)

    def transcribe(self, audio_path: str, language: Optional[str]) -> Dict:
        """Transcribe audio using openai-whisper."""
        self.load_model()

        options = {
            "task": "transcribe",
            "verbose": False,
        }
        if language:
            options["language"] = language

        print("正在进行语音识别 (OpenAI Whisper)...")
        result = self.model.transcribe(str(audio_path), **options)

        return {
            "segments": result["segments"],
            "language": result.get("language", "unknown"),
        }

    def get_name(self) -> str:
        return "OpenAI Whisper"
