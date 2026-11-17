#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文AI图片生成工具
基于通义万象(DashScope)接口
"""

import argparse
import base64
import os
import sys
from pathlib import Path
import logging
import json
from datetime import datetime

# 1. 配置日志器
logger = logging.getLogger("LLM_Interaction")
logger.setLevel(logging.DEBUG)

# 避免重复添加 handler
if not logger.handlers:
    # 文件 Handler
    fh = logging.FileHandler("llm_interaction.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    
    # 控制台 Handler (可选)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)

try:
    import requests
except ImportError:
    print("错误：需要安装 requests 库", file=sys.stderr)
    print("安装命令：pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("错误：需要安装 pyyaml 库", file=sys.stderr)
    print("安装命令：pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def load_config():
    """加载配置文件"""
    candidates = [
        Path.cwd() / ".zhz" / "image-gen" / "config.yaml",
        Path.home() / ".zhz" / "image-gen" / "config.yaml",
    ]
    
    for path in candidates:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    print(f"已加载配置：{path}")
                    return config or {}
            except Exception as e:
                print(f"警告：无法解析配置文件 {path}: {e}")
    
    return {}


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="中文AI图片生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 基本生成
  python main.py --prompt "一只泰迪狗" --image dog.png
  
  # 指定宽高比
  python main.py --prompt "美丽的风景" --image out.png --ar 16:9
  
  # 高清质量
  python main.py --prompt "一只猫" --image out.png --quality 2k
  
  # 从文件读取提示词
  python main.py --promptfiles prompt.txt --image out.png
  
  # 使用参考图片（仅 wan2.7 模型）
  python main.py --prompt "更换背景" --image out.png --model wan2.7-image-pro --ref ref.png
        """
    )
    
    parser.add_argument("--prompt", "-p", help="提示词文本")
    parser.add_argument("--promptfiles", nargs="+", help="从文件读取提示词（可多个文件）")
    parser.add_argument("--image", required=True, help="输出图片路径")
    parser.add_argument("--model", "-m", help="模型ID（默认：qwen-image-2.0-pro）")
    parser.add_argument("--ar", help="宽高比（16:9, 1:1, 4:3 等）")
    parser.add_argument("--size", help="指定尺寸（宽x高，如 1024x1024）")
    parser.add_argument("--quality", choices=["normal", "2k"], default=None,
                       help="质量等级：normal（普通）或 2k（高清）")
    parser.add_argument("--ref", nargs="+", help="参考图片路径（仅 wan2.7-image 系列模型支持）")
    
    return parser.parse_args()


def load_prompt(args):
    """加载提示词"""
    if args.prompt:
        return args.prompt
    
    if args.promptfiles:
        parts = []
        for file_path in args.promptfiles:
            path = Path(file_path)
            if not path.exists():
                print(f"错误：提示词文件不存在：{file_path}", file=sys.stderr)
                sys.exit(1)
            with open(path, "r", encoding="utf-8") as f:
                parts.append(f.read().strip())
        return "\n\n".join(parts)
    
    print("错误：未提供提示词。请使用 --prompt 或 --promptfiles", file=sys.stderr)
    sys.exit(1)


def select_model(args, config):
    """选择模型"""
    if args.model:
        return args.model
    
    if config.get("default_model"):
        return config["default_model"]
    
    if os.getenv("DASHSCOPE_IMAGE_MODEL"):
        return os.getenv("DASHSCOPE_IMAGE_MODEL")
    
    return "qwen-image-2.0-pro"


def select_quality(args, config):
    """选择质量等级"""
    if args.quality:
        return args.quality
    
    if config.get("default_quality"):
        return config["default_quality"]
    
    return "1k"


def parse_size(size_str):
    """解析尺寸字符串"""
    if not size_str:
        return None
    parts = size_str.lower().replace("*", "x").split("x")
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    return None


def resolve_size(model, args, config):
    """解析图片尺寸"""
    if args.size:
        size = parse_size(args.size)
        if size:
            return f"{size[0]}*{size[1]}"
    
    if args.ar:
        ar = args.ar.replace(":", "x")
        quality = args.quality or config.get("default_quality", "1k")
        
        if "qwen-image-2.0" in model:
            ar_sizes = {
                "1x1": (1024, 1024) if quality == "normal" else (1536, 1536),
                "2x3": (768, 1152) if quality == "normal" else (1024, 1536),
                "3x2": (1152, 768) if quality == "normal" else (1536, 1024),
                "3x4": (960, 1280) if quality == "normal" else (1080, 1440),
                "4x3": (1280, 960) if quality == "normal" else (1440, 1080),
                "9x16": (720, 1280) if quality == "normal" else (1080, 1920),
                "16x9": (1280, 720) if quality == "normal" else (1920, 1080),
            }
            if ar in ar_sizes:
                w, h = ar_sizes[ar]
                return f"{w}*{h}"
        
        elif "qwen-image-max" in model or "qwen-image-plus" in model:
            fixed_sizes = {
                "16x9": "1664*928",
                "4x3": "1472*1104",
                "1x1": "1328*1328",
                "3x4": "1104*1472",
                "9x16": "928*1664",
            }
            return fixed_sizes.get(ar, "1664*928")
    
    quality = args.quality or config.get("default_quality", "1k")
    return "1024*1024" if quality == "normal" else "1536*1536"


def load_reference_image(ref_path):
    """加载参考图片为 data URL"""
    path = Path(ref_path)
    if not path.exists():
        raise FileNotFoundError(f"参考图片不存在：{ref_path}")
    
    with open(path, "rb") as f:
        image_data = f.read()
    
    suffix = path.suffix.lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
    }
    mime = mime_types.get(suffix, "image/png")
    
    b64 = base64.b64encode(image_data).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def generate_image(model, prompt, args, config):
    """调用通义万象API生成图片"""
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        # 回退到密钥文件
        for p in [Path.cwd() / ".dashscope_key", Path.home() / ".zhz-skills" / ".dashscope_key", Path(r"C:\Users\zhang\.openclaw\workspace") / ".dashscope_key"]:  # <!-- project: path:C:\Users\zhang\.openclaw\workspace -->
            print(f"path:{p}")
            if p.exists():
                api_key = p.read_text(encoding="utf-8").strip()
                if api_key:
                    print(f"从密钥文件加载: {p}")
                    break
    if not api_key:
        raise ValueError(
            "需要设置 API 密钥，任选其一：\n"
            "  1. 环境变量: set DASHSCOPE_API_KEY=xxx\n"
            "  2. 密钥文件: .dashscope_key"
        )
    
    base_url = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com")
    
    if args.ref:
        if "wan2.7-image" not in model:
            raise ValueError(
                f"模型 {model} 不支持参考图片。"
                "请使用 wan2.7-image-pro 或 wan2.7-image 模型。"
            )
        if len(args.ref) > 9:
            raise ValueError(
                f"wan2.7 模型最多支持9张参考图片，当前提供了 {len(args.ref)} 张。"
            )

    #https://llm-tgh2qgl5vs0d8yi4.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \

    url = f"{base_url}/api/v1/services/aigc/multimodal-generation/generation"
    
    content = []
    
    if args.ref:
        for ref_path in args.ref:
            content.append({"image": load_reference_image(ref_path)})

    logger.info(f"prompt: {prompt}")
    
    content.append({"text": prompt})
    
    body = {
        "model": model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": content,
                }
            ]
        },
        "parameters": {}
    }

    logger.info(f"model: {model}")
    
    # qwen-image-3.0 系列：简化参数，支持 prompt_extend
    if "qwen-image-3.0" in model:
        body["parameters"]["prompt_extend"] = True
        if args.size:
            body["parameters"]["size"] = args.size.replace("x", "*")
        print(f"正在生成图片（模型：{model}）...")
    else:
        # qwen-image-2.0 和其他旧模型：需要完整参数
        size = resolve_size(model, args, config)
        body["parameters"]["size"] = size
        body["parameters"]["prompt_extend"] = False
        
        if "qwen-image-2.0" in model or "qwen-image-max" in model or "qwen-image-plus" in model:
            body["parameters"]["watermark"] = False
            body["parameters"]["negative_prompt"] = (
                "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，"
                "人脸无细节，过度光滑，画面具有AI感，构图混乱，文字模糊，扭曲"
            )
        
        print(f"正在生成图片（模型：{model}，尺寸：{size}）...")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    print(f"正在生成图片（url：{url}）...")


    try:
        response = requests.post(url, headers=headers, json=body, timeout=300)
    except requests.exceptions.Timeout:
        raise RuntimeError("请求超时（300秒），请稍后重试")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"网络请求失败：{e}")
    
    if response.status_code != 200:
        raise RuntimeError(
            f"API错误（{response.status_code}）：{response.text}"
        )
    
    result = response.json()
    
    output = result.get("output", {})
    image_url = output.get("result_image")
    
    if not image_url:
        choices = output.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            msg_content = message.get("content", [])
            for item in msg_content:
                if "image" in item:
                    image_url = item["image"]
                    break
    
    if not image_url:
        raise RuntimeError(f"响应中没有图片：{result}")
    
    if image_url.startswith("http://") or image_url.startswith("https://"):
        try:
            img_response = requests.get(image_url, timeout=60)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"下载图片失败：{e}")
        
        if img_response.status_code != 200:
            raise RuntimeError(f"下载图片失败：{img_response.status_code}")
        return img_response.content
    
    return base64.b64decode(image_url)


def main():
    """主函数"""
    args = parse_args()
    
    config = load_config()
    prompt = load_prompt(args)
    
    model = select_model(args, config)
    quality = select_quality(args, config)
    args.quality = quality
    
    print(f"使用模型：{model}")
    print(f"质量等级：{quality}")
    
    try:
        image_data = generate_image(model, prompt, args, config)
        
        output_path = Path(args.image)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(image_data)
        
        print(f"✓ 图片已保存：{output_path}")
        
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
