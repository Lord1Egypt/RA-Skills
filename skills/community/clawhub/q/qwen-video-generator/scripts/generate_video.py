#!/usr/bin/env python3
"""
阿里云百炼文生视频工具 (Qwen Video Generator)

使用 wan2.2-t2v-plus 模型生成视频
支持异步任务提交和状态查询

环境变量配置:
  DASHSCOPE_API_KEY_VIDEO - 视频专用API Key (优先)
  DASHSCOPE_API_KEY       - 通用API Key (备用)
  VIDEO_OUTPUT_DIR        - 视频输出目录 (默认: workspace/videos/)
  VIDEO_OUTPUT_SIZE       - 分辨率: 480=832*480, 1080=1920*1080 (默认: 480)
  VIDEO_OUTPUT_LENGTH     - 视频秒数，1-15 (默认: 5)
"""

import argparse
import json
import os
import sys
import time
import hashlib
import requests
from pathlib import Path

API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"
TASK_QUERY_URL = "https://dashscope.aliyuncs.com/api/v1/tasks/"

# 分辨率映射
SIZE_MAP = {
    "480": "832*480",
    "1080": "1920*1080"
}

# 支持的分辨率列表
SUPPORTED_SIZES = ["1080*1920", "1920*1080", "1440*1440", "1632*1248", 
                   "1248*1632", "480*832", "832*480", "624*624"]


def get_api_key():
    """获取API Key，优先使用 DASHSCOPE_API_KEY_VIDEO"""
    api_key = os.environ.get("DASHSCOPE_API_KEY_VIDEO")
    if api_key:
        return api_key
    
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if api_key:
        return api_key
    
    print("❌ 错误: 未设置 API Key 环境变量", file=sys.stderr)
    print("   请配置: export DASHSCOPE_API_KEY_VIDEO=your_api_key", file=sys.stderr)
    print("   或使用: export DASHSCOPE_API_KEY=your_api_key", file=sys.stderr)
    sys.exit(1)


def get_output_dir():
    """获取输出目录"""
    output_dir = os.environ.get("VIDEO_OUTPUT_DIR")
    if output_dir:
        return Path(output_dir)
    workspace = os.environ.get("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw" / "workspace"))
    return Path(workspace) / "videos"


def get_video_size(size_arg):
    """
    解析视频分辨率
    - 环境变量 VIDEO_OUTPUT_SIZE: 480 或 1080
    - 命令行参数: 直接指定如 832*480 或简写 480/1080
    """
    # 先检查环境变量
    env_size = os.environ.get("VIDEO_OUTPUT_SIZE", "480")
    
    # 如果命令行指定了 size，优先使用命令行
    if size_arg:
        # 如果是简写 (480/1080)，转换为完整格式
        if size_arg in SIZE_MAP:
            return SIZE_MAP[size_arg]
        return size_arg
    
    # 使用环境变量
    if env_size in SIZE_MAP:
        return SIZE_MAP[env_size]
    
    # 默认 480
    return SIZE_MAP["480"]


def get_video_length(length_arg):
    """
    获取视频时长 (秒)
    - 环境变量 VIDEO_OUTPUT_LENGTH: 1-15
    - 命令行参数: 1-15
    - 默认: 5
    """
    # 命令行优先
    if length_arg is not None:
        length = length_arg
    else:
        try:
            length = int(os.environ.get("VIDEO_OUTPUT_LENGTH", "5"))
        except ValueError:
            length = 5
    
    # 限制范围
    if length < 1:
        length = 1
    elif length > 15:
        length = 15
    
    return length


def submit_video_task(api_key, prompt, size="832*480", duration=5, prompt_extend=True, model="wan2.2-t2v-plus"):
    """提交文生视频任务"""
    headers = {
        "X-DashScope-Async": "enable",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "size": size,
            "duration": duration,
            "prompt_extend": prompt_extend
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"❌ 提交任务失败: {response.status_code}", file=sys.stderr)
        print(f"   响应: {response.text}", file=sys.stderr)
        sys.exit(1)
    
    result = response.json()
    task_id = result.get("output", {}).get("task_id")
    
    if not task_id:
        print(f"❌ 未获取到任务ID: {result}", file=sys.stderr)
        sys.exit(1)
    
    return task_id


def query_task_status(api_key, task_id):
    """查询任务状态"""
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(f"{TASK_QUERY_URL}{task_id}", headers=headers)
    
    if response.status_code != 200:
        return None, f"查询失败: {response.status_code}"
    
    result = response.json()
    status = result.get("output", {}).get("task_status")
    return status, result


def download_video(url, output_path):
    """下载视频文件并设置权限 (644: rw-r--r--)"""
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print(f"❌ 下载失败: {response.status_code}", file=sys.stderr)
        return False
    
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    # 设置文件权限为 644 (rw-r--r--)，让 nginx 可以读取
    os.chmod(output_path, 0o644)
    
    return True


def generate_filename(prompt, prefix="video"):
    """根据prompt生成文件名"""
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:12]
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}_{prompt_hash}.mp4"


def main():
    parser = argparse.ArgumentParser(
        description="阿里云百炼文生视频工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础用法 (使用环境变量配置)
  python3 generate_video.py --prompt "一只猫在草地上奔跑"
  
  # 指定分辨率简写
  python3 generate_video.py --prompt "日落时分的海滩" --size 1080
  
  # 指定视频时长
  python3 generate_video.py --prompt "城市夜景" --length 10

环境变量:
  DASHSCOPE_API_KEY_VIDEO  - 视频专用API Key (优先)
  DASHSCOPE_API_KEY        - 通用API Key (备用)
  VIDEO_OUTPUT_DIR         - 视频输出目录 (默认: workspace/videos/)
  VIDEO_OUTPUT_SIZE        - 分辨率: 480=832*480, 1080=1920*1080 (默认: 480)
  VIDEO_OUTPUT_LENGTH      - 视频秒数，1-15 (默认: 5)
"""
    )
    
    parser.add_argument("--prompt", "-p", required=True, help="视频描述文本")
    parser.add_argument("--size", "-s", default=None, 
                        help="视频分辨率，支持简写(480/1080)或完整格式(832*480/1920*1080)")
    parser.add_argument("--length", "-l", type=int, default=None,
                        help="视频时长(秒)，1-15")
    parser.add_argument("--model", "-m", default="wan2.2-t2v-plus", help="模型名称")
    parser.add_argument("--no-prompt-extend", action="store_true", help="禁用prompt自动扩展")
    parser.add_argument("--timeout", "-t", type=int, default=600, help="最大等待秒数 (默认: 600)")
    parser.add_argument("--poll-interval", type=int, default=10, help="轮询间隔秒数 (默认: 10)")
    
    args = parser.parse_args()
    
    api_key = get_api_key()
    output_dir = get_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 解析分辨率和时长
    size = get_video_size(args.size)
    length = get_video_length(args.length)
    
    # 提交任务
    print(f"📤 提交文生视频任务...")
    print(f"   模型: {args.model}")
    print(f"   分辨率: {size}")
    print(f"   时长: {length}秒")
    print(f"   输出目录: {output_dir}")
    print(f"   Prompt: {args.prompt[:50]}{'...' if len(args.prompt) > 50 else ''}")
    
    task_id = submit_video_task(
        api_key=api_key,
        prompt=args.prompt,
        size=size,
        duration=length,
        prompt_extend=not args.no_prompt_extend,
        model=args.model
    )
    
    print(f"✅ 任务已提交，task_id: {task_id}")
    
    # 轮询任务状态
    print(f"⏳ 等待视频生成 (最多 {args.timeout} 秒)...")
    
    start_time = time.time()
    last_status = None
    
    while time.time() - start_time < args.timeout:
        status, result = query_task_status(api_key, task_id)
        
        if status != last_status:
            status_emoji = {
                "PENDING": "⏳",
                "RUNNING": "🎬",
                "SUCCEEDED": "✅",
                "FAILED": "❌",
                "CANCELED": "🚫"
            }.get(status, "❓")
            print(f"   {status_emoji} 状态: {status}")
            last_status = status
        
        if status == "SUCCEEDED":
            video_url = result.get("output", {}).get("video_url")
            if video_url:
                filename = generate_filename(args.prompt)
                output_path = output_dir / filename
                
                print(f"📥 下载视频: {video_url}")
                if download_video(video_url, output_path):
                    print(f"✅ 视频已保存: {output_path}")
                    print(f"VIDEO_PATH:{output_path}")
                else:
                    sys.exit(1)
            else:
                print(f"❌ 未找到视频URL", file=sys.stderr)
                sys.exit(1)
            break
        
        elif status == "FAILED":
            error_msg = result.get("output", {}).get("message", "未知错误")
            print(f"❌ 任务失败: {error_msg}", file=sys.stderr)
            sys.exit(1)
        
        elif status in ["CANCELED", "UNKNOWN"]:
            print(f"❌ 任务异常: {status}", file=sys.stderr)
            sys.exit(1)
        
        time.sleep(args.poll_interval)
    else:
        print(f"❌ 超时: 任务在 {args.timeout} 秒内未完成", file=sys.stderr)
        print(f"   task_id: {task_id} (可用于后续查询)", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
