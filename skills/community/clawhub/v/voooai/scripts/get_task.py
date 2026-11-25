#!/usr/bin/env python3
"""图片/视频生成任务：提交、查询、轮询、下载、取消。

图片生成与视频生成统一走任务系统：
  1. POST /api/create-task  — 提交任务（task_type=image|video），立即扣积分，返回 task_id
  2. GET  /api/tasks/<id>   — 轮询任务状态与结果（image_url/video_url/audio_url）
  3. PATCH /api/tasks/<id>/cancel — 取消未完成任务

本文件既可作为独立 CLI（查询/下载/取消已有任务），也向 image_generate.py /
video_generate.py 暴露共享助手：create_task() 与 download_media()。

鉴权：Authorization: Bearer vooai_xxx（AccessKey，需付费会员）。
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _common import (
    http_request,
    poll_task,
    extract_task_media,
    format_business_error,
    json_output,
    error_exit,
    DEFAULT_TASK_TIMEOUT,
    DEFAULT_TASK_POLL_INTERVAL,
    PLATFORM_URL,
)
# 复用 node-builder 下载脚本的并行下载工具（同目录）
from download_results import download_file, get_extension_from_url


# ── 共享助手 ────────────────────────────────────────────────────────────────
def download_media(media: list, output_dir: str, prefix: str = "") -> dict:
    """
    下载 extract_task_media() 产出的媒体列表到本地。

    Args:
        media: [{'type': 'image|video|audio', 'url': str}, ...]
        output_dir: 输出目录（不存在则创建）
        prefix: 文件名前缀（如 'poster' → poster_01.png）

    Returns:
        {'downloaded_files': [路径...], 'errors': [{file,url,error}...]}
    """
    os.makedirs(output_dir, exist_ok=True)
    downloaded, errors = [], []
    for i, item in enumerate(media, 1):
        url = item.get("url", "")
        if not url:
            continue
        ext = get_extension_from_url(url, ".bin")
        name = f"{prefix}_{i:02d}{ext}" if prefix else f"{i:02d}{ext}"
        filepath = os.path.join(output_dir, name)
        fp, err = download_file(url, filepath)
        if err:
            errors.append({"file": fp, "url": url, "error": err})
            print(f"✗ 下载失败: {os.path.basename(filepath)}", file=sys.stderr)
        else:
            downloaded.append(fp)
            print(f"✓ 已下载: {os.path.basename(filepath)}", file=sys.stderr)
    return {"downloaded_files": downloaded, "errors": errors}


def create_task(body: dict, wait: bool = True, timeout: int = DEFAULT_TASK_TIMEOUT,
                interval: int = DEFAULT_TASK_POLL_INTERVAL, output_dir: str = "",
                prefix: str = "", dry_run: bool = False) -> dict:
    """
    提交 /api/create-task 任务，按需轮询与下载，返回统一结果字典。

    Args:
        body: create-task 请求体（须含 prompt 与 task_type）
        wait: 是否轮询直到完成（False 时提交后立即返回 task_id）
        timeout/interval: 轮询超时与间隔
        output_dir: 非空则下载结果到该目录
        prefix: 下载文件名前缀
        dry_run: 仅打印将发送的请求，不实际调用（无凭证/CI 场景）

    Returns:
        {'success': bool, 'task_id': str, 'status': str, 'media': [...],
         'points_deducted': n, 'remaining_points': n, ...}
    """
    if dry_run:
        return {
            "success": True,
            "dry_run": True,
            "endpoint": "POST /api/create-task",
            "request_body": body,
            "message": "dry-run：未实际提交任务",
        }

    print(f"正在提交 {body.get('task_type', 'image')} 生成任务...", file=sys.stderr)
    status_code, data = http_request("POST", "/api/create-task", body, timeout=60)

    if status_code not in (200, 201, 202) or not data.get("success"):
        error_exit(format_business_error(status_code, data))

    task_id = data.get("task_id", "")
    out = {
        "success": True,
        "task_id": task_id,
        "status": data.get("status", "pending"),
        "points_deducted": data.get("points_deducted"),
        "remaining_points": data.get("remaining_points"),
        "remaining_extra_credits": data.get("remaining_extra_credits"),
    }

    if not wait:
        out["message"] = f"任务已提交（task_id={task_id}），使用 get_task.py {task_id} --poll 查询进度"
        return out

    # 轮询直到完成
    final_status, task = poll_task(task_id, timeout=timeout, interval=interval)
    out["status"] = final_status

    if final_status == "completed":
        media = extract_task_media(task)
        out["media"] = media
        out["result_urls"] = [m["url"] for m in media]
        if output_dir:
            dl = download_media(media, output_dir, prefix)
            out["output_dir"] = output_dir
            out["downloaded_files"] = dl["downloaded_files"]
            if dl["errors"]:
                out["download_errors"] = dl["errors"]
    elif final_status == "failed":
        out["success"] = False
        out["error_message"] = task.get("error_message", "任务执行失败")
    elif final_status == "cancelled":
        out["success"] = False
        out["message"] = "任务已取消"
    elif final_status == "timeout":
        out["success"] = False
        out["hint"] = f"任务可能仍在执行中，请稍后用 get_task.py {task_id} 查询，或到 {PLATFORM_URL} 查看"

    return out


# ── CLI ─────────────────────────────────────────────────────────────────────
def cancel_task(task_id: str) -> dict:
    """取消任务：PATCH /api/tasks/<id>/cancel"""
    status_code, data = http_request("PATCH", f"/api/tasks/{task_id}/cancel")
    if status_code not in (200, 202) or not (isinstance(data, dict) and data.get("success", True) is not False):
        return {"success": False, "error": format_business_error(status_code, data)}
    return {"success": True, "task_id": task_id, "status": "cancelled", "raw": data}


def main():
    parser = argparse.ArgumentParser(
        description="查询/下载/取消 VoooAI 图片·视频生成任务",
        epilog="""
环境变量:
  VOOOAI_ACCESS_KEY  必填，Bearer 鉴权（需付费会员）
  VOOOAI_BASE_URL    可选，默认 https://voooai.com

示例:
  # 单次查询任务状态
  python3 get_task.py <task_id>

  # 轮询直到完成
  python3 get_task.py <task_id> --poll

  # 轮询并下载结果到目录
  python3 get_task.py <task_id> --poll --output-dir ./output --prefix poster

  # 取消任务
  python3 get_task.py <task_id> --cancel

任务结果字段:
  task.status ∈ pending | processing | completed | failed | cancelled
  task.image_url / video_url / audio_url  按媒体类型分字段返回
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("task_id", help="任务 ID（由 image_generate.py / video_generate.py 返回）")
    parser.add_argument("--poll", action="store_true", help="轮询直到完成或超时")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TASK_TIMEOUT, help=f"轮询超时秒数（默认 {DEFAULT_TASK_TIMEOUT}）")
    parser.add_argument("--interval", type=int, default=DEFAULT_TASK_POLL_INTERVAL, help=f"轮询间隔秒数（默认 {DEFAULT_TASK_POLL_INTERVAL}）")
    parser.add_argument("--output-dir", default="", help="下载目录（非空则下载结果）")
    parser.add_argument("--prefix", default="", help="下载文件名前缀")
    parser.add_argument("--cancel", action="store_true", help="取消该任务")
    args = parser.parse_args()

    task_id = args.task_id.strip()
    if not task_id:
        error_exit("task_id 不能为空")

    if args.cancel:
        json_output(cancel_task(task_id))
        return

    if args.poll:
        final_status, task = poll_task(task_id, timeout=args.timeout, interval=args.interval)
        out = {"success": final_status == "completed", "task_id": task_id, "status": final_status}
        if final_status == "completed":
            media = extract_task_media(task)
            out["media"] = media
            out["result_urls"] = [m["url"] for m in media]
            if args.output_dir:
                dl = download_media(media, args.output_dir, args.prefix)
                out["output_dir"] = args.output_dir
                out["downloaded_files"] = dl["downloaded_files"]
                if dl["errors"]:
                    out["download_errors"] = dl["errors"]
        elif final_status == "failed":
            out["error_message"] = task.get("error_message", "任务执行失败")
        elif final_status == "timeout":
            out["hint"] = f"任务可能仍在执行中，请稍后重试或到 {PLATFORM_URL} 查看"
        json_output(out)
        if not out.get("success"):
            sys.exit(1)
        return

    # 单次查询
    status_code, data = http_request("GET", f"/api/tasks/{task_id}")
    if status_code != 200 or not (isinstance(data, dict) and data.get("success")):
        error_exit(format_business_error(status_code, data))
    task = data.get("task", {}) or {}
    out = {
        "success": True,
        "task_id": task_id,
        "status": task.get("status", "unknown"),
        "media_type": task.get("media_type") or task.get("task_type"),
        "engine_type": task.get("engine_type"),
    }
    media = extract_task_media(task)
    if media:
        out["media"] = media
        out["result_urls"] = [m["url"] for m in media]
    if task.get("error_message"):
        out["error_message"] = task["error_message"]
    json_output(out)


if __name__ == "__main__":
    main()
