#!/usr/bin/env python3
"""图片生成：POST /api/create-task（task_type=image）→ 轮询 /api/tasks/<id> → 下载。

Agent 只需把用户的图片需求原文作为 prompt 传入，引擎/参数由平台 Auto 解析。
如需图生图，先用 upload_file.py 上传参考图得到 URL/asset_id，再经 --reference-image-ids 传入。

⚠️ 提交即扣积分：调用前应先向用户说明预估成本并获确认（见 SKILL.md「积分确认」）。
鉴权：Authorization: Bearer vooai_xxx（AccessKey，需付费会员）。
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import json_output, error_exit, DEFAULT_TASK_TIMEOUT, DEFAULT_TASK_POLL_INTERVAL
from get_task import create_task


def build_image_body(args) -> dict:
    """根据 CLI 参数构建 /api/create-task 图片任务请求体。"""
    body = {
        "prompt": args.prompt,
        "task_type": "image",
    }
    if args.negative_prompt:
        body["negative_prompt"] = args.negative_prompt
    if args.aspect_ratio:
        body["aspect_ratio"] = args.aspect_ratio
    if args.resolution_tier:
        body["resolution_tier"] = args.resolution_tier
    if args.image_size:
        body["image_size"] = args.image_size
    if args.model_type:
        body["model_type"] = args.model_type
    if args.engine_type:
        body["engine_type"] = args.engine_type       # 留空则平台 Auto 选引擎
    if args.quality:
        body["quality"] = args.quality
    if args.style:
        body["style"] = args.style
    if args.reference_image_ids:
        body["reference_image_ids"] = args.reference_image_ids
    return body


def main():
    parser = argparse.ArgumentParser(
        description="VoooAI 图片生成（文生图 / 图生图）",
        epilog="""
环境变量:
  VOOOAI_ACCESS_KEY  必填，Bearer 鉴权（需付费会员）
  VOOOAI_BASE_URL    可选，默认 https://voooai.com

示例:
  # 文生图（最简）
  python3 image_generate.py "一只戴眼镜的橘猫，写实风格"

  # 指定比例与画质，并下载到本地
  python3 image_generate.py "赛博朋克城市夜景" --aspect-ratio 16:9 --quality high --output-dir ./out

  # 图生图（先上传参考图）
  python3 upload_file.py ./ref.png            # → 得到 file_url / file_id
  python3 image_generate.py "把这张草图变成写实图" --reference-image-ids <file_url>

  # 仅提交不等待（稍后用 get_task.py 轮询）
  python3 image_generate.py "产品海报" --no-wait

  # 无凭证演练（打印请求体，不实际调用）
  python3 image_generate.py "测试" --dry-run

注意:
  - 提交即扣积分，调用前应向用户确认成本
  - 引擎留空时平台按 文生图/图生图 自动选择默认引擎
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("prompt", help="图片描述（会原样传递给平台，请勿改写用户意图）")
    parser.add_argument("--negative-prompt", default="", help="负向提示词（可选）")
    parser.add_argument("--aspect-ratio", default="", help="画面比例，如 1:1 / 16:9 / 9:16")
    parser.add_argument("--resolution-tier", default="", help="分辨率档位")
    parser.add_argument("--image-size", default="", help="图片尺寸（向后兼容字段，如 1024x1024）")
    parser.add_argument("--model-type", default="", help="模型类型")
    parser.add_argument("--engine-type", default="", help="指定图片引擎（留空=Auto）")
    parser.add_argument("--quality", default="", help="画质档位 low/medium/high（部分引擎生效）")
    parser.add_argument("--style", default="", help="风格（如 realistic）")
    parser.add_argument("--reference-image-ids", nargs="+", default=[], help="图生图参考图 URL/asset_id 列表")
    parser.add_argument("--output-dir", default="", help="下载目录（非空则下载结果）")
    parser.add_argument("--prefix", default="", help="下载文件名前缀")
    parser.add_argument("--no-wait", action="store_true", help="仅提交，不轮询等待")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TASK_TIMEOUT, help=f"轮询超时秒数（默认 {DEFAULT_TASK_TIMEOUT}）")
    parser.add_argument("--interval", type=int, default=DEFAULT_TASK_POLL_INTERVAL, help=f"轮询间隔秒数（默认 {DEFAULT_TASK_POLL_INTERVAL}）")
    parser.add_argument("--dry-run", action="store_true", help="仅打印请求体，不实际调用（无凭证/CI）")
    args = parser.parse_args()

    prompt = (args.prompt or "").strip()
    if not prompt:
        error_exit("prompt 不能为空")

    body = build_image_body(args)
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
