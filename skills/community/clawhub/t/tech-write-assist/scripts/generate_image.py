#!/usr/bin/env python3
"""
AI 配图生成脚本
支持多个图像生成 API provider: 火山方舟 Ark (Seedream), Replicate, OpenAI (DALL-E)

用法:
    # 单图模式
    python generate_image.py "prompt" "16:9" "output.png"

    # 批量模式
    python generate_image.py --batch image_specs.json output_dir/

    # 指定 provider
    IMAGE_PROVIDER=ark python generate_image.py "prompt" "16:9" "output.png"

环境变量:
    IMAGE_PROVIDER       - 图像生成服务: ark (默认), replicate, openai
    ARK_API_KEY          - 火山方舟 Ark API key
    REPLICATE_API_TOKEN  - Replicate API token
    OPENAI_API_KEY       - OpenAI API key
"""

import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print("ERROR: requests library not installed. Run: pip install requests")
    sys.exit(1)


# =============================================================================
# Provider: Replicate (Seedream 5.0 Lite)
# =============================================================================

REPLICATE_API_URL = "https://api.replicate.com/v1/predictions"
REPLICATE_MODEL = "bytedance/seedream-5-lite"

# 比例映射: 我们的标准比例 -> Replicate API 接受的比例
REPLICATE_ASPECT_RATIOS = {
    "1:1": "1:1",
    "3:4": "3:4",
    "4:3": "4:3",
    "16:9": "16:9",
    "9:16": "9:16",
    "3:2": "3:2",
    "2:3": "2:3",
    "21:9": "21:9",
}


def generate_replicate(prompt, aspect_ratio="16:9", output_path="output.png"):
    """通过 Replicate API 调用 Seedream 5.0 Lite 生成图片"""
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        raise ValueError(
            "REPLICATE_API_TOKEN not set. "
            "Get your token at https://replicate.com/account/api-tokens"
        )

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    # 映射比例
    api_ratio = REPLICATE_ASPECT_RATIOS.get(aspect_ratio, "16:9")

    payload = {
        "version": REPLICATE_MODEL,
        "input": {
            "prompt": prompt,
            "size": "2K",
            "aspect_ratio": api_ratio,
            "output_format": "png",
        },
    }

    # 创建预测任务
    resp = requests.post(REPLICATE_API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    prediction = resp.json()

    # 轮询等待完成 (最长 5 分钟)
    poll_url = prediction["urls"]["get"]
    max_wait = 300
    waited = 0
    while prediction["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(3)
        waited += 3
        if waited > max_wait:
            raise TimeoutError(f"Image generation timed out after {max_wait}s")
        prediction = requests.get(poll_url, headers=headers, timeout=30).json()

    if prediction["status"] != "succeeded":
        error = prediction.get("error", "Unknown error")
        raise RuntimeError(f"Replicate generation failed: {error}")

    # 下载图片
    image_url = prediction["output"]
    if isinstance(image_url, list):
        image_url = image_url[0]

    img_data = requests.get(image_url, timeout=60).content
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_data)

    return output_path


# =============================================================================
# Provider: OpenAI (DALL-E 3)
# =============================================================================

OPENAI_API_URL = "https://api.openai.com/v1/images/generations"

# DALL-E 3 支持的尺寸
OPENAI_SIZES = {
    "1:1": "1024x1024",
    "16:9": "1792x1024",
    "9:16": "1024x1792",
    "3:4": "1024x1792",   # 近似
    "4:3": "1792x1024",   # 近似
    "3:2": "1792x1024",   # 近似
    "2:3": "1024x1792",   # 近似
    "21:9": "1792x1024",  # 近似
}


def generate_openai(prompt, aspect_ratio="16:9", output_path="output.png"):
    """通过 OpenAI API 调用 DALL-E 3 生成图片"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not set. "
            "Get your key at https://platform.openai.com/api-keys"
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    size = OPENAI_SIZES.get(aspect_ratio, "1792x1024")

    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": "hd",
        "response_format": "url",
    }

    resp = requests.post(OPENAI_API_URL, json=payload, headers=headers, timeout=120)
    resp.raise_for_status()
    result = resp.json()

    image_url = result["data"][0]["url"]
    img_data = requests.get(image_url, timeout=60).content
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_data)

    return output_path


# =============================================================================
# Provider: 火山方舟 Ark (Seedream 5.0)
# =============================================================================

ARK_API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
ARK_MODEL = "doubao-seedream-5-0-260128"

# 比例映射: 需要满足最小 3,686,400 像素 (1920x1920)
ARK_SIZES = {
    "1:1": "2048x2048",
    "3:4": "1920x2560",
    "4:3": "2560x1920",
    "16:9": "2560x1440",
    "9:16": "1440x2560",
    "3:2": "2400x1600",
    "2:3": "1600x2400",
    "21:9": "2560x1098",
}


def generate_ark(prompt, aspect_ratio="16:9", output_path="output.png"):
    """通过火山方舟 Ark API 调用 Seedream 5.0 生成图片"""
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        raise ValueError(
            "ARK_API_KEY not set. "
            "Get your key at https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey"
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    size = ARK_SIZES.get(aspect_ratio, "2048x2048")

    payload = {
        "model": ARK_MODEL,
        "prompt": prompt,
        "size": size,
    }

    resp = requests.post(ARK_API_URL, json=payload, headers=headers, timeout=120)
    resp.raise_for_status()
    result = resp.json()

    image_url = result["data"][0]["url"]
    img_data = requests.get(image_url, timeout=60).content
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_data)

    return output_path


# =============================================================================
# Provider 路由
# =============================================================================

PROVIDERS = {
    "ark": generate_ark,
    "replicate": generate_replicate,
    "openai": generate_openai,
}


def get_provider():
    """获取当前配置的 provider"""
    provider = os.environ.get("IMAGE_PROVIDER", "ark").lower()
    if provider not in PROVIDERS:
        print(f"WARNING: Unknown provider '{provider}', falling back to replicate")
        provider = "replicate"
    return provider


def generate_image(prompt, aspect_ratio="16:9", output_path="output.png"):
    """统一的图片生成入口"""
    provider = get_provider()
    generate_fn = PROVIDERS[provider]

    print(f"  Generating image with {provider}...")
    print(f"  Prompt: {prompt[:80]}...")
    print(f"  Aspect ratio: {aspect_ratio}")

    result = generate_fn(prompt, aspect_ratio, output_path)
    print(f"  Saved to: {result}")
    return result


# =============================================================================
# 批量生成
# =============================================================================

def batch_generate(image_specs, output_dir):
    """
    批量生成多张配图

    image_specs: list of dict, 每项包含:
        - name: 文件名（不含扩展名）
        - prompt: 图片生成 prompt
        - aspect_ratio: 比例 (可选, 默认 "16:9")
        - platform: 所属平台 (可选, 用于日志)
    """
    os.makedirs(output_dir, exist_ok=True)

    total = len(image_specs)
    results = []
    success_count = 0
    fail_count = 0

    print(f"\nBatch generating {total} images...")
    print(f"Provider: {get_provider()}")
    print(f"Output: {output_dir}\n")

    for i, spec in enumerate(image_specs):
        name = spec.get("name", f"image_{i}")
        prompt = spec.get("prompt", "")
        aspect_ratio = spec.get("aspect_ratio", "16:9")
        platform = spec.get("platform", "unknown")

        print(f"[{i + 1}/{total}] {name} ({platform})")

        output_path = os.path.join(output_dir, f"{name}.png")

        try:
            generate_image(prompt, aspect_ratio, output_path)
            results.append({
                "name": name,
                "path": output_path,
                "platform": platform,
                "status": "ok",
            })
            success_count += 1
        except Exception as e:
            error_msg = str(e)
            print(f"  ERROR: {error_msg}")
            results.append({
                "name": name,
                "platform": platform,
                "status": "fail",
                "error": error_msg,
            })
            fail_count += 1

        # 请求间隔，避免 rate limit
        if i < total - 1:
            time.sleep(1)

    print(f"\nBatch complete: {success_count} succeeded, {fail_count} failed")

    # 保存结果日志
    results_path = os.path.join(output_dir, "generation_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Results log: {results_path}")

    return results


# =============================================================================
# CLI 入口
# =============================================================================

def print_usage():
    print("Usage:")
    print("  Single image: python generate_image.py <prompt> [aspect_ratio] [output_path]")
    print("  Batch mode:   python generate_image.py --batch <specs.json> <output_dir>")
    print("")
    print("Environment variables:")
    print("  IMAGE_PROVIDER       - ark (default), replicate, openai")
    print("  ARK_API_KEY          - 火山方舟 Ark API key (Seedream)")
    print("  REPLICATE_API_TOKEN  - Replicate API token")
    print("  OPENAI_API_KEY       - OpenAI API key")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    if sys.argv[1] == "--batch":
        if len(sys.argv) < 4:
            print("Usage: python generate_image.py --batch <specs.json> <output_dir>")
            sys.exit(1)
        specs_path = sys.argv[2]
        output_dir = sys.argv[3]

        with open(specs_path, "r", encoding="utf-8") as f:
            specs = json.load(f)

        results = batch_generate(specs, output_dir)
        # 输出 JSON 结果到 stdout
        print("\n--- RESULTS JSON ---")
        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif sys.argv[1] in ("--help", "-h"):
        print_usage()

    else:
        prompt = sys.argv[1]
        aspect_ratio = sys.argv[2] if len(sys.argv) > 2 else "16:9"
        output_path = sys.argv[3] if len(sys.argv) > 3 else "output.png"

        generate_image(prompt, aspect_ratio, output_path)


if __name__ == "__main__":
    main()
