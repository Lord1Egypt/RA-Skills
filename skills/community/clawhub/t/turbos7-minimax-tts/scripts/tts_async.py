#!/usr/bin/env python3
"""
MiniMax 异步语音合成工具
用法: python tts_async.py "要转换的文本" --voice "音色ID"
     python tts_async.py --query --task-id 123456789
"""

import argparse
import os
import requests
import sys
import time


def tts_async_create(
    text: str,
    voice_id: str = "Chinese (Mandarin)_Lyrical_Voice",
    model: str = "speech-2.8-hd",
    speed: float = 1.0,
    vol: float = 1.0,
    pitch: int = 0,
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
            "bitrate": bitrate,
            "format": format,
        },
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"正在创建异步任务...")
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    result = response.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"API 错误: {result.get('base_resp', {}).get('status_msg', '未知错误')}")

    return result


def tts_async_query(task_id: int, api_key: str = None):
    """查询异步任务状态"""
    api_key = api_key or os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

    url = f"https://api.minimaxi.com/v1/query/t2a_async_query_v2?task_id={task_id}"

    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers, timeout=30)
    return response.json()


def main():
    parser = argparse.ArgumentParser(description="MiniMax 异步语音合成工具")
    parser.add_argument("text", nargs="?", help="要转换的文本")
    parser.add_argument("--query", action="store_true", help="查询任务状态")
    parser.add_argument("--task-id", type=int, help="任务 ID")
    parser.add_argument("--voice", dest="voice_id", default="Chinese (Mandarin)_Lyrical_Voice")
    parser.add_argument("--model", default="speech-2.8-hd")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--format", default="mp3", choices=["mp3", "pcm", "flac"])
    parser.add_argument("--wait", action="store_true", help="等待任务完成")
    parser.add_argument("--api-key", dest="api_key")

    args = parser.parse_args()

    try:
        if args.query:
            if not args.task_id:
                print("❌ 查询模式需要 --task-id", file=sys.stderr)
                sys.exit(1)

            result = tts_async_query(args.task_id, args.api_key)
            status = result.get("status")
            print(f"任务状态: {status}")

            if status == "Success":
                print(f"文件 ID: {result.get('file_id')}")
            elif status == "Failed":
                print(f"任务失败")
            elif status == "Expired":
                print(f"任务已过期")

        else:
            if not args.text:
                print("❌ 需要提供文本内容", file=sys.stderr)
                sys.exit(1)

            result = tts_async_create(
                text=args.text,
                voice_id=args.voice_id,
                model=args.model,
                speed=args.speed,
                format=args.format,
                api_key=args.api_key,
            )

            task_id = result["task_id"]
            file_id = result["file_id"]
            print(f"\n✅ 任务创建成功!")
            print(f"任务 ID: {task_id}")
            print(f"文件 ID: {file_id}")

            if args.wait:
                print("\n等待任务完成...")
                while True:
                    time.sleep(5)
                    status_result = tts_async_query(task_id, args.api_key)
                    status = status_result.get("status")
                    print(f"  状态: {status}")

                    if status in ["Success", "Failed", "Expired"]:
                        break

                if status == "Success":
                    print(f"\n🎉 任务完成! 文件 ID: {status_result.get('file_id')}")
                else:
                    print(f"\n❌ 任务结束，状态: {status}")

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
