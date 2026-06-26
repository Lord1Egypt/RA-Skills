from abc import ABC, abstractmethod
from pathlib import Path


class TTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, output_path: Path, context_text: str = "") -> tuple[str, float]:
        """Generate TTS audio and return relative/absolute file path plus duration in seconds."""
