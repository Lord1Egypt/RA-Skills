#!/usr/bin/env python3
"""
MiniMax 视频生成工具
支持文生视频、图生视频、首尾帧生成视频
自动保存视频到本地，显示进度
用法: python generate_video.py "视频描述" --model MiniMax-Hailuo-2.3
     python generate_video.py "视频描述" --model MiniMax-Hailuo-2.3 --first-image path/to/image.jpg
     python generate_video.py "视频描述" --model MiniMax-Hailuo-02 --first-image start.jpg --last-image end.jpg
"""

import argparse
import os
import requests
import sys
import time
import base64


def create_video(
    prompt: str,
    model: str = "MiniMax-Hailuo-2.3",
    first_image: str = None,
    last_image: str = None,
    duration: int = 6,
    resolution: str = "768P",
    prompt_optimizer: bool = True,
    fast_pretreatment: bool = False,
    aigc_watermark: bool = False,
    api_key: str = None,
):
    """创建视频生成任务"""

    api_key = api_key or os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

    url = "https://api.minimaxi.com/v1/video_generation"

    payload = {
        "model": model,
        "prompt": prompt,
        "duration": duration,
        "resolution": resolution,
        "prompt_optimizer": prompt_optimizer,
        "aigc_watermark": aigc_watermark,
    }

    # 处理图片输入
    if first_image:
        if first_image.startswith("http"):
            payload["first_frame_image"] = first_image
        else:
            with open(first_image, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode()
            ext = first_image.split(".")[-1].lower()
            mime = f"image/{ext}" if ext in ["jpg", "jpeg", "png", "webp"] else "image/jpeg"
            payload["first_frame_image"] = f"data:{mime};base64,{img_base64}"

    if last_image:
        if last_image.startswith("http"):
            payload["last_frame_image"] = last_image
        else:
            with open(last_image, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode()
            ext = last_image.split(".")[-1].lower()
            mime = f"image/{ext}" if ext in ["jpg", "jpeg", "png", "webp"] else "image/jpeg"
            payload["last_frame_image"] = f"data:{mime};base64,{img_base64}"

    if fast_pretreatment and model in ["MiniMax-Hailuo-2.3", "MiniMax-Hailuo-2.3-Fast", "MiniMax-Hailuo-02"]:
        payload["fast_pretreatment"] = True

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"正在创建视频生成任务 ({model})...")
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    result = response.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"API 错误: {result.get('base_resp', {}).get('status_msg', '未知错误')}")

    return result


def query_video(task_id: str, api_key: str = None):
    """查询视频任务状态"""
    api_key = api_key or os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("未设置 MINIMAX_API_KEY 环境变量")

    url = f"https://api.minimaxi.com/v1/query/video_generation?task_id={task_id}"

    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers, timeout=30)
    return response.json()


def download_video(file_id: int, save_path: str, api_key: str = None):
    """下载视频到本地"""
    api_key = api_key or os.getenv("MINIMAX_API_KEY")

    file_resp = requests.get(
        f"https://api.minimaxi.com/v1/files/retrieve?file_id={file_id}",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    result = file_resp.json()

    if result.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"获取下载链接失败: {result.get('base_resp', {}).get('status_msg')}")

    download_url = result["file"]["download_url"]

    print(f"正在下载视频 (约 3-5MB)...\n")
    video_resp = requests.get(download_url, timeout=180)
    with open(save_path, 'wb') as f:
        f.write(video_resp.content)


def wait_for_video(task_id: str, api_key: str = None, interval: int = 5):
    """等待视频生成完成，显示进度"""
    print(f"\n等待视频生成完成 (任务ID: {task_id})")
    print("(按 Ctrl+C 可中断等待)\n")

    status_map = {
        "Preparing": "准备中",
        "Queueing": "队列中",
        "Processing": "生成中",
        "Success": "成功",
        "Fail": "失败",
    }

    dots = 0
    while True:
        result = query_video(task_id, api_key)
        status = result.get("status")

        # 进度显示
        if status == "Processing":
            dots = (dots + 1) % 4
            loading = "." * dots
            print(f"\r  状态: {status_map.get(status, status)} {loading}    ", end="", flush=True)
        else:
            print(f"\r  状态: {status_map.get(status, status)}       ")

        if status in ["Success", "Fail"]:
            print()  # 换行
            if status == "Success":
                print(f"✅ 视频生成成功!")
                print(f"   文件ID: {result.get('file_id')}")
                print(f"   分辨率: {result.get('video_width')}x{result.get('video_height')}")
                return result.get("file_id")
            else:
                raise Exception("视频生成失败")

        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="MiniMax 视频生成工具")
    parser.add_argument("prompt", nargs="?", help="视频描述")
    parser.add_argument("--model", default="MiniMax-Hailuo-2.3",
                        help="模型名称")
    parser.add_argument("--first-image", dest="first_image", help="起始帧图片路径或URL")
    parser.add_argument("--last-image", dest="last_image", help="结束帧图片路径或URL")
    parser.add_argument("--duration", type=int, choices=[6, 10], default=6, help="视频时长(秒)")
    parser.add_argument("--resolution", default="768P",
                        choices=["512P", "720P", "768P", "1080P"], help="分辨率")
    parser.add_argument("--no-optimizer", action="store_true", help="禁用 prompt 优化")
    parser.add_argument("--fast", action="store_true", help="启用快速预处理")
    parser.add_argument("--watermark", action="store_true", help="添加水印")
    parser.add_argument("--query", dest="query_task_id", help="查询任务状态")
    parser.add_argument("--api-key", dest="api_key")
    parser.add_argument("--save-dir", dest="save_dir",
                        default="~/.openclaw/workspace/assets/videos",
                        help="保存目录")

    args = parser.parse_args()

    try:
        if args.query_task_id:
            result = query_video(args.query_task_id, args.api_key)
            print(f"任务ID: {result.get('task_id')}")
            print(f"状态: {result.get('status')}")
            if result.get('file_id'):
                print(f"文件ID: {result.get('file_id')}")
            if result.get('video_width'):
                print(f"分辨率: {result.get('video_width')}x{result.get('video_height')}")
            return

        if not args.prompt and not args.first_image:
            print("❌ 需要提供 --prompt 或 --first-image", file=sys.stderr)
            sys.exit(1)

        # 创建任务
        result = create_video(
            prompt=args.prompt or "视频生成",
            model=args.model,
            first_image=args.first_image,
            last_image=args.last_image,
            duration=args.duration,
            resolution=args.resolution,
            prompt_optimizer=not args.no_optimizer,
            fast_pretreatment=args.fast,
            aigc_watermark=args.watermark,
            api_key=args.api_key,
        )

        task_id = result["task_id"]
        print(f"\n✅ 任务创建成功!")
        print(f"   任务ID: {task_id}")
        print(f"   模型: {args.model}")
        print(f"   时长: {args.duration}s")
        print(f"   分辨率: {args.resolution}")

        # 等待完成
        file_id = wait_for_video(task_id, args.api_key)

        # 保存视频
        save_dir = os.path.expanduser(args.save_dir)
        os.makedirs(save_dir, exist_ok=True)

        timestamp = int(time.time())
        filename = f"video_{task_id}_{timestamp}.mp4"
        save_path = os.path.join(save_dir, filename)

        download_video(file_id, save_path, args.api_key)

        file_size = os.path.getsize(save_path) / (1024 * 1024)
        print(f"\n💾 视频已保存: {save_path}")
        print(f"📊 文件大小: {file_size:.2f} MB")

    except KeyboardInterrupt:
        print("\n\n已中断，可使用 --query 后续查询")
        print(f"任务ID: {task_id}")
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
