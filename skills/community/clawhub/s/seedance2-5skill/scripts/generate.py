#!/usr/bin/env python3
"""Seedance2.5 Skill - AI视频/图片生成脚本（多平台通用）"""

import os
import sys
import json
import argparse

# 多平台兼容：Coze用coze_workload_identity，OpenClaw/WorkBuddy用标准requests
try:
    from coze_workload_identity import requests
    IS_COZE = True
except ImportError:
    import requests
    IS_COZE = False

API_BASE = "https://seedance25movie.coze.site"
SKILL_ID = "7659691849480814655"


def get_api_key():
    """获取API Key（兼容多平台）"""
    # 优先读取Coze注入的环境变量
    key = os.getenv(f"COZE_AI_DIRECTOR_KEY_{SKILL_ID}")
    if key and not key.startswith("COZE_CRED_DUMMY"):
        return key
    # 回退到通用环境变量（OpenClaw/WorkBuddy/ClawHub）
    key = os.getenv("AI_DIRECTOR_API_KEY")
    if key:
        return key
    print(json.dumps({
        "error": "API Key未配置。请设置环境变量 AI_DIRECTOR_API_KEY=sk-xxx，或在扣子技能中配置API Key凭证",
        "help": "访问 https://seedance25movie.coze.site 注册获取API Key"
    }, ensure_ascii=False))
    sys.exit(1)


def mcp_call(tool_name, arguments, timeout=60):
    """统一MCP API调用"""
    api_key = get_api_key()
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments,
        },
        "id": 1,
    }

    try:
        response = requests.post(
            f"{API_BASE}/api/mcp",
            headers=headers,
            json=payload,
            timeout=timeout,
            proxies={"http": None, "https": None},
        )
        data = response.json()

        if "result" in data:
            content = data["result"].get("content", [])
            if content:
                text = content[0].get("text", "")
                try:
                    return json.loads(text) if isinstance(text, str) else text
                except json.JSONDecodeError:
                    return {"raw": text}
            return {"info": "无返回内容"}
        elif "error" in data:
            return {"error": data["error"].get("message", str(data["error"]))}
        else:
            return {"error": "未知响应格式"}

    except Exception as e:
        return {"error": f"请求失败: {str(e)}"}


def generate_video(prompt, model="seedance-2.0", ratio="16:9", resolution="480p", duration=4, image_url=None):
    """生成视频"""
    model_map = {
        "seedance-2.0": "doubao-seedance-2-0-260128",
        "seedance-2.0-fast": "doubao-seedance-2-0-fast-260128",
        "seedance-1.5-pro": "doubao-seedance-1-5-pro-responses",
    }
    actual_model = model_map.get(model, model)

    args = {
        "model": actual_model,
        "prompt": prompt,
        "ratio": ratio,
        "resolution": resolution,
        "duration": duration,
    }
    if image_url:
        args["image_url"] = image_url
        args["mode"] = "first_frame"

    result = mcp_call("generate_video", args)

    if isinstance(result, dict):
        if result.get("task_id"):
            print(json.dumps({
                "success": True,
                "task_id": result["task_id"],
                "model": model,
                "message": f"视频生成任务已提交，任务ID: {result['task_id']}，预计1-5分钟完成，请用 query.py status {result['task_id']} 查询"
            }, ensure_ascii=False))
        elif result.get("error"):
            print(json.dumps({"error": result["error"]}, ensure_ascii=False))
        else:
            print(json.dumps(result, ensure_ascii=False))
    else:
        print(json.dumps({"error": "解析失败", "raw": str(result)}, ensure_ascii=False))


def generate_image(prompt, model="seedream-5.0-lite", size="1024x1024"):
    """生成图片"""
    args = {
        "prompt": prompt,
        "model": model,
        "size": size,
    }
    result = mcp_call("text_to_image", args, timeout=120)

    if isinstance(result, dict):
        if result.get("task_id"):
            print(json.dumps({
                "success": True,
                "task_id": result["task_id"],
                "message": f"图片生成任务已提交，任务ID: {result['task_id']}"
            }, ensure_ascii=False))
        elif result.get("error"):
            print(json.dumps({"error": result["error"]}, ensure_ascii=False))
        elif result.get("url") or result.get("image_url"):
            print(json.dumps({
                "success": True,
                "url": result.get("url") or result.get("image_url"),
            }, ensure_ascii=False))
        else:
            print(json.dumps(result, ensure_ascii=False))
    else:
        print(json.dumps({"error": "解析失败", "raw": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seedance2.5 Skill - AI视频图片生成")
    subparsers = parser.add_subparsers(dest="command", help="生成类型")

    # 视频生成
    vp = subparsers.add_parser("video", help="生成视频")
    vp.add_argument("prompt", help="视频提示词")
    vp.add_argument("--model", default="seedance-2.0",
                    help="模型: seedance-2.0, seedance-2.0-fast, seedance-1.5-pro")
    vp.add_argument("--ratio", default="16:9", help="比例: 16:9, 9:16, 1:1")
    vp.add_argument("--resolution", default="480p", help="分辨率: 480p, 720p, 1080p")
    vp.add_argument("--duration", type=int, default=4, help="时长(秒): 4,6,8,10")
    vp.add_argument("--image-url", help="参考图片URL（图生视频）")

    # 图片生成
    ip = subparsers.add_parser("image", help="生成图片")
    ip.add_argument("prompt", help="图片提示词")
    ip.add_argument("--model", default="seedream-5.0-lite", help="图片模型")
    ip.add_argument("--size", default="1024x1024", help="图片尺寸")

    args = parser.parse_args()

    if args.command == "video":
        generate_video(args.prompt, args.model, args.ratio, args.resolution, args.duration, args.image_url)
    elif args.command == "image":
        generate_image(args.prompt, args.model, args.size)
    else:
        parser.print_help()
