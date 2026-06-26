from pathlib import Path

from .config import AppConfig
from .notifier import CommandNotifier, ConsoleNotifier
from .transcribe import transcribe_audio
from .translate import translate_text
from .tts import synthesize_with_piper
from .types import PipelineResult
from .utils import ensure_dir, write_json, write_text



def run_pipeline(config: AppConfig) -> PipelineResult:
    output_dir = ensure_dir(config.output_dir)

    transcript_path = output_dir / "01_transcript.txt"
    translation_path = output_dir / "02_translation.txt"
    audio_path = output_dir / "03_translation.wav"
    metadata_path = output_dir / "result.json"

    notifier = CommandNotifier(
        transcript_command=config.transcript_command,
        translation_command=config.translation_command,
        audio_command=config.audio_command,
    )
    fallback_notifier = ConsoleNotifier()

    transcript = transcribe_audio(
        input_file=str(config.input_file),
        model_name=config.whisper_model,
        source_lang=config.source_lang,
        device=config.device,
        compute_type=config.compute_type,
        backend=config.transcribe_backend,
    )
    write_text(transcript_path, transcript.text)
    notifier.notify_transcript(transcript.text)
    fallback_notifier.notify_transcript(transcript.text)

    translation = translate_text(
        text=transcript.text,
        source_lang=config.source_lang,
        target_lang=config.target_lang,
        backend=config.translation_backend,
        translation_file=config.translation_file,
        interactive=config.interactive_translate,
        translation_service_url=config.translation_service_url,
    )
    write_text(translation_path, translation.text)
    notifier.notify_translation(translation.text)
    fallback_notifier.notify_translation(translation.text)

    synthesize_with_piper(
        text=translation.text,
        output_wav=audio_path,
        model_path=config.piper_model,
        piper_binary=config.piper_binary,
        backend=config.tts_backend,
    )
    notifier.notify_audio(audio_path)
    fallback_notifier.notify_audio(audio_path)

    result = PipelineResult(
        input_file=str(config.input_file),
        transcript_file=str(transcript_path),
        translation_file=str(translation_path),
        audio_file=str(audio_path),
        metadata_file=str(metadata_path),
        transcript=transcript,
        translation=translation,
    )
    write_json(metadata_path, result.to_dict())
    return result
