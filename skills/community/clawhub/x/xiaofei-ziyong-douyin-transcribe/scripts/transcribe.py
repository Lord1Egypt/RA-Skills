#!/usr/bin/env python3
"""
Douyin Video Transcribe - 全自动管道
用法: python3 transcribe.py --url "https://v.douyin.com/xxxxx"
"""

import subprocess
import os
import sys
import json
import time
import argparse
import re


def e(cmd, timeout=120):
    """执行shell命令，返回 (returncode, stdout, stderr)"""
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def get_video_url(douyin_url):
    """通过Node.js脚本获取视频直链"""
    print("  使用 puppeteer-core 拦截 hellotik 请求...", flush=True)
    
    js_path = os.path.join(os.path.dirname(__file__), 'get_video_url.js')
    if not os.path.exists(js_path):
        return None, None
    
    rc, out, err = e(
        f'DOUYIN_URL="{douyin_url}" node {js_path} 2>&1',
        timeout=90
    )
    
    # 从stdout解析JSON
    for line in out.split('\n'):
        if line.startswith('RESULT_JSON:'):
            try:
                data = json.loads(line[len('RESULT_JSON:'):])
                return data.get('videoUrl'), data.get('coverUrl')
            except:
                pass
    
    return None, None


def download_file(url, path):
    """下载文件"""
    if not url:
        return False
    url = url.strip().strip('"').strip("'")
    print(f"  下载: {url[:80]}...", flush=True)
    rc, out, err = e(f'curl -L --max-time 120 -o "{path}" "{url}" 2>&1')
    if os.path.exists(path):
        size = os.path.getsize(path)
        if size > 5000:
            print(f"  下载完成: {size//1024}KB", flush=True)
            return True
    return False


def extract_audio(video_path, audio_path):
    """ffmpeg提取音频"""
    print("  提取音频（WAV 16kHz单声道）...", flush=True)
    rc, out, err = e(
        f'ffmpeg -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_path}" -y 2>&1 | tail -5',
        timeout=300
    )
    ok = os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000
    if ok:
        print(f"  音频提取完成: {os.path.getsize(audio_path)//1024}KB", flush=True)
    return ok


def transcribe(audio_path):
    """使用coli进行语音转写"""
    print("  开始转写（sensevoice模型，约2-4分钟）...", flush=True)
    
    # 优先用coli CLI
    rc, out, err = e(f'coli asr --model sensevoice "{audio_path}" 2>&1', timeout=600)
    if rc == 0 and out.strip():
        return out.strip()
    
    # 备选：uv + faster-whisper
    print("  coli不可用，尝试faster-whisper...", flush=True)
    rc2, out2, err2 = e(
        f'uv run --with faster-whisper python3 -c "\n'
        'from faster_whisper import WhisperModel\n'
        'model = WhisperModel(\"small\", device=\"cpu\", compute_type=\"int8\")\n'
        'segs, _ = model.transcribe(\"{audio_path}\", beam_size=5)\n'
        'for s in segs: print(s.text, end=\"\", flush=True)\n'
        'print()\n" 2>&1',
        timeout=600
    )
    if rc2 == 0 and out2.strip():
        return out2.strip()
    
    print(f"  转写失败: {err[-300:]}", flush=True)
    return None


def main():
    p = argparse.ArgumentParser(description='抖音视频语音转写')
    p.add_argument('--url', '-u', required=True, help='抖音视频链接')
    p.add_argument('--output-dir', '-o', default='/tmp', help='临时文件目录')
    p.add_argument('--folder-token', '-f', default='', help='飞书云盘folder_token')
    p.add_argument('--space-id', '-s', default='', help='飞书知识库space_id')
    p.add_argument('--no-feishu', action='store_true', help='跳过飞书上传统步')
    p.add_argument('--cleanup', action='store_true', help='完成后删除临时文件')
    
    args = p.parse_args()
    
    out_dir = args.output_dir
    os.makedirs(out_dir, exist_ok=True)
    
    video_path = os.path.join(out_dir, 'douyin_video.mp4')
    audio_path = os.path.join(out_dir, 'douyin_audio.wav')
    cover_path = os.path.join(out_dir, 'douyin_cover.jpg')
    transcript_path = os.path.join(out_dir, 'transcript.txt')
    
    print("=" * 60, flush=True)
    print("抖音视频语音转写", flush=True)
    print(f"URL: {args.url}", flush=True)
    print("=" * 60, flush=True)
    
    # Step 1: 获取视频直链
    print("\n[Step 1] 获取视频直链...", flush=True)
    video_url, cover_url = get_video_url(args.url)
    
    if not video_url:
        print("ERROR: 无法获取视频直链", flush=True)
        sys.exit(1)
    
    print(f"  直链获取成功: {video_url[:100]}...", flush=True)
    
    # 下载封面
    if cover_url:
        print("\n[Step 2] 下载封面...", flush=True)
        download_file(cover_url, cover_path)
    
    # Step 2/3: 下载视频
    print("\n[Step 3] 下载视频...", flush=True)
    if not download_file(video_url, video_path):
        print("ERROR: 视频下载失败", flush=True)
        sys.exit(1)
    
    # Step 4: 提取音频
    print("\n[Step 4] 提取音频...", flush=True)
    if not extract_audio(video_path, audio_path):
        print("ERROR: 音频提取失败", flush=True)
        sys.exit(1)
    
    # Step 5: 转写
    print("\n[Step 5] 语音转写...", flush=True)
    transcript = transcribe(audio_path)
    if not transcript:
        print("ERROR: 转写失败", flush=True)
        sys.exit(1)
    
    # 保存转录
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcript)
    
    print("\n" + "=" * 60, flush=True)
    print("【转录结果】", flush=True)
    print("=" * 60, flush=True)
    print(transcript, flush=True)
    print("=" * 60, flush=True)
    print(f"\n转录文本已保存: {transcript_path}", flush=True)
    
    # Step 6: 飞书上传统步（可选）
    if not args.no_feishu and (args.folder_token or args.space_id):
        print("\n[Step 6] 上传到飞书...", flush=True)
        try:
            from feishu_upload import do_upload
            do_upload(
                video_path, audio_path, transcript, args.url,
                args.folder_token, args.space_id
            )
        except Exception as ex:
            print(f"  飞书上传统步跳过: {ex}", flush=True)
    
    # Step 7: 清理
    if args.cleanup:
        for p_ in [video_path, audio_path]:
            try: os.remove(p_)
            except: pass
        print("\n临时文件已清理")
    
    print("\n✅ 全部完成!", flush=True)


if __name__ == '__main__':
    main()
