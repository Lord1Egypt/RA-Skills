#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
微信视频号直播回放下载技能 - V2 (Secure & Portable)
功能：
1. 根据视频号名称搜索用户，获取 username
2. 获取该用户的直播历史记录
3. 按指定日期筛选回放，下载视频文件
4. (可选) 使用 Whisper 转写直播稿
"""

import os
import sys
import json
import time
import tempfile
import argparse
import requests
from datetime import datetime
from pathlib import Path
import subprocess

# ==================== 配置区域 (V2 - 动态与安全) ====================

def find_openclaw_root():
    """健壮地向上查找 .openclaw 根目录。"""
    current_path = Path(__file__).resolve().parent
    for _ in range(5):
        if (current_path / 'config.json').exists() and (current_path / 'skills').is_dir():
            return current_path
        if current_path.parent == current_path:
            break
        current_path = current_path.parent
    home_path = Path.home() / '.openclaw'
    return home_path if home_path.exists() else None

OPENCLAW_ROOT = find_openclaw_root()

if not OPENCLAW_ROOT:
    print("致命错误：无法定位 .openclaw 根目录。", file=sys.stderr)
    sys.exit(1)

CONFIG_PATH = OPENCLAW_ROOT / 'config.json'
DEFAULT_OUTPUT_DIR = OPENCLAW_ROOT / "workspace" / "data"
REPLAY_INPUT_BASE = OPENCLAW_ROOT / "skills" / "live-replay-analyzer" / "input"

# 强制 UTF-8 输出
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1, closefd=False)
sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1, closefd=False)

WHISPER_MODEL = "base"
API_BASE = "https://api.tikhub.io/api/v1"
USER_SEARCH_URL = f"{API_BASE}/wechat_channels/fetch_user_search"
LIVE_HISTORY_URL = f"{API_BASE}/wechat_channels/fetch_live_history"

# ==================== 辅助函数 ====================

def get_config_value(key: str, default=None):
    """从 config.json 安全地读取配置值"""
    if not CONFIG_PATH.exists():
        return default
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
        return config.get(key, default)
    except (json.JSONDecodeError, IOError):
        return default

def get_tikhub_token():
    """从配置中安全地获取 TikHub Token"""
    token = get_config_value('tikhub_api_token', os.getenv('TIKHUB_TOKEN'))
    if not token:
        raise ValueError("错误：未在 config.json 或环境变量中配置 'tikhub_api_token'")
    return token

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def call_api(url, params, token):
    """调用 TikHub API，返回 JSON 响应"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url=url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_msg = f"API 请求失败：{e}"
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f"\n状态码：{e.response.status_code}"
            try:
                error_msg += f"\n响应内容：{e.response.text}"
            except:
                pass
        raise Exception(error_msg)

def download_file(url, filepath):
    """流式下载大文件"""
    try:
        with requests.get(url, stream=True, timeout=120) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded = 0
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = downloaded * 100 / total_size
                            print(f"\r下载进度：{percent:.1f}%", end='', file=sys.stderr)
            print(f"  下载完成：{filepath} ({downloaded/1024/1024:.1f} MB)", file=sys.stderr)
            return True
    except Exception as e:
        print(f"  下载失败：{e}", file=sys.stderr)
        return False

# ==================== 核心功能 ====================

def search_user(keywords, token):
    """根据关键词搜索视频号用户，返回第一个用户的完整信息"""
    params = {'keywords': keywords, 'page': 1}
    data = call_api(USER_SEARCH_URL, params, token)
    if data.get('code') != 200:
        raise Exception(f"搜索失败：{data.get('message', '未知错误')}")
    users = data.get('data', [])
    if not users:
        raise Exception(f"未找到用户：{keywords}")
    return users[0]

def get_live_history(username, token):
    """获取指定用户的直播历史记录"""
    params = {'username': username}
    data = call_api(LIVE_HISTORY_URL, params, token)
    if data.get('code') != 200:
        raise Exception(f"获取直播历史失败：{data.get('message', '未知错误')}")
    return data.get('data', {}).get('object', [])

def filter_replays_by_date(replays, target_date=None):
    """按日期筛选回放记录"""
    if not replays:
        return None, None
    sorted_replays = sorted(replays, key=lambda x: x.get('createtime', 0), reverse=True)
    if target_date is None:
        replay = sorted_replays[0]
        date_str = datetime.fromtimestamp(replay['createtime']).strftime('%Y-%m-%d')
        return replay, date_str
    try:
        target_dt = datetime.strptime(target_date, '%Y-%m-%d')
        target_start = int(target_dt.timestamp())
        target_end = target_start + 86400
    except ValueError:
        raise Exception(f"日期格式错误，应为 YYYY-MM-DD，如 2026-03-12")
    for replay in sorted_replays:
        ts = replay.get('createtime', 0)
        if target_start <= ts < target_end:
            return replay, target_date
    raise Exception(f"未找到 {target_date} 的直播回放")

def extract_video_url(replay):
    """从回放记录中提取可下载的视频 URL"""
    obj_desc = replay.get('object_desc', {})
    media_list = obj_desc.get('media', [])
    if not media_list:
        raise Exception("回放记录中无媒体信息")
    media = media_list[0]
    url = media.get('url')
    if not url:
        raise Exception("媒体 URL 不存在")
    return url

def extract_audio(video_path, audio_path):
    """使用 ffmpeg 从视频中提取音频为 MP3"""
    print(f"  输入视频：{video_path}", file=sys.stderr)
    print(f"  输出音频：{audio_path}", file=sys.stderr)
    cmd = ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame', '-y', audio_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if result.returncode != 0:
            if "ffmpeg: not found" in result.stderr or "不是内部或外部命令" in result.stderr:
                raise FileNotFoundError("错误：'ffmpeg' 未在系统 PATH 中找到。请安装 ffmpeg 并将其添加到环境变量中。")
            print(f"  ffmpeg 错误：{result.stderr}", file=sys.stderr)
            return False
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
            print(f"  音频文件生成失败或为空", file=sys.stderr)
            return False
        print(f"  音频提取完成", file=sys.stderr)
        return True
    except FileNotFoundError as e:
        print(f"  致命错误：{e}", file=sys.stderr)
        raise e
    except Exception as e:
        print(f"  音频提取异常：{e}", file=sys.stderr)
        return False

def transcribe_audio(audio_path):
    """使用 Whisper 将音频转写为文字"""
    try:
        import whisper
        model = whisper.load_model(WHISPER_MODEL)
        print(f"  正在使用 Whisper ({WHISPER_MODEL}) 转写音频...", file=sys.stderr)
        result = model.transcribe(
            audio=audio_path,
            language='zh',
            initial_prompt="以下是普通话的句子。",
            compression_ratio_threshold=2.4,
            logprob_threshold=-1.0,
            no_speech_threshold=0.6,
            word_timestamps=True
        )
        return result['text'].strip()
    except Exception as e:
        print(f"  转写失败：{e}", file=sys.stderr)
        return None

def build_filename(nickname, date_str, timestamp=None):
    """生成文件名"""
    if timestamp is None:
        timestamp = int(time.time())
    safe_nickname = "".join(c for c in nickname if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_nickname = safe_nickname.replace(' ', '_')
    return f"{safe_nickname}_{date_str}_{timestamp}.mp4"

# ==================== 主程序 ====================

def main():
    parser = argparse.ArgumentParser(description="微信视频号直播回放下载技能 (V2)")
    parser.add_argument("--keywords", required=True, help="视频号名称（搜索关键词）")
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)，不指定则下载最新一次回放")
    parser.add_argument("--output-dir", help="输出目录")
    parser.add_argument("--no-transcribe", action="store_true", help="跳过语音转文字步骤，只下载视频")
    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else DEFAULT_OUTPUT_DIR
    ensure_dir(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {
        "task": "微信视频号直播回放下载",
        "keywords": args.keywords,
        "target_date": args.date,
        "timestamp": timestamp,
        "status": "started"
    }

    script_dir = REPLAY_INPUT_BASE / args.keywords / args.date if args.date else REPLAY_INPUT_BASE / args.keywords
    ensure_dir(script_dir)
    txt_path = script_dir / "script.txt"

    try:
        tikhub_token = get_tikhub_token()

        # 1. 搜索用户
        print(f"\n[步骤 1] 搜索用户：{args.keywords}", file=sys.stderr)
        user = search_user(args.keywords, tikhub_token)
        username = user.get('contact', {}).get('username')
        nickname = user.get('contact', {}).get('nickname', args.keywords)
        print(f"  找到用户：{nickname} (username: {username})", file=sys.stderr)
        results['user'] = {
            'nickname': nickname,
            'username': username,
            'head_url': user.get('contact', {}).get('head_url')
        }

        # 2. 获取直播历史
        print(f"\n[步骤 2] 获取直播历史...", file=sys.stderr)
        replays = get_live_history(username, tikhub_token)
        print(f"  获取到 {len(replays)} 条直播记录", file=sys.stderr)

        # 3. 筛选回放
        print(f"\n[步骤 3] 筛选回放...", file=sys.stderr)
        target_replay, target_date_str = filter_replays_by_date(replays, args.date)
        if not target_replay:
            raise Exception("未找到符合条件的直播回放")
        print(f"  选中日期：{target_date_str}", file=sys.stderr)

        # 4. 提取下载 URL
        video_url = extract_video_url(target_replay)
        print(f"\n[步骤 4] 获取下载地址", file=sys.stderr)

        # 5. 下载视频
        filename = build_filename(nickname, target_date_str)
        filepath = output_dir / filename
        print(f"\n[步骤 5] 下载视频：{filepath}", file=sys.stderr)
        success = download_file(video_url, filepath)
        if not success:
            raise Exception("下载失败")
        results['downloaded_file'] = str(filepath)
        results['video_url'] = video_url

        # 6. 转录
        if not args.no_transcribe:
            print(f"\n[步骤 6] 提取音频并转写文字...", file=sys.stderr)
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_audio:
                audio_temp_path = tmp_audio.name
            if not extract_audio(filepath, audio_temp_path):
                raise Exception("音频提取失败")
            text = transcribe_audio(audio_temp_path)
            os.unlink(audio_temp_path)
            if text is None:
                raise Exception("语音转文字失败")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"  文字稿已保存至：{txt_path}", file=sys.stderr)
            results['script_file'] = str(txt_path)
        else:
            print(f"\n[步骤 6] 已跳过转录", file=sys.stderr)

        results['status'] = "success"

    except Exception as e:
        print(f"\n❌ 错误：{e}", file=sys.stderr)
        results['status'] = "failed"
        results['error'] = str(e)

    # 保存报告
    report_filename = f"wechat_replay_{args.keywords}_{timestamp}.json"
    report_path = script_dir / report_filename
    save_json(results, report_path)
    print(f"\n📄 报告已保存：{report_path}", file=sys.stderr)
    print(f"REPORT_PATH:{report_path}")

if __name__ == "__main__":
    main()
