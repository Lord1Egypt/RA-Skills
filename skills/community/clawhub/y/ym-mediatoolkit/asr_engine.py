import importlib.util
import tempfile
from pathlib import Path

from utils import check_media_binaries


def is_asr_available() -> bool:
    return importlib.util.find_spec('faster_whisper') is not None


def transcribe_audio_source(
    media_source: str,
    language: str = 'auto',
    model_size: str = 'base',
) -> dict:
    if not is_asr_available():
        return {
            'status': 'error',
            'message': '缺少 ASR 依赖: faster-whisper。请运行: pip install -r requirements.txt',
            'code': 'missing_asr_dependency',
        }

    try:
        check_media_binaries('ffmpeg')
    except RuntimeError as e:
        return {'status': 'error', 'message': str(e), 'code': 'missing_ffmpeg'}

    try:
        from faster_whisper import WhisperModel
    except Exception as e:
        return {
            'status': 'error',
            'message': f'ASR 引擎加载失败: {e}',
            'code': 'asr_engine_error',
        }

    try:
        with tempfile.TemporaryDirectory() as tmp:
            audio_path = str(Path(tmp) / 'asr_input.wav')
            import subprocess
            cmd = [
                'ffmpeg',
                '-i', media_source,
                '-vn',
                '-ac', '1',
                '-ar', '16000',
                '-y',
                audio_path,
            ]
            ffmpeg_result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if ffmpeg_result.returncode != 0:
                return {
                    'status': 'error',
                    'message': f'ffmpeg 音频预处理失败，返回码: {ffmpeg_result.returncode}',
                    'code': 'ffmpeg_failed',
                }

            model = WhisperModel(model_size, device='cpu', compute_type='int8')
            kwargs = {}
            if language and language != 'auto':
                kwargs['language'] = language
            segments, info = model.transcribe(audio_path, **kwargs)

            captions = []
            for segment in segments:
                text = (segment.text or '').strip()
                if not text:
                    continue
                start_us = int(max(0, float(segment.start)) * 1_000_000)
                end_us = int(max(float(segment.end), float(segment.start)) * 1_000_000)
                if end_us <= start_us:
                    end_us = start_us + 1
                captions.append({
                    'captionTxt': text,
                    'startTimeUs': start_us,
                    'endTimeUs': end_us,
                    'source': 'asr',
                    'confidence': 1.0,
                })

        return {
            'status': 'success',
            'captions': captions,
            'language': getattr(info, 'language', language),
            'duration': getattr(info, 'duration', None),
            'engine': 'faster-whisper',
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e), 'code': 'asr_failed'}
