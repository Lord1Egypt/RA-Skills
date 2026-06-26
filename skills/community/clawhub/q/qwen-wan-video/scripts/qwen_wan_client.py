#!/usr/bin/env python3
"""
通义万相2.6视频生成客户端
直接调用阿里云DashScope API，无需中间代理
"""

import os
import time
import requests
import argparse
from typing import Optional

# 获取API密钥
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")

BASE_URL = "https://dashscope.aliyuncs.com/api/v1"

def create_video_task(
    prompt: str,
    image_url: Optional[str] = None,
    duration: int = 5,
    resolution: str = "720P"
) -> str:
    """创建视频生成任务"""
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"
    }
    
    # 构建输入参数
    input_data = {"prompt": prompt}
    if image_url:
        input_data["image_url"] = image_url
    
    payload = {
        "model": "wan2.6-t2v",
        "input": input_data,
        "parameters": {
            "resolution": resolution,
            "duration": duration,
            "shot_type": "single",
            "watermark": False
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    
    result = response.json()
    return result["output"]["task_id"]

def poll_task_status(task_id: str, timeout: int = 600, poll_interval: int = 10) -> str:
    """轮询任务状态直到完成"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        headers = {"Authorization": f"Bearer {DASHSCOPE_API_KEY}"}
        response = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers=headers
        )
        response.raise_for_status()
        
        result = response.json()
        status = result["output"]["task_status"]
        
        if status == "SUCCEEDED":
            # 修正：处理可能的字段结构差异
            output = result["output"]
            if "results" in output:
                return output["results"][0]["url"]
            elif "result" in output:
                return output["result"]["url"]
            else:
                raise RuntimeError(f"Unexpected response structure: {output}")
        elif status == "FAILED":
            raise RuntimeError(f"任务失败: {result.get('message', '未知错误')}")
        
        time.sleep(poll_interval)
    
    raise TimeoutError(f"任务超时 ({timeout}秒)")

def generate_video_t2v(prompt: str, duration: int = 5, resolution: str = "720P") -> str:
    """文生视频"""
    task_id = create_video_task(prompt, duration=duration, resolution=resolution)
    return poll_task_status(task_id)

def generate_video_i2v(prompt: str, image_url: str, duration: int = 5) -> str:
    """图生视频"""
    task_id = create_video_task(prompt, image_url=image_url, duration=duration)
    return poll_task_status(task_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="通义万相视频生成工具")
    parser.add_argument("mode", choices=["t2v", "i2v"], help="生成模式：t2v(文生视频) 或 i2v(图生视频)")
    parser.add_argument("--prompt", required=True, help="视频描述提示词")
    parser.add_argument("--image-url", help="参考图像URL（仅i2v模式需要）")
    parser.add_argument("--duration", type=int, default=5, help="视频时长(秒)，默认5")
    parser.add_argument("--resolution", default="720P", choices=["720P", "1080P"], help="分辨率")
    
    args = parser.parse_args()
    
    try:
        if args.mode == "t2v":
            video_url = generate_video_t2v(args.prompt, args.duration, args.resolution)
        else:
            if not args.image_url:
                raise ValueError("--image-url 是 i2v 模式必需的参数")
            video_url = generate_video_i2v(args.prompt, args.image_url, args.duration)
        
        print(f"视频生成成功: {video_url}")
    except Exception as e:
        print(f"错误: {e}")
        exit(1)