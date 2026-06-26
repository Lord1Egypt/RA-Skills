from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class TranscriptResult:
    text: str
    language: str | None


@dataclass
class TranslationResult:
    text: str
    source_language: str
    target_language: str


@dataclass
class PipelineResult:
    input_file: str
    transcript_file: str
    translation_file: str
    audio_file: str
    metadata_file: str
    transcript: TranscriptResult
    translation: TranslationResult

    def to_dict(self) -> dict:
        data = asdict(self)
        return data
