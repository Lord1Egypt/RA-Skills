#!/usr/bin/env python3
"""
Video Generation Skill for MiniMax API
Supports: text-to-video, image-to-video, start-end-to-video, subject-reference
"""

import os
import sys
import time
import argparse
import requests

API_KEY = os.environ.get("MINIMAX_API_KEY")
if not API_KEY:
    print("Error: MINIMAX_API_KEY environment variable not set")
    print("Please set it with: export MINIMAX_API_KEY=\"your-api-key\"")
    sys.exit(1)

HEADERS = {"Authorization": f"Bearer {API_KEY}"}
API_HOST = "https://api.minimaxi.com"


def invoke_text_to_video(prompt: str, duration: int = 6, resolution: str = "1080P") -> str:
    """(模式一) 通过文本描述发起视频生成任务。"""
    url = f"{API_HOST}/v1/video_generation"
    payload = {
        "prompt": prompt,
        "model": "MiniMax-Hailuo-2.3",
        "duration": duration,
        "resolution": resolution,
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    task_id = response.json()["task_id"]
    return task_id


def invoke_image_to_video(prompt: str, image_url: str, duration: int = 6, resolution: str = "1080P") -> str:
    """(模式二) 通过首帧图像和文本描述发起视频生成任务。"""
    url = f"{API_HOST}/v1/video_generation"
    payload = {
        "prompt": prompt,
        "first_frame_image": image_url,
        "model": "MiniMax-Hailuo-2.3",
        "duration": duration,
        "resolution": resolution,
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    task_id = response.json()["task_id"]
    return task_id


def invoke_start_end_to_video(prompt: str, first_image: str, last_image: str, duration: int = 6, resolution: str = "1080P") -> str:
    """(模式三) 使用首帧图像、尾帧图像和文本描述发起视频生成任务。"""
    url = f"{API_HOST}/v1/video_generation"
    payload = {
        "prompt": prompt,
        "first_frame_image": first_image,
        "last_frame_image": last_image,
        "model": "MiniMax-Hailuo-02",
        "duration": duration,
        "resolution": resolution,
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    task_id = response.json()["task_id"]
    return task_id


def invoke_subject_reference(prompt: str, subject_image: str, duration: int = 6, resolution: str = "1080P") -> str:
    """(模式四) 使用人物主体图片和文本描述发起视频生成任务"""
    url = f"{API_HOST}/v1/video_generation"
    payload = {
        "prompt": prompt,
        "subject_reference": [
            {
                "type": "character",
                "image": [subject_image],
            }
        ],
        "model": "S2V-01",
        "duration": duration,
        "resolution": resolution,
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    task_id = response.json()["task_id"]
    return task_id


def query_task_status(task_id: str) -> str:
    """根据 task_id 轮询任务状态，直至任务成功或失败。"""
    url = f"{API_HOST}/v1/query/video_generation"
    params = {"task_id": task_id}
    
    print(f"开始轮询任务状态，task_id: {task_id}")
    print("每10秒查询一次，请耐心等待...")
    
    while True:
        time.sleep(10)
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        response_json = response.json()
        status = response_json["status"]
        print(f"当前任务状态: {status}")
        
        if status == "Success":
            return response_json["file_id"]
        elif status == "Fail":
            raise Exception(f"视频生成失败: {response_json.get('error_message', '未知错误')}")


def fetch_video(file_id: str, output_path: str = "output.mp4"):
    """根据 file_id 获取视频下载链接，并将其保存到本地。"""
    url = f"{API_HOST}/v1/files/retrieve"
    params = {"file_id": file_id}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    download_url = response.json()["file"]["download_url"]

    print(f"正在下载视频到 {output_path}...")
    with open(output_path, "wb") as f:
        video_response = requests.get(download_url)
        video_response.raise_for_status()
        f.write(video_response.content)
    print(f"视频已成功保存至 {output_path}")


def main():
    parser = argparse.ArgumentParser(description="MiniMax Video Generation")
    parser.add_argument("--mode", required=True, choices=["text", "image", "start_end", "subject"],
                        help="生成模式: text(文生视频), image(图生视频), start_end(首尾帧), subject(主体参考)")
    parser.add_argument("--prompt", required=True, help="视频描述文本")
    parser.add_argument("--image", help="图生视频的首帧图片URL")
    parser.add_argument("--first", help="首尾帧模式的首帧图片URL")
    parser.add_argument("--last", help="首尾帧模式的尾帧图片URL")
    parser.add_argument("--subject", help="主体参考模式的人脸图片URL")
    parser.add_argument("--duration", type=int, default=6, choices=[6, 10], help="视频时长: 6或10秒")
    parser.add_argument("--resolution", default="1080P", choices=["720P", "1080P"], help="分辨率")
    parser.add_argument("--output", default="output.mp4", help="输出文件名")
    
    args = parser.parse_args()
    
    # 验证参数
    if args.mode == "image" and not args.image:
        parser.error("--image 参数在 image 模式下必填")
    if args.mode == "start_end" and (not args.first or not args.last):
        parser.error("--first 和 --last 参数在 start_end 模式下必填")
    if args.mode == "subject" and not args.subject:
        parser.error("--subject 参数在 subject 模式下必填")
    
    # 创建任务
    print(f"正在创建视频生成任务...")
    print(f"模式: {args.mode}")
    print(f"描述: {args.prompt}")
    
    if args.mode == "text":
        task_id = invoke_text_to_video(args.prompt, args.duration, args.resolution)
    elif args.mode == "image":
        task_id = invoke_image_to_video(args.prompt, args.image, args.duration, args.resolution)
    elif args.mode == "start_end":
        task_id = invoke_start_end_to_video(args.prompt, args.first, args.last, args.duration, args.resolution)
    else:  # subject
        task_id = invoke_subject_reference(args.prompt, args.subject, args.duration, args.resolution)
    
    print(f"视频生成任务已提交，任务 ID: {task_id}")
    
    # 轮询任务状态
    file_id = query_task_status(task_id)
    print(f"任务处理成功，文件 ID: {file_id}")
    
    # 下载视频
    fetch_video(file_id, args.output)


if __name__ == "__main__":
    main()
