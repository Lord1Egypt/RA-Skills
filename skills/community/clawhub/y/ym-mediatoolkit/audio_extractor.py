"""
流式音频提取 - 从远程视频直接提取音频，无需下载完整视频
支持格式: MP3, WAV, AAC, M4A
"""

import subprocess
import requests
import logging
from pathlib import Path

from utils import (
    check_media_binaries,
    get_media_source_name,
    prepare_output_path,
    sanitize_output_path,
    validate_media_source,
    validate_video_url,
)

logger = logging.getLogger(__name__)
FFMPEG_TIMEOUT_SECONDS = 300


def get_remote_file_size(url: str) -> int:
    try:
        validate_video_url(url)
    except ValueError:
        return 0
    try:
        response = requests.head(url, timeout=10)
        if 'content-length' in response.headers:
            return int(response.headers['content-length'])
    except Exception as e:
        logger.warning(f"获取文件大小失败: {e}")
    return 0


def extract_audio_streaming(
    video_url: str,
    output_path: str = None,
    audio_format: str = 'mp3',  # mp3, wav, aac, m4a
    audio_bitrate: str = '128k',  # 128k, 192k, 320k
    sample_rate: int = 44100,  # 44100, 48000
    channels: int = 2,  # 1=mono, 2=stereo
    start_time: float = None,  # 开始时间（秒）
    duration: float = None,  # 持续时间（秒）
    overwrite: bool = True,
    media_roots=None
) -> dict:
    """
    流式提取音频 - ffmpeg 直接从 URL 提取，无需下载视频
    
    Args:
        video_url: 视频 URL
        output_path: 输出路径（可选）
        audio_format: 音频格式 (mp3, wav, aac, m4a)
        audio_bitrate: 音频比特率 (128k, 192k, 320k)
        sample_rate: 采样率 (44100, 48000)
        channels: 声道数 (1=单声道, 2=立体声)
        start_time: 开始时间（秒），提取片段
        duration: 持续时间（秒）
    
    Returns:
        {
            'status': 'success',
            'output_path': str,
            'format': str,
            'size_mb': float,
            'duration_sec': float,
            'streaming': True
        }
    """
    try:
        video_url = validate_media_source(video_url, media_roots=media_roots)
        check_media_binaries('ffmpeg')
        video_name = get_media_source_name(video_url, fallback='audio')
        output_path = prepare_output_path(
            output_path=output_path,
            default_dir='output/audio',
            default_name=video_name,
            extension=f'.{audio_format}',
            overwrite=overwrite
        )
    except (ValueError, RuntimeError) as e:
        return {'status': 'error', 'message': str(e)}
    
    cmd = ['ffmpeg', '-i', video_url]
    
    # 片段提取参数
    if start_time is not None:
        cmd.extend(['-ss', str(start_time)])
    if duration is not None:
        cmd.extend(['-t', str(duration)])
    
    # 音频参数
    if audio_format == 'mp3':
        cmd.extend([
            '-c:a', 'libmp3lame',
            '-b:a', audio_bitrate,
            '-ar', str(sample_rate),
            '-ac', str(channels)
        ])
    elif audio_format == 'wav':
        cmd.extend([
            '-c:a', 'pcm_s16le',  # WAV 无损格式
            '-ar', str(sample_rate),
            '-ac', str(channels)
        ])
    elif audio_format == 'aac':
        cmd.extend([
            '-c:a', 'aac',
            '-b:a', audio_bitrate,
            '-ar', str(sample_rate),
            '-ac', str(channels)
        ])
    elif audio_format == 'm4a':
        cmd.extend([
            '-c:a', 'aac',
            '-b:a', audio_bitrate,
            '-ar', str(sample_rate),
            '-ac', str(channels),
            '-movflags', '+faststart'
        ])
    else:
        return {'status': 'error', 'message': f'Unsupported format: {audio_format}'}
    
    # 输出参数
    cmd.extend(['-y' if overwrite else '-n', output_path])
    
    logger.info(f"开始流式音频提取: {video_url[:80]}...")
    logger.info(f"输出格式: {audio_format}, 比特率: {audio_bitrate}, 采样率: {sample_rate}")
    logger.info(f"命令: {' '.join(cmd[:5])}...")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=FFMPEG_TIMEOUT_SECONDS
        )
        
        # 解析 ffmpeg 输出摘要
        last_progress = ""
        duration_sec = 0
        
        for line in result.stderr.splitlines():
            if 'Duration:' in line and duration_sec == 0:
                # 解析总时长
                import re
                match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})', line)
                if match:
                    h, m, s = match.groups()
                    duration_sec = int(h) * 3600 + int(m) * 60 + float(s)
                    logger.info(f"视频总时长: {duration_sec:.2f}秒")
            
            if 'size=' in line and 'time=' in line:
                progress = line.strip()
                if progress != last_progress:
                    logger.info(f"进度: {progress}")
                    last_progress = progress

        if result.returncode != 0:
            return {
                'status': 'error',
                'message': f'ffmpeg 错误，返回码: {result.returncode}'
            }
        
        # 检查输出文件
        if not Path(output_path).exists():
            return {'status': 'error', 'message': '输出文件未生成'}
        
        file_size = Path(output_path).stat().st_size
        
        # 获取提取的音频时长
        audio_duration = duration_sec if duration_sec > 0 else None
        
        logger.info(f"音频提取完成: {file_size/(1024*1024):.2f}MB")
        
        return {
            'status': 'success',
            'output_path': output_path,
            'format': audio_format,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'duration_sec': audio_duration,
            'bitrate': audio_bitrate,
            'sample_rate': sample_rate,
            'channels': channels,
            'streaming': True
        }
        
    except subprocess.TimeoutExpired:
        return {'status': 'error', 'message': f'音频提取超时（{FFMPEG_TIMEOUT_SECONDS}秒）'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def extract_audio_batch(
    videos: list,
    output_dir: str = 'output/audio',
    audio_format: str = 'mp3',
    audio_bitrate: str = '128k',
    sample_rate: int = 44100,
    overwrite: bool = True,
    media_roots=None
) -> dict:
    """
    批量提取音频
    
    Args:
        videos: 视频列表 [{'url': 'https://...', 'name': 'video1'}, ...]
        output_dir: 输出目录
        audio_format: 音频格式
        audio_bitrate: 比特率
        sample_rate: 采样率
    
    Returns:
        批量结果
    """
    import os
    output_dir = sanitize_output_path(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    success_count = 0
    
    for i, video in enumerate(videos):
        url = video.get('video_url') or video.get('url') or video.get('source')
        name = video.get('name', f'audio_{i+1}')
        
        if not url:
            results.append({'name': name, 'status': 'error', 'message': 'Missing video_url/url/source'})
            continue
        
        output_path = video.get('output_path') or os.path.join(output_dir, f"{name}.{audio_format}")
        
        logger.info(f"批量处理 [{i+1}/{len(videos)}]: {name}")
        
        result = extract_audio_streaming(
            video_url=url,
            output_path=output_path,
            audio_format=audio_format,
            audio_bitrate=audio_bitrate,
            sample_rate=sample_rate,
            overwrite=overwrite,
            media_roots=media_roots
        )
        
        result['name'] = name
        results.append(result)
        
        if result.get('status') == 'success':
            success_count += 1
    
    return {
        'status': 'success',
        'total': len(videos),
        'success': success_count,
        'failed': len(videos) - success_count,
        'results': results
    }


def get_audio_info(video_url: str, media_roots=None) -> dict:
    import re
    try:
        video_url = validate_media_source(video_url, media_roots=media_roots)
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    try:
        check_media_binaries('ffprobe')
    except RuntimeError as e:
        return {'status': 'error', 'message': str(e)}
    
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', video_url]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {'status': 'error', 'message': 'ffprobe failed'}
        
        import json
        data = json.loads(result.stdout)
        
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'audio':
                return {
                    'status': 'success',
                    'has_audio': True,
                    'audio_codec': stream.get('codec_name', 'unknown'),
                    'audio_bitrate': stream.get('bit_rate', 'unknown'),
                    'sample_rate': int(stream.get('sample_rate', 0)) if stream.get('sample_rate') else 0,
                    'channels': stream.get('channels', 0),
                    'language': stream.get('tags', {}).get('language', 'unknown')
                }
        
        return {'status': 'success', 'has_audio': False, 'message': 'No audio stream found'}
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
