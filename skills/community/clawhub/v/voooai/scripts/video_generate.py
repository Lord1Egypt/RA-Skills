#!/usr/bin/env python3
"""视频生成：POST /api/create-task（task_type=video）→ 轮询 /api/tasks/<id> → 下载。

支持文生视频、图生视频、参考视频/音频驱动。Agent 把用户需求原文作为 prompt 传入，
引擎/参数由平台 Auto 解析；如需指定引擎或时长，用对应选项覆盖。

⚠️ 提交即扣积分（视频通常成本较高）：调用前应先向用户说明预估成本并获确认。
鉴权：Authorization: Bearer vooai_xxx（AccessKey，需付费会员）。
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import json_output, error_exit, DEFAULT_TASK_TIMEOUT, DEFAULT_TASK_POLL_INTERVAL
from get_task import create_task

# 视频轮询默认更久（视频生成比图片慢）
DEFAULT_VIDEO_TIMEOUT = 600


def build_video_body(args) -> dict:
    """根据 CLI 参数构建 /api/create-task 视频任务请求体。"""
    body = {
        "prompt": args.prompt,
        "task_type": "video",
    }
    if args.negative_prompt:
        body["negative_prompt"] = args.negative_prompt
    if args.video_aspect_ratio:
        body["video_aspect_ratio"] = args.video_aspect_ratio
    if args.video_duration:
        body["video_duration"] = args.video_duration
    if args.video_size:
        body["video_size"] = args.video_size
    if args.video_engine_type:
        body["video_engine_type"] = args.video_engine_type   # 留空则平台 Auto 选引擎
    if args.generation_type:
        body["generation_type"] = args.generation_type       # TEXT / FIRST&LAST / REFERENCE
    if args.reference_image_ids:
        body["reference_image_ids"] = args.reference_image_ids
    if args.reference_video_ids:
        body["reference_video_ids"] = args.reference_video_ids
    if args.reference_audio_ids:
        body["reference_audio_ids"] = args.reference_audio_ids
    return body


def main():
    parser = argparse.ArgumentParser(
        description="VoooAI 视频生成（文生视频 / 图生视频 / 参考驱动）",
        epilog="""
环境变量:
  VOOOAI_ACCESS_KEY  必填，Bearer 鉴权（需付费会员）
  VOOOAI_BASE_URL    可选，默认 https://voooai.com

示例:
  # 文生视频（最简）
  python3 video_generate.py "一只机器人在跳舞，霓虹灯背景"

  # 图生视频（先上传参考图）
  python3 upload_file.py ./first.png         # → 得到 file_url
  python3 video_generate.py "让这张图动起来" --reference-image-ids <file_url>

  # 指定时长/比例/引擎并下载
  python3 video_generate.py "咖啡产品广告" --video-duration 8 --video-aspect-ratio 16:9 --output-dir ./out

  # 仅提交不等待（视频较慢，可稍后轮询）
  python3 video_generate.py "海浪拍打礁石" --no-wait
  python3 get_task.py <task_id> --poll --timeout 600

  # 无凭证演练
  python3 video_generate.py "测试" --dry-run

生成类型 (--generation-type):
  TEXT         文生视频（默认）
  FIRST&LAST   首尾帧
  REFERENCE    参考驱动

注意:
  - 提交即扣积分，视频成本较高，调用前务必向用户确认
  - 引擎留空时平台按 文生视频/图生视频 自动选择默认引擎
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("prompt", help="视频描述（会原样传递给平台，请勿改写用户意图）")
    parser.add_argument("--negative-prompt", default="", help="负向提示词（可选）")
    parser.add_argument("--video-aspect-ratio", default="", help="视频比例，如 16:9 / 9:16 / 1:1")
    parser.add_argument("--video-duration", default="", help="视频时长（秒）")
    parser.add_argument("--video-size", default="", help="视频尺寸/清晰度，如 480p / 720p / 1080p")
    parser.add_argument("--video-engine-type", default="", help="指定视频引擎（留空=Auto）")
    parser.add_argument("--generation-type", default="", help="生成类型 TEXT / FIRST&LAST / REFERENCE")
    parser.add_argument("--reference-image-ids", nargs="+", default=[], help="参考图 URL/asset_id 列表（图生视频）")
    parser.add_argument("--reference-video-ids", nargs="+", default=[], help="参考视频 URL/asset_id 列表")
    parser.add_argument("--reference-audio-ids", nargs="+", default=[], help="参考音频 URL/asset_id 列表")
    parser.add_argument("--output-dir", default="", help="下载目录（非空则下载结果）")
    parser.add_argument("--prefix", default="", help="下载文件名前缀")
    parser.add_argument("--no-wait", action="store_true", help="仅提交，不轮询等待")
    parser.add_argument("--timeout", type=int, default=DEFAULT_VIDEO_TIMEOUT, help=f"轮询超时秒数（默认 {DEFAULT_VIDEO_TIMEOUT}）")
    parser.add_argument("--interval", type=int, default=DEFAULT_TASK_POLL_INTERVAL, help=f"轮询间隔秒数（默认 {DEFAULT_TASK_POLL_INTERVAL}）")
    parser.add_argument("--dry-run", action="store_true", help="仅打印请求体，不实际调用（无凭证/CI）")
    args = parser.parse_args()

    prompt = (args.prompt or "").strip()
    if not prompt:
        error_exit("prompt 不能为空")

    body = build_video_body(args)
    result = create_task(
        body,
        wait=not args.no_wait,
        timeout=args.timeout,
        interval=args.interval,
        output_dir=args.output_dir,
        prefix=args.prefix,
        dry_run=args.dry_run,
    )
    json_output(result)
    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
