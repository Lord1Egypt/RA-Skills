#!/usr/bin/env python3
"""
MiniMax 异步语音合成工具
使用异步端点，自动保存音频到本地
用法: python tts_sync.py "要转换的文本" --voice "音色ID" --speed 1.0
"""

import argparse
import os
import requests
import sys
import time


def create_tts_task(
    text: str,
    voice_id: str = "Chinese (Mandarin)_Lyrical_Voice",
    speed: float = 1.0,
    vol: float = 1.0,
    pitch: int = 0,
    emotion: str = None,
    model: str = "speech-2.8-hd",
    format: str = "mp3",
    sample_rate: int = 32000,
    bitrate: int = 128000,
    api_key: str = None,
):
    """创建异步语音合成任务"""
    api_key = api_key or os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

    url = "https://api.minimaxi.com/v1/t2a_async_v2"

    payload = {
        "model": model,
        "text": text,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": vol,
            "pitch": pitch,
        },
        "audio_setting": {
            "audio_sample_rate": sample_rate,
            "format": format,
            "bitrate": bitrate,
            "channel": 1,
        },
    }

    if emotion:
        payload["voice_setting"]["emotion"] = emotion

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"正在创建语音合成任务...")
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    result = response.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"API 错误: {result.get('base_resp', {}).get('status_msg', '未知错误')}")

    return result


def query_tts_task(task_id: int, api_key: str = None):
    """查询任务状态"""
    api_key = api_key or os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

    url = f"https://api.minimaxi.com/v1/query/t2a_async_query_v2?task_id={task_id}"

    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers, timeout=30)
    return response.json()


def download_audio(file_id: int, save_path: str, api_key: str = None):
    """下载音频到本地"""
    api_key = api_key or os.getenv("MINIMAX_API_KEY")

    file_resp = requests.get(
        f"https://api.minimaxi.com/v1/files/retrieve?file_id={file_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    result = file_resp.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"获取下载链接失败: {result.get('base_resp', {}).get('status_msg')}")

    download_url = result["file"]["download_url"]

    print(f"正在下载音频...")
    audio_resp = requests.get(download_url, timeout=60)
    with open(save_path, 'wb') as f:
        f.write(audio_resp.content)


def wait_for_completion(task_id: int, api_key: str = None, interval: int = 3, max_wait: int = 60):
    """等待任务完成"""
    status_map = {
        "Processing": "处理中",
        "Success": "成功",
        "Failed": "失败",
        "Expired": "已过期"
    }

    print(f"等待语音合成完成 (任务ID: {task_id})...")
    start_time = time.time()

    while time.time() - start_time < max_wait:
        result = query_tts_task(task_id, api_key)
        status = result.get("status")

        print(f"  状态: {status_map.get(status, status)}...", end="", flush=True)

        if status == "Success":
            print(" ✅")
            return result.get("file_id")
        elif status in ["Failed", "Expired"]:
            print(f" ❌")
            raise Exception(f"任务{status_map.get(status, status)}")

        print("")
        time.sleep(interval)

    raise Exception(f"等待超时（{max_wait}秒）")


def main():
    parser = argparse.ArgumentParser(description="MiniMax 语音合成工具")
    parser.add_argument("text", help="要转换的文本")
    parser.add_argument("--voice", dest="voice_id", default="Chinese (Mandarin)_Lyrical_Voice")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--vol", type=float, default=1.0)
    parser.add_argument("--pitch", type=int, default=0)
    parser.add_argument("--emotion", choices=["happy", "sad", "angry", "fearful", "disgusted", "surprised", "calm", "fluent", "whisper"])
    parser.add_argument("--model", default="speech-2.8-hd")
    parser.add_argument("--format", default="mp3", choices=["mp3", "pcm", "flac"])
    parser.add_argument("--sample-rate", type=int, default=32000)
    parser.add_argument("--bitrate", type=int, default=128000)
    parser.add_argument("--api-key", dest="api_key")
    parser.add_argument("--save-dir", dest="save_dir",
                        default="~/.openclaw/workspace/assets/audios",
                        help="保存目录")
    parser.add_argument("--save-name", dest="save_name",
                        help="保存文件名（不含扩展名）")

    args = parser.parse_args()

    try:
        # 创建任务
        result = create_tts_task(
            text=args.text,
            voice_id=args.voice_id,
            speed=args.speed,
            vol=args.vol,
            pitch=args.pitch,
            emotion=args.emotion,
            model=args.model,
            format=args.format,
            sample_rate=args.sample_rate,
            bitrate=args.bitrate,
            api_key=args.api_key,
        )

        task_id = result["task_id"]
        print(f"✅ 任务创建成功! 任务ID: {task_id}")

        # 等待完成
        file_id = wait_for_completion(task_id, args.api_key)

        # 保存音频
        save_dir = os.path.expanduser(args.save_dir)
        os.makedirs(save_dir, exist_ok=True)

        if args.save_name:
            safe_name = "".join(c for c in args.save_name if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = f"{safe_name}.{args.format}"
        else:
            timestamp = int(time.time())
            filename = f"tts_{timestamp}.{args.format}"

        save_path = os.path.join(save_dir, filename)

        download_audio(file_id, save_path, args.api_key)

        file_size = os.path.getsize(save_path) / (1024 * 1024)
        print(f"\n✅ 语音合成完成!")
        print(f"   保存路径: {save_path}")
        print(f"   文件大小: {file_size:.2f} MB")

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
