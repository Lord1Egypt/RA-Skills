#!/usr/bin/env python3
"""
Video to Text - 视频转文字工具
支持本地处理和在线API
"""
import os
import sys
import argparse
import subprocess
import json

def extract_audio(video_path, output_path=None):
    """从视频提取音频"""
    if not output_path:
        output_path = video_path.rsplit('.', 1)[0] + '.wav'
    
    cmd = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', output_path, '-y']
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ 音频已提取: {output_path}")
        return output_path
    except subprocess.CalledProcessError:
        print("❌ ffmpeg 未安装，请先安装: sudo apt install ffmpeg")
        return None

def transcribe_with_local(video_path, model='base', language='zh'):
    """使用本地 Whisper 转写"""
    try:
        import whisper
    except ImportError:
        print("请安装 whisper: pip install openai-whisper")
        return None
    
    print(f"🔄 加载模型: {model}...")
    model = whisper.load_model(model)
    
    print("🔄 转写中...")
    result = model.transcribe(video_path, language=language)
    
    return result['text']

def transcribe_assemblyai(audio_path, api_key):
    """使用 AssemblyAI API"""
    import requests
    
    # 上传音频
    with open(audio_path, 'rb') as f:
        response = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers={'authorization': api_key},
            files={'file': f}
        )
    
    audio_url = response.json()['upload_url']
    
    # 转写
    response = requests.post(
        'https://api.assemblyai.com/v2/transcript',
        headers={'authorization': api_key},
        json={'audio_url': audio_url, 'language_code': 'zh'}
    )
    
    transcript_id = response.json()['id']
    
    # 等待结果
    import time
    while True:
        response = requests.get(
            f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
            headers={'authorization': api_key}
        )
        status = response.json()['status']
        
        if status == 'completed':
            return response.json()['text']
        elif status == 'error':
            return None
        time.sleep(3)

def cmd_convert(args):
    video_path = args.video
    
    if not os.path.exists(video_path):
        print(f"❌ 文件不存在: {video_path}")
        return
    
    output = args.output or video_path.rsplit('.', 1)[0] + '.txt'
    lang = args.lang or 'zh'
    
    # 提取音频
    audio_path = video_path.rsplit('.', 1)[0] + '.wav'
    print("🔄 提取音频...")
    extract_audio(video_path, audio_path)
    
    # 转写
    if args.api == 'assemblyai' and args.api_key:
        print("🔄 使用 AssemblyAI 转写...")
        text = transcribe_assemblyai(audio_path, args.api_key)
    else:
        print("🔄 使用本地 Whisper 转写...")
        text = transcribe_with_local(video_path, language=lang)
    
    if text:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✅ 已保存: {output}")
    else:
        print("❌ 转写失败")

def cmd_extract_audio(args):
    video_path = args.video
    output = args.output or video_path.rsplit('.', 1)[0] + '.wav'
    extract_audio(video_path, output)

def main():
    parser = argparse.ArgumentParser(description='Video to Text')
    subparsers = parser.add_subparsers()
    
    # convert
    p_conv = subparsers.add_parser('convert', help='视频转文字')
    p_conv.add_argument('video', help='视频文件路径')
    p_conv.add_argument('--lang', '-l', default='zh', help='语言: zh/en')
    p_conv.add_argument('--output', '-o', help='输出文件')
    p_conv.add_argument('--api', default='local', choices=['local', 'assemblyai'], help='转写方式')
    p_conv.add_argument('--api-key', help='API Key (AssemblyAI)')
    p_conv.set_defaults(func=cmd_convert)
    
    # extract-audio
    p_audio = subparsers.add_parser('extract-audio', help='提取音频')
    p_audio.add_argument('video', help='视频文件')
    p_audio.add_argument('--output', '-o', help='输出音频文件')
    p_audio.set_defaults(func=cmd_extract_audio)
    
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
