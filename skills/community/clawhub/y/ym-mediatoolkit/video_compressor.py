"""
流式视频压缩 - 无需下载完整文件
"""
import subprocess
import requests
import logging
from pathlib import Path

from utils import (
    check_media_binaries,
    get_media_source_name,
    is_remote_source,
    prepare_output_path,
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

def get_source_file_size(source: str) -> int:
    if is_remote_source(source):
        return get_remote_file_size(source)
    try:
        return Path(source).stat().st_size
    except OSError:
        return 0


def compress_video_streaming(
    video_url: str,
    output_path: str = None,
    target_ratio: float = 0.1,
    crf: int = 24,
    preset: str = 'veryfast',
    overwrite: bool = True,
    media_roots=None
) -> dict:
    """
    流式压缩视频 - ffmpeg 直接处理 URL
    
    Args:
        video_url: 视频 URL
        output_path: 输出路径（可选）
        target_ratio: 目标体积比例（用于检查，不自动重试）
        crf: CRF值（18-28，越大体积越小）
        preset: 编码预设（ultrafast/veryfast/fast/medium/slow）
    
    Returns:
        {'status': 'success', 'output_path': str, 'original_size_mb': float, 
         'new_size_mb': float, 'ratio': float}
    """
    try:
        video_url = validate_media_source(video_url, media_roots=media_roots)
        check_media_binaries('ffmpeg')
        video_name = get_media_source_name(video_url)
        output_path = prepare_output_path(
            output_path=output_path,
            default_dir='output/videos',
            default_name=f"compressed_{video_name}",
            extension='.mp4',
            overwrite=overwrite
        )
    except (ValueError, RuntimeError) as e:
        return {'status': 'error', 'message': str(e)}
    
    original_size = get_source_file_size(video_url)
    
    # ffmpeg 流式压缩命令
    cmd = [
        'ffmpeg',
        '-i', video_url,           # 直接输入 URL
        '-c:v', 'libx264',
        '-preset', preset,
        '-crf', str(crf),
        '-g', '30',
        '-keyint_min', '30',
        '-sc_threshold', '0',
        '-bf', '0',
        '-refs', '1',
        '-vsync', 'cfr',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',
        '-y' if overwrite else '-n',
        output_path
    ]
    
    logger.info(f"开始流式压缩: {video_url[:80]}...")
    logger.info(f"输出文件: {output_path}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=FFMPEG_TIMEOUT_SECONDS
        )

        # 记录 ffmpeg 进度摘要
        last_progress = ""
        for line in result.stderr.splitlines():
            if 'frame=' in line and 'speed=' in line:
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
        
        new_size = Path(output_path).stat().st_size
        actual_ratio = new_size / original_size if original_size > 0 else 0
        
        logger.info(f"压缩完成: {original_size/(1024*1024):.2f}MB -> {new_size/(1024*1024):.2f}MB, 比例: {actual_ratio:.2f}")
        
        return {
            'status': 'success',
            'output_path': output_path,
            'original_size_mb': round(original_size / (1024 * 1024), 2) if original_size else 0,
            'new_size_mb': round(new_size / (1024 * 1024), 2),
            'ratio': round(actual_ratio, 3),
            'crf_used': crf,
            'streaming': True
        }
        
    except subprocess.TimeoutExpired:
        return {'status': 'error', 'message': f'压缩超时（{FFMPEG_TIMEOUT_SECONDS}秒）'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def compress_with_adaptive_crf(
    video_url: str,
    output_path: str = None,
    target_ratio: float = 0.1,
    max_attempts: int = 3,
    overwrite: bool = True,
    media_roots=None
) -> dict:
    """
    自适应 CRF 压缩 - 自动调整参数直到达到目标比例
    """
    crf_values = [24, 26, 28, 30]  # 依次尝试
    best_result = None
    final_output_path = output_path

    if final_output_path is None:
        safe_source = validate_media_source(video_url, media_roots=media_roots)
        video_name = get_media_source_name(safe_source)
        final_output_path = str(Path('output/videos') / f"compressed_{video_name}.mp4")
    
    for i, crf in enumerate(crf_values[:max_attempts]):
        logger.info(f"尝试 {i+1}/{max_attempts}: CRF={crf}")

        attempt_output_path = final_output_path
        if i > 0:
            attempt_path = Path(final_output_path)
            attempt_output_path = str(
                attempt_path.with_name(f"{attempt_path.stem}.try{i+1}{attempt_path.suffix}")
            )
        
        result = compress_video_streaming(
            video_url=video_url,
            output_path=attempt_output_path,
            target_ratio=target_ratio,
            crf=crf,
            overwrite=overwrite,
            media_roots=media_roots
        )
        
        if result['status'] != 'success':
            continue
        
        if result['ratio'] <= target_ratio:
            # 达到目标，移动文件到最终位置
            if i > 0 and result['output_path'] != final_output_path:
                import shutil
                shutil.move(result['output_path'], final_output_path)
                result['output_path'] = final_output_path
            return result
        
        best_result = result
    
    # 未达到目标，返回最好的结果
    if best_result:
        logger.warning(f"未达到目标比例 {target_ratio}，最佳比例: {best_result['ratio']}")
        if best_result['output_path'] != final_output_path:
            import shutil
            shutil.move(best_result['output_path'], final_output_path)
            best_result['output_path'] = final_output_path
        return best_result
    
    return {'status': 'error', 'message': '所有压缩尝试均失败'}
