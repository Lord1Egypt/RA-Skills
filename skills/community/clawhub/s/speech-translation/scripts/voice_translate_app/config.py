from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    input_file: Path
    output_dir: Path
    source_lang: str
    target_lang: str
    whisper_model: str
    piper_model: Path
    transcribe_backend: str = "faster-whisper"
    tts_backend: str = "piper"
    translation_backend: str = "llm"
    translation_file: Path | None = None
    interactive_translate: bool = True
    translation_service_url: str | None = None
    transcript_command: str | None = None
    translation_command: str | None = None
    audio_command: str | None = None
    piper_binary: str = "piper"
    device: str = "auto"
    compute_type: str = "default"
