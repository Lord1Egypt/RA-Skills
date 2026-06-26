import json
from difflib import SequenceMatcher
from pathlib import Path

from asr_engine import transcribe_audio_source
from ocr_engine import recognize_frame_texts
from utils import get_media_source_name, prepare_output_path, validate_media_source


def normalize_caption(caption: dict) -> dict:
    text = str(caption.get('captionTxt') or '').strip()
    start_us = int(caption.get('startTimeUs', 0))
    end_us = int(caption.get('endTimeUs', start_us + 1))
    if end_us <= start_us:
        end_us = start_us + 1
    confidence = caption.get('confidence', 0)
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0
    return {
        'captionTxt': text,
        'startTimeUs': start_us,
        'endTimeUs': end_us,
        'source': caption.get('source') or 'unknown',
        'confidence': round(max(0, min(1, confidence)), 4),
    }


def clean_captions(captions: list) -> list:
    cleaned = []
    last_text = None
    for raw in sorted(captions or [], key=lambda item: int(item.get('startTimeUs', 0))):
        caption = normalize_caption(raw)
        text = caption['captionTxt']
        if not text:
            continue
        if text == last_text:
            continue
        cleaned.append(caption)
        last_text = text
    return cleaned


def fuse_asr_ocr_captions(asr_captions: list, ocr_captions: list) -> list:
    if not asr_captions:
        return clean_captions(ocr_captions)
    if not ocr_captions:
        return clean_captions(asr_captions)

    fused = []
    cleaned_ocr = clean_captions(ocr_captions)
    for raw_asr in clean_captions(asr_captions):
        caption = dict(raw_asr)
        matching_ocr = [
            item for item in cleaned_ocr
            if item['endTimeUs'] >= caption['startTimeUs'] and item['startTimeUs'] <= caption['endTimeUs']
        ]
        best = None
        best_score = 0
        for item in matching_ocr:
            score = SequenceMatcher(None, caption['captionTxt'], item['captionTxt']).ratio()
            score = max(score, item.get('confidence', 0) * 0.8)
            if score > best_score:
                best = item
                best_score = score
        if best and best.get('confidence', 0) >= 0.75 and len(best['captionTxt']) >= 2:
            caption['captionTxt'] = best['captionTxt']
            caption['source'] = 'fusion'
            caption['confidence'] = round(max(caption.get('confidence', 0), best.get('confidence', 0)), 4)
        fused.append(caption)
    return clean_captions(fused)


def write_captions_json(
    captions: list,
    source: str,
    mode: str,
    output_path: str = None,
    overwrite: bool = True,
) -> str:
    name = get_media_source_name(source, fallback='captions')
    output_path = prepare_output_path(
        output_path=output_path,
        default_dir='output/subtitles',
        default_name=name,
        extension='.captions.json',
        overwrite=overwrite,
    )
    payload = {
        'source': source,
        'mode': mode,
        'captions': clean_captions(captions),
    }
    Path(output_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return output_path


def extract_subtitles(
    source: str,
    mode: str = 'fusion',
    language: str = 'auto',
    output_path: str = None,
    overwrite: bool = True,
    media_roots=None,
    model_size: str = 'base',
    sample_interval_sec: float = 1.0,
    crop_bottom_ratio: float = 0.35,
) -> dict:
    if mode not in ('asr', 'ocr', 'fusion'):
        return {'status': 'error', 'message': f'Unsupported subtitle mode: {mode}', 'code': 'unsupported_subtitle_mode'}

    try:
        source = validate_media_source(source, media_roots=media_roots)
    except ValueError as e:
        return {'status': 'error', 'message': str(e), 'code': 'invalid_source'}

    asr_result = None
    ocr_result = None
    captions = []

    if mode in ('asr', 'fusion'):
        asr_result = transcribe_audio_source(source, language=language, model_size=model_size)
        if asr_result.get('status') != 'success':
            return asr_result
        captions = asr_result.get('captions', [])

    if mode in ('ocr', 'fusion'):
        ocr_result = recognize_frame_texts(
            source,
            sample_interval_sec=sample_interval_sec,
            crop_bottom_ratio=crop_bottom_ratio,
        )
        if mode == 'ocr' and ocr_result.get('status') != 'success':
            return ocr_result
        if mode == 'ocr':
            captions = ocr_result.get('captions', [])
        elif ocr_result.get('status') == 'success':
            captions = fuse_asr_ocr_captions(captions, ocr_result.get('captions', []))

    captions = clean_captions(captions)
    try:
        final_output_path = write_captions_json(
            captions=captions,
            source=source,
            mode=mode,
            output_path=output_path,
            overwrite=overwrite,
        )
    except ValueError as e:
        return {'status': 'error', 'message': str(e), 'code': 'output_path_error'}
    except Exception as e:
        return {'status': 'error', 'message': f'字幕文件写入失败: {e}', 'code': 'caption_write_failed'}

    return {
        'status': 'success',
        'reply': f'已生成字幕：{final_output_path}',
        'source': source,
        'mode': mode,
        'outputPath': final_output_path,
        'captions': captions,
        'asr': asr_result,
        'ocr': ocr_result,
    }
