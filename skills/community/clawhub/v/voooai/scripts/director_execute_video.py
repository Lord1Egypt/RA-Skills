#!/usr/bin/env python3
"""编导模式 · 逐分镜出视频（路 B）：POST /api/director/v2/<session_id>/execute_storyboard_video。

直接为某个分镜创建视频生成任务（跳过 LLM），异步执行，返回 task_id。
可用 --poll 轮询任务并下载结果（复用 /api/tasks 任务系统）。

与 director_export.py（路 A：导出整条工作流批量执行）互补：
  - 路 A 适合一次性出全片
  - 路 B 适合单独重出/预览某个分镜的视频

⚠️ 视频生成消耗积分，调用前应向用户确认。
鉴权：Authorization: Bearer vooai_xxx（AccessKey，需付费会员）。
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import (
    http_request, json_output, error_exit, format_business_error,
    poll_task, extract_task_media, DEFAULT_TASK_TIMEOUT, DEFAULT_TASK_POLL_INTERVAL,
    PLATFORM_URL,
)
from _director import require_session
from get_task import download_media

# 视频轮询默认更久
DEFAULT_VIDEO_TIMEOUT = 600


def main():
    parser = argparse.ArgumentParser(
        description="为编导会话中的单个分镜生成视频",
        epilog="""
环境变量:
  VOOOAI_ACCESS_KEY  必填，Bearer 鉴权（需付费会员）
  VOOOAI_BASE_URL    可选，默认 https://voooai.com

示例:
  # 为某分镜出视频（storyboard_id 来自 director_status --full 的分镜数据）
  python3 director_execute_video.py --storyboard-id sb_xxxxxxxx

  # 覆盖引擎与提示词，并轮询下载
  python3 director_execute_video.py --storyboard-id sb_xxxxxxxx --engine evolink_seedance --poll --output-dir ./out

  # 无凭证演练
  python3 director_execute_video.py --storyboard-id sb_xxxxxxxx --dry-run

说明:
  - 返回 task_id 后可单独用 get_task.py <task_id> --poll 查询/下载
  - 提交即创建异步视频任务并消耗积分
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--storyboard-id", required=True, help="分镜 ID（sb_xxx，必填）")
    parser.add_argument("--session-id", default="", help="会话 ID（缺省读状态文件）")
    parser.add_argument("--tab-id", default=None, help="页签 ID（缺省读状态文件）")
    parser.add_argument("--state-file", default="", help="会话状态文件路径")
    parser.add_argument("--engine", default="", help="覆盖视频引擎（可选）")
    parser.add_argument("--prompt", default="", help="覆盖提示词（纯文本，可选）")
    parser.add_argument("--output-format", default="", help="成片封装格式 mp4/mov（默认 mp4）")
    parser.add_argument("--draft-finalize", action="store_true", help="Draft→1080p 成片委托模式")
    parser.add_argument("--draft-task-id", default="", help="样片任务 ID（配合 --draft-finalize）")
    parser.add_argument("--poll", action="store_true", help="提交后轮询任务直到完成")
    parser.add_argument("--output-dir", default="", help="配合 --poll：下载结果到该目录")
    parser.add_argument("--prefix", default="", help="下载文件名前缀")
    parser.add_argument("--timeout", type=int, default=DEFAULT_VIDEO_TIMEOUT, help=f"轮询超时秒数（默认 {DEFAULT_VIDEO_TIMEOUT}）")
    parser.add_argument("--interval", type=int, default=DEFAULT_TASK_POLL_INTERVAL, help=f"轮询间隔秒数（默认 {DEFAULT_TASK_POLL_INTERVAL}）")
    parser.add_argument("--dry-run", action="store_true", help="仅打印请求体，不实际调用（无凭证/CI）")
    args = parser.parse_args()

    storyboard_id = (args.storyboard_id or "").strip()
    if not storyboard_id:
        error_exit("storyboard-id 不能为空")

    session_id, _tab_id = require_session(args)

    body = {"storyboard_id": storyboard_id}
    if args.engine:
        body["engine"] = args.engine
    if args.prompt:
        body["prompt"] = args.prompt
    if args.output_format:
        body["output_format"] = args.output_format
    if args.draft_finalize:
        body["draft_finalize"] = True
    if args.draft_task_id:
        body["draft_task_id"] = args.draft_task_id

    if args.dry_run:
        json_output({"success": True, "dry_run": True,
                     "endpoint": f"POST /api/director/v2/{session_id}/execute_storyboard_video",
                     "request_body": body, "message": "dry-run：未实际提交"})
        return

    print(f"正在为分镜 {storyboard_id} 创建视频任务...", file=sys.stderr)
    code, data = http_request("POST", f"/api/director/v2/{session_id}/execute_storyboard_video",
                              body, timeout=120)
    if code not in (200, 201, 202) or not (isinstance(data, dict) and data.get("success")):
        error_exit(format_business_error(code, data if isinstance(data, dict) else {"message": str(data)}))

    task_id = data.get("task_id", "")
    out = {
        "success": True,
        "session_id": session_id,
        "storyboard_id": storyboard_id,
        "task_id": task_id,
        "video_engine": data.get("video_engine", ""),
        "status": data.get("status", "pending"),
    }

    if args.poll and task_id:
        final_status, task = poll_task(task_id, timeout=args.timeout, interval=args.interval)
        out["status"] = final_status
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
            out["success"] = False
            out["error_message"] = task.get("error_message", "视频生成失败")
        elif final_status == "timeout":
            out["hint"] = f"任务可能仍在执行，请稍后用 get_task.py {task_id} --poll 查询，或到 {PLATFORM_URL} 查看"
    elif not args.poll and task_id:
        out["message"] = f"视频任务已提交（task_id={task_id}），用 get_task.py {task_id} --poll 查询进度"

    json_output(out)
    if not out.get("success", True):
        sys.exit(1)


if __name__ == "__main__":
    main()
