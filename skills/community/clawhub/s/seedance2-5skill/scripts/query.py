#!/usr/bin/env python3
"""Seedance2.5 Skill - 查询脚本（积分/状态/作品）多平台通用"""

import os
import sys
import json
import argparse

# 多平台兼容
try:
    from coze_workload_identity import requests
except ImportError:
    import requests

API_BASE = "https://seedance25movie.coze.site"
SKILL_ID = "7659691849480814655"


def get_api_key():
    """获取API Key（兼容多平台）"""
    key = os.getenv(f"COZE_AI_DIRECTOR_KEY_{SKILL_ID}")
    if key and not key.startswith("COZE_CRED_DUMMY"):
        return key
    key = os.getenv("AI_DIRECTOR_API_KEY")
    if key:
        return key
    print(json.dumps({"error": "API Key未配置，请设置 AI_DIRECTOR_API_KEY 环境变量"}, ensure_ascii=False))
    sys.exit(1)


def mcp_call(tool_name, arguments=None, timeout=30):
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
            "arguments": arguments or {},
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


def check_credits():
    """查询积分余额"""
    result = mcp_call("check_credits")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def check_status(task_id):
    """查询任务状态"""
    result = mcp_call("check_status", {"task_id": task_id})

    if isinstance(result, dict):
        status = result.get("status", "unknown")
        if status == "completed":
            video_url = result.get("video_url") or result.get("url", "")
            print(json.dumps({
                "status": "completed",
                "video_url": video_url,
                "message": f"✅ 视频生成完成！下载链接: {video_url}"
            }, ensure_ascii=False, indent=2))
        elif status == "failed":
            print(json.dumps({
                "status": "failed",
                "message": "❌ 生成失败，积分已自动退还，可重新提交"
            }, ensure_ascii=False, indent=2))
        elif status in ("processing", "pending", "running"):
            print(json.dumps({
                "status": status,
                "message": "⏳ 正在生成中，请30秒后再次查询"
            }, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"error": "解析失败"}, ensure_ascii=False))


def list_works(work_type="all", limit=10):
    """查看作品列表"""
    result = mcp_call("list_works", {"type": work_type, "limit": limit})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seedance2.5 Skill - 查询工具")
    subparsers = parser.add_subparsers(dest="command", help="查询类型")

    subparsers.add_parser("credits", help="查询积分余额")

    sp = subparsers.add_parser("status", help="查询任务状态")
    sp.add_argument("task_id", help="任务ID")

    wp = subparsers.add_parser("works", help="查看作品列表")
    wp.add_argument("--type", default="all", help="类型: video, image, all")
    wp.add_argument("--limit", type=int, default=10, help="数量")

    args = parser.parse_args()

    if args.command == "credits":
        check_credits()
    elif args.command == "status":
        check_status(args.task_id)
    elif args.command == "works":
        list_works(args.type, args.limit)
    else:
        parser.print_help()
