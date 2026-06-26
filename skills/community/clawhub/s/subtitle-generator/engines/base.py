"""ASR Engine abstract base class."""
from abc import ABC, abstractmethod
from typing import Dict, Optional


class ASREngine(ABC):
    """Abstract base class for ASR engines."""

    @abstractmethod
    def load_model(self) -> None:
        """Load the ASR model (lazy loading)."""
        ...

    @abstractmethod
    def transcribe(self, audio_path: str, language: Optional[str]) -> Dict:
        """Transcribe audio file.

        Args:
            audio_path: Path to the audio file.
            language: Language code (e.g., 'zh', 'en', 'ja') or None for auto-detect.

        Returns:
            Dict with keys:
                - "segments": List[Dict] with keys "text", "start", "end"
                - "language": Detected or specified language code
        """
        ...

    @abstractmethod
    def get_name(self) -> str:
        """Return the engine name."""
        ...
