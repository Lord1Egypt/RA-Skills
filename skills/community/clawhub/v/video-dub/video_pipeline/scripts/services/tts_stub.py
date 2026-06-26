from pathlib import Path

from services.tts_base import TTSProvider


class StubTTSProvider(TTSProvider):
    def synthesize(self, text: str, output_path: Path) -> tuple[str, float]:
        # Placeholder for a real TTS engine. We keep the contract stable for future replacement.
        return str(output_path), 0.0
