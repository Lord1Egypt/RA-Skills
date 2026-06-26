from pathlib import Path

from .types import TranscriptResult



def transcribe_audio(
    input_file: str,
    model_name: str,
    source_lang: str,
    device: str = "auto",
    compute_type: str = "default",
    backend: str = "faster-whisper",
) -> TranscriptResult:
    if backend == "mock":
        text = Path(input_file).read_text(encoding="utf-8").strip()
        return TranscriptResult(text=text, language=source_lang)

    from faster_whisper import WhisperModel

    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments, info = model.transcribe(input_file, language=source_lang)
    text = "".join(segment.text for segment in segments).strip()
    return TranscriptResult(text=text, language=getattr(info, "language", source_lang))
