#!/usr/bin/env python3
"""
suno_generate.py — kie.ai Suno API 渐进生成脚本
用法: python suno_generate.py --style_tags "..." --lyrics "..." --title "..." [--instrumental] [--model V5]

API 文档: https://docs.kie.ai/suno-api/

必需环境变量:
  KIEAI_API_KEY  — kie.ai API 密钥（从 https://kie.ai/api-key 获取）

可选环境变量:
  CALLBACK_URL   — 回调地址；空字符串（默认）则不传给 API，使用内部轮询

安全说明:
  - SSL 验证始终启用，不可禁用
  - 建议 CALLBACK_URL 使用内部可信端点，或留空使用轮询
"""

import os
import sys
import json
import time
import argparse
import requests

API_KEY = os.environ.get("KIEAI_API_KEY")
BASE_URL = "https://api.kie.ai"

# 回调地址：空字符串（默认）则不传给 API，避免默认回调到第三方地址
CALLBACK_URL = os.environ.get("CALLBACK_URL", "")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def submit_generate(style_tags: str, lyrics: str, title: str,
                   model: str = "V5", instrumental: bool = False) -> str:
    """
    提交 Suno 生成任务，返回 task_id
    POST /api/v1/generate
    """
    if not API_KEY:
        raise Exception("错误: 请设置 KIEAI_API_KEY 环境变量")

    payload = {
        "prompt": lyrics,
        "style": style_tags,
        "title": title,
        "customMode": True,
        "instrumental": instrumental,
        "model": model,
    }
    # 仅当 CALLBACK_URL 非空时才传递，避免默认回调到第三方地址
    if CALLBACK_URL:
        payload["callBackUrl"] = CALLBACK_URL

    resp = requests.post(
        f"{BASE_URL}/api/v1/generate",
        headers=HEADERS,
        json=payload,
        timeout=30
    )
    data = resp.json()

    if resp.status_code != 200 or data.get("code") != 200:
        raise Exception(f"提交失败: {data.get('msg', resp.text)}")

    task_id = data["data"]["taskId"]
    print(f"[提交成功] task_id={task_id}", file=sys.stderr)
    return task_id


def check_task(task_id: str) -> dict:
    """
    查询任务状态
    GET /api/v1/generate/record-info?taskId={task_id}
    返回 data 字段内容，查询失败返回 None
    """
    if not API_KEY:
        raise Exception("错误: 请设置 KIEAI_API_KEY 环境变量")

    url = f"{BASE_URL}/api/v1/generate/record-info?taskId={task_id}"
    resp = requests.get(url, headers=HEADERS, timeout=20)
    data = resp.json()
    if data.get("code") != 200:
        return None
    return data["data"]


def poll_task(task_id: str, timeout: int = 300, interval: int = 15) -> dict:
    """
    轮询任务状态，直到完成或失败
    返回: { status, songs: [{audioUrl, title}], audio_url, title }
    状态流转: PENDING → TEXT_SUCCESS → FIRST_SUCCESS → SUCCESS
    终止状态: SUCCESS / FIRST_SUCCESS / CREATE_TASK_FAILED / GENERATE_AUDIO_FAILED /
              CALLBACK_EXCEPTION / SENSITIVE_WORD_ERROR
    """
    print(f"[开始轮询] task_id={task_id}, timeout={timeout}s", file=sys.stderr)

    end_time = time.time() + timeout

    while time.time() < end_time:
        result = check_task(task_id)
        if result is None:
            raise Exception("查询失败，请检查网络或 API Key")

        status = result.get("status")
        print(f"[状态] {status}", file=sys.stderr)

        if status in ("SUCCESS", "FIRST_SUCCESS"):
            suno_data = (result.get("response") or {}).get("sunoData") or []
            songs = []
            for item in suno_data:
                songs.append({
                    "audioUrl": item.get("audioUrl", ""),
                    "title": item.get("title", "")
                })
            audio_url = songs[0]["audioUrl"] if songs else ""
            title = songs[0]["title"] if songs else ""
            return {
                "status": status,
                "songs": songs,
                "audio_url": audio_url,
                "title": title
            }

        if status in ("CREATE_TASK_FAILED", "GENERATE_AUDIO_FAILED",
                      "CALLBACK_EXCEPTION", "SENSITIVE_WORD_ERROR"):
            error_msg = result.get("errorMessage") or status
            raise Exception(f"生成失败 [{status}]: {error_msg}")

        # PENDING / TEXT_SUCCESS: 继续轮询
        time.sleep(interval)

    raise TimeoutError(f"任务 {task_id} 超过 {timeout}s 未完成")


def main():
    parser = argparse.ArgumentParser(description="kie.ai Suno API 渐进生成")
    parser.add_argument("--style_tags", required=True, help="Suno 风格标签（≤115字符）")
    parser.add_argument("--lyrics", required=False, default="", help="歌词（含结构标签）")
    parser.add_argument("--title", required=True, help="歌名（≤80字符）")
    parser.add_argument("--model", default="V4_5", help="模型版本（默认 V4_5）")
    parser.add_argument("--instrumental", action="store_true", help="纯音乐模式")
    parser.add_argument("--timeout", type=int, default=300, help="轮询超时（秒）")

    args = parser.parse_args()

    if not API_KEY:
        print("错误: 未设置 KIEAI_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    # 校验 style_tags 长度
    if len(args.style_tags) > 115:
        print(f"警告: style_tags {len(args.style_tags)} 字符 > 115，将被截断", file=sys.stderr)
        args.style_tags = args.style_tags[:115]

    try:
        task_id = submit_generate(
            style_tags=args.style_tags,
            lyrics=args.lyrics,
            title=args.title,
            model=args.model,
            instrumental=args.instrumental
        )

        result = poll_task(task_id, timeout=args.timeout)

        # 输出 JSON 到 stdout（主代理读取）
        output = {
            "success": True,
            "task_id": task_id,
            "status": result["status"],
            "audio_url": result["audio_url"],
            "title": result["title"],
            "songs": result["songs"]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    except Exception as e:
        output = {
            "success": False,
            "error": str(e)
        }
        print(json.dumps(output, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
