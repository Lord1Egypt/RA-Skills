#!/usr/bin/env python3
"""
ClawHub Skill 统一入口 - 流式视频处理
支持:
1. 压缩: ffmpeg 流式处理，无需下载
2. 封面: 部分下载，只取需要的帧
3. 音频: 流式提取，转 MP3/WAV
"""

import sys
import json
import argparse
import logging
from pathlib import Path

from utils import check_media_binaries, get_media_source_name, sanitize_output_path, validate_media_source
from intent_parser import parse_media_intent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入模块
from frame_extractor import extract_thumbnail_from_url
from video_compressor import compress_video_streaming, compress_with_adaptive_crf
from audio_extractor import extract_audio_streaming, extract_audio_batch, get_audio_info
from subtitle_extractor import extract_subtitles
from caption_segmenter import (
    load_captions_payload,
    load_protected_terms,
    segment_captions,
    write_segmented_captions_json,
)
from job_manager import JobManager, collect_output_paths, protocol_error


def get_input_source(params: dict) -> str:
    return params.get('video_url') or params.get('url') or params.get('source')


def normalized_video_params(params: dict) -> dict:
    source = get_input_source(params)
    if source and 'video_url' not in params:
        return {**params, 'video_url': source}
    return params

def handle_compress(params: dict) -> dict:
    params = normalized_video_params(params)
    video_url = params.get('video_url')
    if not video_url:
        return {'status': 'error', 'message': 'Missing video_url/url/source'}
    try:
        video_url = validate_media_source(video_url, media_roots=params.get('media_roots'))
        check_media_binaries('ffmpeg')
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    except RuntimeError as e:
        return {'status': 'error', 'message': str(e)}
    
    output_path = params.get('output_path')
    if output_path:
        try:
            output_path = sanitize_output_path(output_path)
        except ValueError as e:
            return {'status': 'error', 'message': str(e)}
    target_ratio = params.get('target_ratio', 0.1)
    adaptive = params.get('adaptive', True)
    crf = params.get('crf', 24)
    preset = params.get('preset', 'veryfast')
    overwrite = params.get('overwrite', True)
    
    logger.info(f"压缩请求: {video_url[:80]}...")
    
    if adaptive:
        try:
            result = compress_with_adaptive_crf(
                video_url=video_url,
                output_path=output_path,
                target_ratio=target_ratio,
                max_attempts=params.get('max_attempts', 3),
                overwrite=overwrite,
                media_roots=params.get('media_roots')
            )
        except ValueError as e:
            return {'status': 'error', 'message': str(e)}
    else:
        try:
            result = compress_video_streaming(
                video_url=video_url,
                output_path=output_path,
                target_ratio=target_ratio,
                crf=crf,
                preset=preset,
                overwrite=overwrite,
                media_roots=params.get('media_roots')
            )
        except ValueError as e:
            return {'status': 'error', 'message': str(e)}
    
    return result


def handle_thumbnail(params: dict) -> dict:
    params = normalized_video_params(params)
    video_url = params.get('video_url')
    if not video_url:
        return {'status': 'error', 'message': 'Missing video_url/url/source'}
    try:
        video_url = validate_media_source(video_url, media_roots=params.get('media_roots'))
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    
    time_seconds = params.get('time_seconds')
    frame_number = params.get('frame_number')
    
    if time_seconds is None and frame_number is None:
        time_seconds = 0
    
    save_path = params.get('save_path')
    if save_path:
        try:
            save_path = sanitize_output_path(save_path)
        except ValueError as e:
            return {'status': 'error', 'message': str(e)}
    resize_width = params.get('resize_width')
    quality = params.get('quality', 85)
    overwrite = params.get('overwrite', True)
    
    logger.info(f"封面提取: {video_url[:80]}... time={time_seconds}, frame={frame_number}")
    
    result = extract_thumbnail_from_url(
        video_url=video_url,
        time_seconds=time_seconds,
        frame_number=frame_number,
        save_path=save_path,
        resize_width=resize_width,
        quality=quality,
        overwrite=overwrite,
        media_roots=params.get('media_roots')
    )
    
    return result


def handle_audio(params: dict) -> dict:
    params = normalized_video_params(params)
    video_url = params.get('video_url')
    if not video_url:
        return {'status': 'error', 'message': 'Missing video_url/url/source'}
    try:
        video_url = validate_media_source(video_url, media_roots=params.get('media_roots'))
        check_media_binaries('ffmpeg')
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    except RuntimeError as e:
        return {'status': 'error', 'message': str(e)}
    
    output_path = params.get('output_path')
    if output_path:
        try:
            output_path = sanitize_output_path(output_path)
        except ValueError as e:
            return {'status': 'error', 'message': str(e)}
    audio_format = params.get('format', 'mp3')  # mp3, wav, aac, m4a
    audio_bitrate = params.get('bitrate', '128k')
    sample_rate = params.get('sample_rate', 44100)
    channels = params.get('channels', 2)
    start_time = params.get('start_time')
    duration = params.get('duration')
    overwrite = params.get('overwrite', True)
    
    # 格式验证
    if audio_format not in ['mp3', 'wav', 'aac', 'm4a']:
        return {'status': 'error', 'message': f'Unsupported format: {audio_format}. Supported: mp3, wav, aac, m4a'}
    
    logger.info(f"音频提取: {video_url[:80]}... format={audio_format}, bitrate={audio_bitrate}")
    
    try:
        result = extract_audio_streaming(
            video_url=video_url,
            output_path=output_path,
            audio_format=audio_format,
            audio_bitrate=audio_bitrate,
            sample_rate=sample_rate,
            channels=channels,
            start_time=start_time,
            duration=duration,
            overwrite=overwrite,
            media_roots=params.get('media_roots')
        )
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    
    return result


def handle_audio_batch(params: dict) -> dict:
    """批量音频提取"""
    videos = params.get('videos', [])
    if not videos:
        return {'status': 'error', 'message': 'Missing videos list'}
    
    output_dir = params.get('output_dir', 'output/audio')
    try:
        output_dir = sanitize_output_path(output_dir)
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    audio_format = params.get('format', 'mp3')
    audio_bitrate = params.get('bitrate', '128k')
    sample_rate = params.get('sample_rate', 44100)
    overwrite = params.get('overwrite', True)
    
    logger.info(f"批量音频提取: {len(videos)} 个视频, 格式={audio_format}")
    
    result = extract_audio_batch(
        videos=videos,
        output_dir=output_dir,
        audio_format=audio_format,
        audio_bitrate=audio_bitrate,
        sample_rate=sample_rate,
        overwrite=overwrite,
        media_roots=params.get('media_roots')
    )
    
    return result


def handle_audio_info(params: dict) -> dict:
    params = normalized_video_params(params)
    video_url = params.get('video_url')
    if not video_url:
        return {'status': 'error', 'message': 'Missing video_url/url/source'}
    try:
        video_url = validate_media_source(video_url, media_roots=params.get('media_roots'))
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    
    logger.info(f"获取音频信息: {video_url[:80]}...")
    
    result = get_audio_info(video_url, media_roots=params.get('media_roots'))
    return result


def handle_batch(params: dict) -> dict:
    """批量处理（压缩/封面）"""
    videos = params.get('videos', [])
    action = params.get('action', 'thumbnail')
    output_dir = params.get('output_dir')
    overwrite = params.get('overwrite', True)
    
    if not videos:
        return {'status': 'error', 'message': 'Missing videos list'}
    
    results = []
    for i, video in enumerate(videos):
        logger.info(f"批量处理 [{i+1}/{len(videos)}]")
        video = normalized_video_params({**params, **video})
        video.pop('videos', None)
        video.pop('action', None)
        video.pop('output_dir', None)
        if action == 'compress':
            if output_dir and not video.get('output_path'):
                import os
                try:
                    safe_output_dir = sanitize_output_path(output_dir)
                except ValueError as e:
                    res = {'status': 'error', 'message': str(e)}
                    results.append(res)
                    continue
                os.makedirs(safe_output_dir, exist_ok=True)
                source_name = get_media_source_name(get_input_source(video) or '', fallback=f'video_{i+1}')
                name = video.get('name') or f"compressed_{source_name}"
                video['output_path'] = str(Path(safe_output_dir) / f"{name}.mp4")
            elif video.get('name') and not video.get('output_path'):
                video['output_path'] = str(Path('output/videos') / f"{video['name']}.mp4")
            res = handle_compress(video)
        elif action == 'audio':
            if output_dir and not video.get('output_path'):
                import os
                try:
                    safe_output_dir = sanitize_output_path(output_dir)
                except ValueError as e:
                    res = {'status': 'error', 'message': str(e)}
                    results.append(res)
                    continue
                os.makedirs(safe_output_dir, exist_ok=True)
                audio_format = video.get('format', params.get('format', 'mp3'))
                source_name = get_media_source_name(get_input_source(video) or '', fallback=f'audio_{i+1}')
                name = video.get('name') or source_name
                video = {
                    **params,
                    **video,
                    'output_path': str(Path(safe_output_dir) / f"{name}.{audio_format}")
                }
                video.pop('videos', None)
                video.pop('action', None)
                video.pop('output_dir', None)
            elif video.get('name') and not video.get('output_path'):
                audio_format = video.get('format', params.get('format', 'mp3'))
                video['output_path'] = str(Path('output/audio') / f"{video['name']}.{audio_format}")
            res = handle_audio(video)
        else:
            if output_dir and not video.get('save_path'):
                import os
                try:
                    safe_output_dir = sanitize_output_path(output_dir)
                except ValueError as e:
                    res = {'status': 'error', 'message': str(e)}
                    results.append(res)
                    continue
                os.makedirs(safe_output_dir, exist_ok=True)
                source_name = get_media_source_name(get_input_source(video) or '', fallback=f'thumbnail_{i+1}')
                name = video.get('name') or source_name
                video = {
                    **params,
                    **video,
                    'save_path': str(Path(safe_output_dir) / f"{name}.jpg")
                }
                video.pop('videos', None)
                video.pop('action', None)
                video.pop('output_dir', None)
            elif video.get('name') and not video.get('save_path'):
                video['save_path'] = str(Path('output/thumbs') / f"{video['name']}.jpg")
            res = handle_thumbnail(video)
        results.append(res)
    
    success_count = sum(1 for r in results if r.get('status') == 'success')
    
    return {
        'status': 'success',
        'total': len(results),
        'success': success_count,
        'failed': len(results) - success_count,
        'results': results
    }


def handle_info(params: dict) -> dict:
    params = normalized_video_params(params)
    video_url = params.get('video_url')
    if not video_url:
        return {'status': 'error', 'message': 'Missing video_url/url/source'}
    try:
        video_url = validate_media_source(video_url, media_roots=params.get('media_roots'))
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    
    from utils import is_remote_source
    from frame_extractor import RemoteVideoFrameExtractor, get_local_video_info
    
    try:
        if is_remote_source(video_url):
            extractor = RemoteVideoFrameExtractor(video_url, timeout=30)
            info = extractor.get_video_info()
            info['file_size_mb'] = round(extractor.file_size / (1024 * 1024), 2)
        else:
            info = get_local_video_info(video_url)
            info['file_size_mb'] = round(Path(video_url).stat().st_size / (1024 * 1024), 2)
        return {'status': 'success', 'info': info}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def handle_subtitle(params: dict) -> dict:
    params = normalized_video_params(params)
    source = params.get('video_url')
    if not source:
        return {'status': 'error', 'message': 'Missing video_url/url/source'}
    output_path = params.get('output_path') or params.get('save_path')
    if output_path:
        try:
            output_path = sanitize_output_path(output_path)
        except ValueError as e:
            return {'status': 'error', 'message': str(e)}
    return extract_subtitles(
        source=source,
        mode=params.get('mode', 'fusion'),
        language=params.get('language', 'auto'),
        output_path=output_path,
        overwrite=params.get('overwrite', True),
        media_roots=params.get('media_roots'),
        model_size=params.get('model_size', 'base'),
        sample_interval_sec=params.get('sample_interval_sec', 1.0),
        crop_bottom_ratio=params.get('crop_bottom_ratio', 0.35),
    )


def handle_asr(params: dict) -> dict:
    return handle_subtitle({**params, 'mode': 'asr'})


def handle_ocr(params: dict) -> dict:
    return handle_subtitle({**params, 'mode': 'ocr'})


def handle_caption_segment(params: dict) -> dict:
    caption_path = params.get('caption_path') or params.get('input_path')
    captions = params.get('captions')
    source = params.get('source')

    if caption_path:
        try:
            payload = load_captions_payload(caption_path)
        except ValueError as e:
            return {'status': 'error', 'message': str(e), 'code': 'invalid_caption_input'}
        captions = captions or payload.get('captions')
        source = source or payload.get('source') or caption_path

    if not isinstance(captions, list):
        return {'status': 'error', 'message': 'Missing captions or caption_path', 'code': 'missing_captions'}

    try:
        max_chars = int(params.get('max_chars', 12))
        if max_chars <= 0:
            raise ValueError('max_chars must be positive')
        protected_terms = load_protected_terms(
            params.get('protected_terms'),
            params.get('protected_terms_path'),
        )
        segmented = segment_captions(
            captions,
            max_chars=max_chars,
            protected_terms=protected_terms,
            auto_protect_ascii=params.get('auto_protect_ascii', True),
        )
        output_path = write_segmented_captions_json(
            captions=segmented,
            output_path=params.get('output_path'),
            caption_path=caption_path,
            source=source,
            max_chars=max_chars,
            protected_terms=protected_terms,
            overwrite=params.get('overwrite', True),
        )
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        return {'status': 'error', 'message': f'字幕分句失败: {e}', 'code': 'caption_segment_failed'}

    return {
        'status': 'success',
        'reply': f'已完成字幕分句：{output_path}',
        'source': source,
        'mode': 'segment',
        'outputPath': output_path,
        'maxChars': max_chars,
        'protectedTerms': protected_terms,
        'captions': segmented,
    }


PIPELINE_STEP_HANDLERS = {
    'info': handle_info,
    'thumbnail': handle_thumbnail,
    'audio': handle_audio,
    'compress': handle_compress,
    'audio_info': handle_audio_info,
    'asr': handle_asr,
    'ocr': handle_ocr,
    'subtitle': handle_subtitle,
    'caption_segment': handle_caption_segment,
}


def _pipeline_status(step_results: list) -> str:
    if not step_results:
        return 'error'
    executed = [step for step in step_results if step.get('status') != 'skipped']
    if not executed:
        return 'skipped'
    success_count = sum(1 for step in executed if step.get('status') == 'success')
    failed_count = len(executed) - success_count
    if success_count and failed_count:
        return 'partial'
    if success_count == len(executed):
        return 'success'
    return 'error'


def _pipeline_default_output_path(step_id: str, action: str, output_dir: str, params: dict) -> dict:
    if action == 'thumbnail' and not params.get('save_path'):
        return {**params, 'save_path': str(Path(output_dir) / f"{step_id}.jpg")}
    if action == 'audio' and not params.get('output_path'):
        audio_format = params.get('format', 'mp3')
        return {**params, 'output_path': str(Path(output_dir) / f"{step_id}.{audio_format}")}
    if action == 'compress' and not params.get('output_path'):
        return {**params, 'output_path': str(Path(output_dir) / f"{step_id}.mp4")}
    if action in ('asr', 'ocr', 'subtitle') and not params.get('output_path'):
        return {**params, 'output_path': str(Path(output_dir) / f"{step_id}.captions.json")}
    if action == 'caption_segment' and not params.get('output_path'):
        return {**params, 'output_path': str(Path(output_dir) / f"{step_id}.captions.json")}
    return params


def _latest_caption_output_path(step_results: list) -> str:
    for step in reversed(step_results):
        result = step.get('result') or {}
        for path in reversed(collect_output_paths(result)):
            if path.endswith('.captions.json'):
                return path
    return None


def handle_pipeline(params: dict) -> dict:
    """JSON 驱动的同步媒体流水线。"""
    source = get_input_source(params)
    if not source:
        return {'status': 'error', 'message': 'Missing video_url/url/source'}

    steps = params.get('steps')
    if not isinstance(steps, list) or not steps:
        return {'status': 'error', 'message': 'Missing steps list'}

    try:
        source = validate_media_source(source, media_roots=params.get('media_roots'))
        name = params.get('name') or get_media_source_name(source, fallback='pipeline')
        output_dir = sanitize_output_path(params.get('output_dir') or str(Path('output/pipeline') / name))
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}

    overwrite = params.get('overwrite', True)
    output_dir_path = Path(output_dir)
    manifest_path = output_dir_path / 'manifest.json'
    if manifest_path.exists() and not overwrite:
        return {'status': 'error', 'message': f'输出文件已存在且 overwrite=false: {manifest_path}'}

    output_dir_path.mkdir(parents=True, exist_ok=True)
    step_results = []

    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            step_results.append({
                'id': f'step_{index + 1}',
                'action': None,
                'status': 'error',
                'message': 'Step must be an object'
            })
            continue

        step_id = step.get('id')
        action = step.get('action')
        if not step_id or not action or 'enabled' not in step:
            step_results.append({
                'id': step_id or f'step_{index + 1}',
                'action': action,
                'status': 'error',
                'message': 'Step requires id, action, and enabled'
            })
            continue

        if not isinstance(step.get('enabled'), bool):
            step_results.append({
                'id': step_id,
                'action': action,
                'status': 'error',
                'message': 'Step enabled must be boolean'
            })
            continue

        if not step['enabled']:
            step_results.append({
                'id': step_id,
                'action': action,
                'status': 'skipped'
            })
            continue

        handler = PIPELINE_STEP_HANDLERS.get(action)
        if handler is None:
            step_results.append({
                'id': step_id,
                'action': action,
                'status': 'error',
                'message': f'Unsupported pipeline action: {action}'
            })
            continue

        step_params = step.get('params') or {}
        if not isinstance(step_params, dict):
            step_results.append({
                'id': step_id,
                'action': action,
                'status': 'error',
                'message': 'Step params must be an object'
            })
            continue

        call_params = {
            'video_url': source,
            'name': name,
            'overwrite': overwrite,
            'media_roots': params.get('media_roots'),
            **step_params
        }
        if action == 'caption_segment' and not call_params.get('captions') and not call_params.get('caption_path'):
            previous_caption_path = _latest_caption_output_path(step_results)
            if previous_caption_path:
                call_params['caption_path'] = previous_caption_path
        call_params = _pipeline_default_output_path(step_id, action, output_dir, call_params)

        try:
            result = handler(call_params)
        except Exception as e:
            result = {'status': 'error', 'message': str(e)}

        step_results.append({
            'id': step_id,
            'action': action,
            'status': result.get('status', 'error'),
            'params': call_params,
            'result': result
        })

    executed = [step for step in step_results if step.get('status') != 'skipped']
    success_count = sum(1 for step in executed if step.get('status') == 'success')
    failed_count = len(executed) - success_count
    status = _pipeline_status(step_results)

    manifest = {
        'status': status,
        'source': source,
        'name': name,
        'output_dir': output_dir,
        'manifest_path': str(manifest_path),
        'total_steps': len(step_results),
        'success': success_count,
        'failed': failed_count,
        'skipped': sum(1 for step in step_results if step.get('status') == 'skipped'),
        'steps': step_results
    }

    try:
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    except Exception as e:
        return {'status': 'error', 'message': f'写入 manifest 失败: {e}', 'manifest': manifest}

    return manifest


def _chat_reply(action: str, result: dict, output_paths: list) -> str:
    status = result.get('status')
    if status in ('success', 'partial', 'skipped'):
        if action == 'audio' and output_paths:
            return f"已提取音频：{output_paths[0]}"
        if action == 'thumbnail' and output_paths:
            return f"已提取封面：{output_paths[0]}"
        if action == 'compress' and output_paths:
            return f"已压缩视频：{output_paths[0]}"
        if action == 'pipeline':
            if output_paths:
                return f"流水线处理完成，manifest：{output_paths[-1]}"
            return f"流水线处理完成，状态：{status}"
        if action in ('asr', 'ocr', 'subtitle') and output_paths:
            return f"已生成字幕：{output_paths[0]}"
        if action == 'caption_segment' and output_paths:
            return f"已完成字幕分句：{output_paths[0]}"
        if action == 'audio_info':
            return "已获取音频信息。"
        if action == 'info':
            return "已获取媒体信息。"
        return f"处理完成，状态：{status}"
    return f"没有处理成功：{result.get('message', '未知错误')}"


def _infer_error_code(action: str, result: dict) -> str:
    if result.get('code'):
        return result['code']

    status = result.get('status')
    if status in ('success', 'partial', 'skipped'):
        return 'ok'

    message = str(result.get('message') or result.get('reply') or '')
    lowered = message.lower()
    if 'missing video_url/url/source' in lowered or 'missing source' in lowered:
        return 'missing_source'
    if 'missing steps' in lowered:
        return 'missing_steps'
    if 'missing captions' in lowered or 'caption_path' in lowered:
        return 'missing_captions'
    if 'unsupported pipeline action' in lowered or 'unsupported action' in lowered:
        return 'unsupported_action'
    if 'step requires' in lowered or 'step must' in lowered:
        return 'invalid_step'
    if 'overwrite=false' in lowered or '输出文件已存在' in message:
        return 'output_exists'
    if 'media_roots' in message or '路径穿越' in message or '禁止访问' in message or '超出允许' in message:
        return 'source_not_allowed'
    if 'ffmpeg' in lowered or 'ffprobe' in lowered or '返回码' in message:
        return 'ffmpeg_failed'
    if 'paddleocr' in lowered or result.get('action') == 'ocr':
        return 'missing_ocr_dependency'
    if 'faster-whisper' in lowered or result.get('action') == 'asr':
        return 'missing_asr_dependency'
    if action == 'chat' and not result.get('result'):
        return 'parse_failed'
    return 'error'


def _hint_for_code(code: str) -> str:
    hints = {
        'ok': '处理完成。',
        'missing_source': '请传入 video_url、url 或 source。',
        'missing_steps': 'pipeline 必须显式传入 steps 数组。',
        'missing_captions': '请传入 captions 数组，或传入 caption_path 指向已有字幕 JSON。',
        'unsupported_action': '请检查 action 名称是否在当前版本支持列表中。',
        'invalid_step': 'pipeline step 必须包含 id、action、enabled，且 enabled 为布尔值。',
        'output_exists': '如需覆盖已有文件，请传入 overwrite=true，或更换输出路径。',
        'source_not_allowed': '请确认本地文件位于当前工作目录或 media_roots 白名单内。',
        'ffmpeg_failed': '请确认 ffmpeg/ffprobe 已安装，且输入媒体文件可正常读取。',
        'missing_asr_dependency': '请运行 pip install -r requirements.txt 安装 faster-whisper 相关依赖。',
        'missing_ocr_dependency': '请运行 pip install -r requirements.txt 安装 paddleocr 相关依赖。',
        'parse_failed': '可以这样说：将 "sample.mp4" 提取音频；或传入明确的 pipeline JSON。',
        'error': '请查看 message 字段获取具体原因。',
    }
    return hints.get(code, hints['error'])


def _finalize_action_result(action: str, result: dict) -> dict:
    if not isinstance(result, dict):
        result = {'status': 'error', 'message': f'Invalid handler result for {action}'}
    result.setdefault('status', 'error')

    code = _infer_error_code(action, result)
    result.setdefault('code', code)
    result.setdefault('hint', _hint_for_code(code))
    if 'reply' not in result:
        result['reply'] = _chat_reply(action, result, collect_output_paths(result))
    return result


def _with_action_protocol(action: str, handler):
    def wrapped(params: dict) -> dict:
        try:
            return _finalize_action_result(action, handler(params))
        except Exception as e:
            return _finalize_action_result(action, {'status': 'error', 'message': str(e)})
    wrapped.__name__ = getattr(handler, '__name__', f'handle_{action}')
    wrapped.__doc__ = getattr(handler, '__doc__', None)
    return wrapped


def _apply_chat_output_defaults(action: str, params: dict) -> dict:
    output_dir = params.pop('output_dir', None)
    if not output_dir:
        return params
    name = params.get('name') or get_media_source_name(get_input_source(params) or '', fallback='media')
    if action == 'audio' and not params.get('output_path'):
        audio_format = params.get('format', 'mp3')
        params['output_path'] = str(Path(output_dir) / f"{name}.{audio_format}")
    elif action == 'thumbnail' and not params.get('save_path'):
        params['save_path'] = str(Path(output_dir) / f"{name}.jpg")
    elif action == 'compress' and not params.get('output_path'):
        params['output_path'] = str(Path(output_dir) / f"compressed_{name}.mp4")
    elif action in ('asr', 'ocr', 'subtitle') and not params.get('output_path'):
        params['output_path'] = str(Path(output_dir) / f"{name}.captions.json")
    elif action == 'caption_segment' and not params.get('output_path'):
        params['output_path'] = str(Path(output_dir) / f"{name}.segmented.captions.json")
    else:
        params['output_dir'] = output_dir
    return params


CHAT_AUTO_ASYNC_ACTIONS = {
    'audio',
    'compress',
    'asr',
    'ocr',
    'subtitle',
    'caption_segment',
    'batch',
    'pipeline',
}


def _chat_parse_error(parsed: dict) -> dict:
    return {
        'status': 'error',
        'reply': '我没识别出要执行的媒体操作，可以这样说：将 "sample.mp4" 提取音频',
        'intent': parsed.get('intent'),
        'action': parsed.get('action'),
        'params': parsed.get('params', {}),
        'result': None,
        'output_paths': [],
    }


def _prepare_chat_call(params: dict, action_handlers: dict = None) -> dict:
    action_handlers = action_handlers or ACTIONS
    message = params.get('message') or params.get('text')
    parsed = parse_media_intent(message)
    if parsed.get('missing_fields'):
        return _chat_parse_error(parsed)

    action = parsed.get('action')
    handler = action_handlers.get(action)
    if action == 'chat' or handler is None:
        return _chat_parse_error(parsed)

    call_params = dict(parsed.get('params') or {})
    passthrough_keys = (
        'media_roots', 'overwrite', 'output_dir', 'output_path', 'save_path',
        'format', 'bitrate', 'sample_rate', 'channels', 'target_ratio',
        'adaptive', 'crf', 'preset', 'mode', 'language', 'model_size',
        'sample_interval_sec', 'crop_bottom_ratio',
        'caption_path', 'captions', 'max_chars', 'protected_terms',
        'protected_terms_path', 'auto_protect_ascii'
    )
    for key in passthrough_keys:
        if key in params and key not in call_params:
            call_params[key] = params[key]
    if action != 'pipeline':
        call_params = _apply_chat_output_defaults(action, call_params)

    return {
        'status': 'success',
        'message': message,
        'parsed': parsed,
        'intent': parsed.get('intent'),
        'action': action,
        'handler': handler,
        'params': call_params,
    }


def _chat_async_mode(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered == 'auto':
            return 'auto'
    return None


def _chat_should_run_async(action: str, mode) -> bool:
    if mode is True:
        return True
    if mode == 'auto':
        return action in CHAT_AUTO_ASYNC_ACTIONS
    return False


def _chat_wait_timeout(params: dict):
    if 'wait_timeout_sec' not in params or params.get('wait_timeout_sec') is None:
        return 0.0, None
    value = params.get('wait_timeout_sec')
    if isinstance(value, bool):
        return None, protocol_error('invalid_wait_timeout', 'wait_timeout_sec must be a number between 0 and 30')
    try:
        timeout = float(value)
    except (TypeError, ValueError):
        return None, protocol_error('invalid_wait_timeout', 'wait_timeout_sec must be a number between 0 and 30')
    if timeout < 0 or timeout > 30:
        return None, protocol_error('invalid_wait_timeout', 'wait_timeout_sec must be a number between 0 and 30')
    return timeout, None


def _chat_job_response(queued: dict, prepared: dict, job: dict = None) -> dict:
    data = job or queued
    response = {
        'status': data.get('status', queued.get('status')),
        'code': data.get('code', queued.get('code', 'ok')),
        'reply': data.get('reply', queued.get('reply')),
        'hint': data.get('hint', queued.get('hint', '可通过 poll_url 查询任务状态。')),
        'intent': prepared.get('intent'),
        'action': prepared.get('action'),
        'params': prepared.get('params'),
        'job_id': queued.get('job_id'),
        'job_path': queued.get('job_path'),
        'poll_url': queued.get('poll_url'),
        'result': data.get('result'),
        'output_paths': data.get('output_paths', []),
        'error': data.get('error'),
    }
    return response


def _submit_prepared_chat_job(params: dict, prepared: dict, job_manager: JobManager) -> dict:
    action = prepared['action']
    call_params = prepared['params']
    timeout, timeout_error = _chat_wait_timeout(params)
    if timeout_error:
        return timeout_error

    metadata = {
        'created_by': 'chat',
        'intent': prepared.get('intent'),
        'source': get_input_source(call_params),
        'message': prepared.get('message'),
    }
    queued = job_manager.submit(action, call_params, metadata=metadata)
    if queued.get('status') != 'queued':
        return queued

    if timeout > 0:
        job = job_manager.wait_for_job(queued['job_id'], timeout=timeout)
        if job.get('status') in ('success', 'partial', 'skipped', 'error', 'running'):
            return _chat_job_response(queued, prepared, job=job)

    return _chat_job_response(queued, prepared)


def _chat_job_http_status(result: dict) -> int:
    if result.get('status') in ('queued', 'running'):
        return 202
    if result.get('code') in ('invalid_async_mode', 'invalid_wait_timeout', 'invalid_params', 'invalid_json'):
        return 400
    return 200


def submit_chat_job(params: dict, job_manager: JobManager, action_handlers: dict = None) -> dict:
    prepared = _prepare_chat_call(params, action_handlers=action_handlers)
    if prepared.get('status') != 'success':
        return prepared
    return _submit_prepared_chat_job(params, prepared, job_manager)


def _run_prepared_chat_call(prepared: dict) -> dict:
    action = prepared['action']
    handler = prepared['handler']
    call_params = prepared['params']

    try:
        result = handler(call_params)
    except Exception as e:
        result = {'status': 'error', 'message': str(e)}

    output_paths = collect_output_paths(result)
    return {
        'status': result.get('status', 'error'),
        'reply': _chat_reply(action, result, output_paths),
        'intent': prepared.get('intent'),
        'action': action,
        'params': call_params,
        'result': result,
        'output_paths': output_paths,
    }


def handle_chat(params: dict) -> dict:
    prepared = _prepare_chat_call(params)
    if prepared.get('status') != 'success':
        return prepared
    return _run_prepared_chat_call(prepared)


handle_compress = _with_action_protocol('compress', handle_compress)
handle_thumbnail = _with_action_protocol('thumbnail', handle_thumbnail)
handle_audio = _with_action_protocol('audio', handle_audio)
handle_audio_batch = _with_action_protocol('audio_batch', handle_audio_batch)
handle_audio_info = _with_action_protocol('audio_info', handle_audio_info)
handle_batch = _with_action_protocol('batch', handle_batch)
handle_info = _with_action_protocol('info', handle_info)
handle_subtitle = _with_action_protocol('subtitle', handle_subtitle)
handle_caption_segment = _with_action_protocol('caption_segment', handle_caption_segment)
handle_asr = _with_action_protocol('asr', handle_asr)
handle_ocr = _with_action_protocol('ocr', handle_ocr)
handle_pipeline = _with_action_protocol('pipeline', handle_pipeline)
handle_chat = _with_action_protocol('chat', handle_chat)

PIPELINE_STEP_HANDLERS.update({
    'info': handle_info,
    'thumbnail': handle_thumbnail,
    'audio': handle_audio,
    'compress': handle_compress,
    'audio_info': handle_audio_info,
    'asr': handle_asr,
    'ocr': handle_ocr,
    'subtitle': handle_subtitle,
    'caption_segment': handle_caption_segment,
})


# Action 映射
ACTIONS = {
    'compress': handle_compress,
    'thumbnail': handle_thumbnail,
    'audio': handle_audio,
    'audio_batch': handle_audio_batch,
    'audio_info': handle_audio_info,
    'asr': handle_asr,
    'ocr': handle_ocr,
    'subtitle': handle_subtitle,
    'caption_segment': handle_caption_segment,
    'batch': handle_batch,
    'info': handle_info,
    'pipeline': handle_pipeline,
    'chat': handle_chat
}


def run_cli():
    """命令行模式"""
    parser = argparse.ArgumentParser(description='Video Streaming Skill')
    parser.add_argument('--input', '-i', required=True, help='Input JSON string or file path')
    parser.add_argument('--action', '-a', choices=ACTIONS.keys(), help='Action to perform')
    args = parser.parse_args()
    
    try:
        try:
            input_is_file = Path(args.input).exists()
        except OSError:
            input_is_file = False
        if input_is_file:
            with open(args.input, 'r') as f:
                params = json.load(f)
        else:
            params = json.loads(args.input)
    except json.JSONDecodeError:
        params = {'action': args.action} if args.action else {}
        for pair in args.input.split():
            if '=' in pair:
                k, v = pair.split('=', 1)
                params[k] = v
    
    action = args.action or params.get('action')
    
    if not action or action not in ACTIONS:
        print(json.dumps({'status': 'error', 'message': f'Invalid action: {action}'}))
        sys.exit(1)
    
    result = ACTIONS[action](params)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def create_app(action_handlers: dict = None, job_manager: JobManager = None):
    from flask import Flask, request, jsonify
    try:
        from flask_cors import CORS
    except ImportError:
        CORS = lambda app: app

    action_handlers = action_handlers or ACTIONS
    job_manager = job_manager or JobManager(action_handlers)
    try:
        job_manager.cleanup_jobs(retention_days=7, max_jobs=200)
    except Exception as e:
        logger.warning(f"Job cleanup failed: {e}")

    app = Flask(__name__)
    CORS(app)

    try:
        check_media_binaries('ffmpeg', 'ffprobe')
        media_dependencies = {'status': 'ok'}
    except RuntimeError as e:
        logger.warning(str(e))
        media_dependencies = {'status': 'error', 'message': str(e)}

    def json_body():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return None, (jsonify(protocol_error('invalid_json', 'No JSON body')), 400)
        return data, None

    def action_route(action_name: str):
        def route():
            data, error_response = json_body()
            if error_response:
                return error_response
            if action_name == 'chat':
                async_mode = _chat_async_mode(data.get('async', False))
                if async_mode is None:
                    return jsonify(protocol_error('invalid_async_mode', 'async must be false, true, or "auto"')), 400
                timeout, timeout_error = _chat_wait_timeout(data)
                if timeout_error:
                    return jsonify(timeout_error), 400
                prepared = _prepare_chat_call(data, action_handlers=action_handlers)
                if prepared.get('status') != 'success':
                    return jsonify(_finalize_action_result('chat', prepared))
                if _chat_should_run_async(prepared.get('action'), async_mode):
                    result = _finalize_action_result(
                        'chat',
                        _submit_prepared_chat_job(data, prepared, job_manager),
                    )
                    return jsonify(result), _chat_job_http_status(result)
                return jsonify(_finalize_action_result('chat', _run_prepared_chat_call(prepared)))
            return jsonify(action_handlers[action_name](data))
        route.__name__ = f'route_{action_name}'
        return route

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            'status': 'ok',
            'skill': 'video-streaming-toolkit',
            'media_dependencies': media_dependencies
        })

    @app.route('/skill/jobs', methods=['POST', 'GET'])
    def jobs():
        if request.method == 'POST':
            data, error_response = json_body()
            if error_response:
                return error_response
            if 'params' not in data or data.get('params') is None:
                params = {}
            else:
                params = data.get('params')
                if not isinstance(params, dict):
                    return jsonify(protocol_error('invalid_params', 'params must be an object')), 400
            metadata = {
                'created_by': 'jobs',
                'source': get_input_source(params),
            }
            result = job_manager.submit(data.get('action'), params, metadata=metadata)
            return jsonify(result), 202 if result.get('status') == 'queued' else 400

        result = job_manager.list_jobs(
            status=request.args.get('status'),
            limit=request.args.get('limit', 50),
        )
        return jsonify(result)

    @app.route('/skill/jobs/<job_id>', methods=['GET'])
    def job_detail(job_id):
        result = job_manager.get_job(job_id)
        return jsonify(result), 200 if result.get('code') not in ('invalid_job_id', 'job_not_found') else 404

    for action_name in action_handlers:
        app.add_url_rule(
            f'/skill/{action_name}',
            endpoint=f'skill_{action_name}',
            view_func=action_route(action_name),
            methods=['POST'],
        )

    return app


def run_http_server(host='127.0.0.1', port=8080):
    """HTTP 服务模式"""
    try:
        app = create_app()
        logger.info(f"Starting HTTP server on {host}:{port}")
        app.run(host=host, port=port, threaded=True)
    except ImportError:
        logger.error("Flask not installed. Run: pip install flask flask-cors")
        sys.exit(1)


if __name__ == '__main__':
    if '--serve' in sys.argv or '-s' in sys.argv:
        argv = sys.argv[1:]
        host = '127.0.0.1'
        port = 8080
        i = 0
        while i < len(argv):
            if argv[i] == '--host' and i + 1 < len(argv):
                host = argv[i + 1]
                i += 2
            elif argv[i] == '--port' and i + 1 < len(argv):
                port = int(argv[i + 1])
                i += 2
            else:
                i += 1
        run_http_server(host=host, port=port)
    else:
        run_cli()
