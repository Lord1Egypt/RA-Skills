# -*- coding: utf-8 -*-
"""
STT Skill - 语音识别
自动识别语音消息并转为文字
"""
import os
import re
import subprocess
import asyncio
from pathlib import Path

# 尝试导入 faster_whisper
try:
    from faster_whisper import WhisperModel
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False

# 配置
FFMPEG_PATHS = [
    r'C:\ffmpeg\bin',
    r'C:\ffmpeg',
    r'C:\Program Files\ffmpeg\bin',
    r'C:\Program Files (x86)\ffmpeg\bin',
]
MODEL_SIZE = 'tiny'
LANGUAGE = 'zh'

# 全局模型缓存
_model = None


def find_ffmpeg():
    """查找 ffmpeg 路径"""
    for path in FFMPEG_PATHS:
        ffmpeg_exe = os.path.join(path, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_exe):
            return path
    return None


def get_model():
    """获取或加载 Whisper 模型"""
    global _model
    if _model is None:
        if not STT_AVAILABLE:
            raise RuntimeError('faster-whisper 未安装: pip install faster-whisper')
        print('[STT] 加载 Whisper 模型...')
        _model = WhisperModel(MODEL_SIZE, device='cpu', compute_type='int8')
        print('[STT] 模型加载完成')
    return _model


def convert_to_wav(input_path: str, output_path: str = None) -> str:
    """转换音频为 wav 格式"""
    if output_path is None:
        output_path = input_path.replace('.ogg', '.wav').replace('.mp3', '.wav')
    
    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        raise RuntimeError('未找到 ffmpeg，请安装 ffmpeg')
    
    env = os.environ.copy()
    env['PATH'] = ffmpeg_path + ';' + env.get('PATH', '')
    
    result = subprocess.run(
        ['ffmpeg', '-i', input_path, '-ar', '16000', '-ac', '1', output_path, '-y'],
        capture_output=True,
        env=env
    )
    
    if result.returncode != 0:
        raise RuntimeError(f'音频转换失败: {result.stderr.decode()}')
    
    return output_path


def recognize(audio_path: str, language: str = LANGUAGE) -> str:
    """
    识别语音文件
    
    Args:
        audio_path: 音频文件路径
        language: 语言代码
    
    Returns:
        识别出的文字
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f'文件不存在: {audio_path}')
    
    # 转换格式
    ext = os.path.splitext(audio_path)[1].lower()
    if ext in ['.ogg', '.mp3', '.m4a']:
        wav_path = audio_path.replace(ext, '.wav')
        convert_to_wav(audio_path, wav_path)
    else:
        wav_path = audio_path
    
    # 识别
    model = get_model()
    segments, info = model.transcribe(wav_path, language=language)
    
    text = ' '.join([s.text.strip() for s in segments])
    return text


def find_voice_files(media_dir: str = None):
    """查找最新的语音文件"""
    if media_dir is None:
        # 默认的飞书语音目录
        media_dir = os.path.join(os.path.expanduser('~'), '.openclaw', 'media', 'inbound')
    
    if not os.path.exists(media_dir):
        return None
    
    # 找最新的 ogg 文件
    ogg_files = list(Path(media_dir).glob('*.ogg'))
    if not ogg_files:
        return None
    
    # 按修改时间排序，返回最新的
    latest = max(ogg_files, key=lambda f: f.stat().st_mtime)
    return str(latest)


async def handle_voice_message(voice_file: str = None) -> str:
    """
    处理语音消息
    
    Args:
        voice_file: 语音文件路径，如果为 None 则自动查找最新的
    
    Returns:
        识别出的文字
    """
    if voice_file is None:
        voice_file = find_voice_files()
    
    if voice_file is None:
        return None
    
    try:
        text = recognize(voice_file)
        return text
    except Exception as e:
        print(f'[STT] 识别失败: {e}')
        return None


# Skill 入口点 - 被 OpenClaw 调用
async def main(context):
    """
    Skill 主入口
    
    Args:
        context: OpenClaw 上下文，包含消息、附件等信息
    
    Returns:
        处理结果
    """
    # 检查依赖
    if not STT_AVAILABLE:
        return {
            'error': 'faster-whisper 未安装',
            'hint': '运行: pip install faster-whisper pydub'
        }
    
    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        return {
            'error': '未找到 ffmpeg',
            'hint': '请安装 ffmpeg 并确保在 PATH 中'
        }
    
    # 检查是否有语音附件
    attachments = context.get('attachments', [])
    
    voice_file = None
    for att in attachments:
        if att.get('mime_type', '').startswith('audio/') or att.get('filename', '').endswith('.ogg'):
            voice_file = att.get('path') or att.get('filename')
            break
    
    # 如果没有附件，尝试查找最新的语音文件
    if not voice_file:
        voice_file = find_voice_files()
    
    if not voice_file:
        return {'error': '未找到语音文件'}
    
    # 识别
    try:
        text = recognize(voice_file)
        return {
            'success': True,
            'text': text,
            'file': voice_file
        }
    except Exception as e:
        return {
            'error': str(e)
        }


if __name__ == '__main__':
    # 测试
    import sys
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        result = recognize(audio_file)
        print(f'识别结果: {result}')
    else:
        # 测试找最新文件
        latest = find_voice_files()
        if latest:
            print(f'最新语音文件: {latest}')
            result = recognize(latest)
            print(f'识别结果: {result}')
        else:
            print('未找到语音文件')