#!/usr/bin/env python3
"""用 Nano Banana Pro 逐页生成叙事连续的社媒营销图片套组。"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    raise SystemExit("缺少 requests，请运行 pip3 install requests")


API_ROOT = "https://ai-hive.iclip.cn/api/openapi/v1"
MODEL_ID = "public_model_nano_banana_pro"
CONFIG = Path.home() / ".ai-hive" / "config.json"
OUTPUT = Path.home() / "Downloads" / "AiHive"
PLATFORMS = (
    "instagram-carousel", "xiaohongshu", "douyin-graphic", "wechat",
    "linkedin-carousel", "facebook", "pinterest", "tiktok-shop", "other",
)
FRAMES = (
    "hook", "problem", "insight", "proof", "how-to", "feature",
    "comparison", "lifestyle", "offer", "cta",
)
EVIDENCE_FRAMES = {"proof", "comparison"}
IMAGE_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif",
}


def load_key(explicit=None):
    if explicit:
        return explicit
    if os.environ.get("AI_HIVE_API_KEY"):
        return os.environ["AI_HIVE_API_KEY"]
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        value = data.get("api_key")
        if value:
            try:
                if CONFIG.stat().st_mode & 0o077:
                    CONFIG.chmod(0o600)
            except OSError:
                pass
            return value
    except (OSError, ValueError):
        pass
    raise SystemExit(
        "缺少 AI Hive API Key。使用 --api-key、AI_HIVE_API_KEY，"
        "或运行 social_carousel.py auth --api-key sk-api-*"
    )


class CarouselAPI:
    def __init__(self, key, verbose=False):
        self.verbose = verbose
        self.headers = {
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        }

    def request(self, method, path, **kwargs):
        url = API_ROOT + "/" + path.lstrip("/")
        if self.verbose:
            print("[api]", method, url, file=sys.stderr)
        try:
            response = requests.request(
                method, url, headers=self.headers, timeout=30, **kwargs
            )
        except requests.RequestException as exc:
            raise SystemExit("AI Hive 请求失败：" + str(exc))
        if not response.ok:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            raise SystemExit(
                "AI Hive 返回错误 {}：{}".format(response.status_code, detail)
            )
        if response.status_code == 204:
            return None
        return response.json()

    def pricing(self, routing):
        models = self.request("GET", "models", params={"modelType": "IMAGE"})
        model = next(
            (row for row in models if row.get("publicModelId") == MODEL_ID), None
        )
        if model is None:
            raise SystemExit("当前模型列表没有固定能力：" + MODEL_ID)
        snapshot = next(
            (row for row in model.get("pricingSnapshot", [])
             if row.get("routingMode") == routing),
            None,
        )
        if snapshot is None:
            raise SystemExit("Nano Banana Pro 不支持所选路由：" + routing)
        return snapshot

    def upload_ticket(self, path, content_type):
        return self.request(
            "POST", "media/upload-token",
            json={
                "filename": path.name, "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def complete_upload(self, media_id):
        self.request("POST", "media/{}/complete".format(media_id))

    def generate(self, routing, snapshot, prompt, media_ids, batch, params):
        return self.request(
            "POST", "generation/image",
            json={
                "publicModelId": MODEL_ID, "routingMode": routing,
                "prompt": prompt, "batchSize": batch,
                "imageMediaIds": media_ids, "params": params,
                "pricingSnapshot": snapshot,
            },
        )

    def task(self, task_id):
        return self.request("GET", "generation/tasks/" + task_id)


def validate_brief(args):
    if args.total < 2 or args.total > 20:
        raise SystemExit("--total 必须在 2 到 20 之间")
    if args.position < 1 or args.position > args.total:
        raise SystemExit("--position 必须在 1 到 total 之间")
    if args.frame == "hook" and args.position != 1:
        raise SystemExit("hook 必须是第 1 页")
    if args.frame == "cta" and args.position != args.total:
        raise SystemExit("cta 必须是最后一页")
    if args.frame in EVIDENCE_FRAMES and (not args.claim or not args.claim_source):
        raise SystemExit("proof 和 comparison 必须提供 --claim 与 --claim-source")
    if args.claim and not args.claim_source:
        raise SystemExit("使用 --claim 时必须提供 --claim-source")
    if args.commerce and (not args.product_record or not args.source_image):
        raise SystemExit("--commerce 必须提供 --product-record 和商品 --source-image")
    if len(args.source_role or []) != len(args.source_image or []):
        raise SystemExit("每张 --source-image 必须对应一条 --source-role")
    if len(args.source_image or []) > 8:
        raise SystemExit("最多提供 8 张 --source-image")
    if args.batch < 1 or args.batch > 2:
        raise SystemExit("--batch 必须为 1 或 2")


def prompt_for(args):
    roles = "；".join(
        "参考图{}={}".format(i, role)
        for i, role in enumerate(args.source_role or [], 1)
    )
    fields = [
        ("系列编号", args.campaign_id),
        ("页码", "{}/{}".format(args.position, args.total)),
        ("平台", args.platform), ("本页职责", args.frame),
        ("受众", args.audience), ("系列目标", args.campaign_goal),
        ("本页单一信息", args.single_message), ("参考图职责", roles),
        ("商品事实", args.product_record), ("批准宣称", args.claim),
        ("宣称来源", args.claim_source), ("本页视觉动作", args.visual_beat),
        ("跨页锁定", args.series_lock), ("文案与平台预留", args.copy_reserve),
        ("传递给下一页", args.next_handoff), ("排除项", args.exclusions),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；只完成本页职责，不把整套内容塞进一张图；"
        "保持系列的商品或角色身份、配色、镜头、光线、道具密度与图形母题；"
        "参考图各司其职，风格锚点不得改写商品事实；"
        "不得虚构功能、证据、比较、体验、价格、认证、销量、合作或品牌关系；"
        "若生成文字，交付前逐字人工复核；按发布时的平台安全区与披露规则复查"
    )


def source_file(filename):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("图片不存在：" + str(path))
    content_type = IMAGE_TYPES.get(path.suffix.lower())
    if not content_type:
        raise SystemExit("素材必须是 PNG、JPEG、WebP 或 GIF：" + str(path))
    return path, content_type


def upload(api, filename):
    path, content_type = source_file(filename)
    ticket = api.upload_ticket(path, content_type)
    media_id = ticket["mediaId"]
    transfer = ticket["upload"]
    url = transfer["url"]
    if urlparse(url).scheme != "https":
        raise SystemExit("素材上传地址必须使用 HTTPS")
    try:
        with path.open("rb") as handle:
            response = requests.request(
                transfer.get("method", "PUT"), url,
                headers=transfer.get("headers", {}), data=handle, timeout=300,
            )
    except requests.RequestException as exc:
        raise SystemExit("素材上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "素材上传失败 {}：{}".format(response.status_code, response.text)
        )
    api.complete_upload(media_id)
    print("[source]", path.name, "->", media_id)
    return media_id


def parse_params(values):
    result = {}
    for item in values or []:
        if "=" not in item:
            raise SystemExit("--param 必须使用 key=value：" + item)
        key, value = item.split("=", 1)
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        result[key] = value
    return result


def render(args):
    validate_brief(args)
    api = CarouselAPI(load_key(args.api_key), args.verbose)
    snapshot = api.pricing(args.routing)
    media_ids = [upload(api, item) for item in args.source_image]
    response = api.generate(
        args.routing, snapshot, prompt_for(args), media_ids,
        args.batch, parse_params(args.param),
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print(
        "[carousel]", args.campaign_id,
        "{}/{}".format(args.position, args.total), args.frame,
        "taskId =", task_id,
    )
    if not args.no_download:
        wait_and_download(
            api, task_id, Path(args.output_dir),
            args.campaign_id, args.position, args.frame,
        )


def brief(args):
    validate_brief(args)
    print(prompt_for(args))


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "carousel"


def safe_download(url, destination):
    if urlparse(url).scheme != "https":
        raise SystemExit("结果下载地址必须使用 HTTPS")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=300) as response:
            response.raise_for_status()
            with destination.open("wb") as handle:
                for chunk in response.iter_content(8192):
                    if chunk:
                        handle.write(chunk)
    except requests.RequestException as exc:
        raise SystemExit("结果下载失败：" + str(exc))
    print("[saved]", destination)


def wait_and_download(api, task_id, output_dir, campaign_id, position, frame):
    deadline = time.time() + 1200
    task = None
    while time.time() < deadline:
        task = api.task(task_id)
        items = task.get("items", [])
        statuses = [item.get("status", "UNKNOWN") for item in items]
        print("[task]", task_id, ",".join(statuses) or "PENDING")
        if items and all(value in ("COMPLETED", "FAILED") for value in statuses):
            break
        time.sleep(3)
    else:
        raise SystemExit("任务轮询超时；可用 status 命令继续查询")
    stem = "{}_{:02d}_{}".format(
        safe_name(campaign_id), position, safe_name(frame)
    )
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"], output_dir / "{}_{}.png".format(stem, index)
            )


def status(args):
    api = CarouselAPI(load_key(args.api_key), args.verbose)
    print(json.dumps(api.task(args.task_id), ensure_ascii=False, indent=2))


def auth(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    CONFIG.chmod(0o600)
    print("已安全写入", CONFIG)


def brief_flags(parser):
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--platform", choices=PLATFORMS, required=True)
    parser.add_argument("--frame", choices=FRAMES, required=True)
    parser.add_argument("--position", type=int, required=True)
    parser.add_argument("--total", type=int, required=True)
    parser.add_argument("--commerce", action="store_true")
    parser.add_argument("--source-image", nargs="*", default=[])
    parser.add_argument("--source-role", nargs="*", default=[])
    parser.add_argument("--product-record")
    parser.add_argument("--audience", required=True)
    parser.add_argument("--campaign-goal", required=True)
    parser.add_argument("--single-message", required=True)
    parser.add_argument("--claim")
    parser.add_argument("--claim-source")
    parser.add_argument("--visual-beat", required=True)
    parser.add_argument("--series-lock", required=True)
    parser.add_argument("--copy-reserve")
    parser.add_argument("--next-handoff", required=True)
    parser.add_argument("--exclusions")
    parser.add_argument("--batch", type=int, default=1)


def connection_flags(parser):
    parser.add_argument("--api-key")
    parser.add_argument("--verbose", action="store_true")


def build_cli():
    root = argparse.ArgumentParser(
        description="Nano Banana Pro 社媒轮播营销图片套组工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    make = commands.add_parser("render", help="生成系列中的一页")
    brief_flags(make)
    make.add_argument("--param", nargs="*")
    make.add_argument(
        "--routing", choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    make.add_argument("--output-dir", default=str(OUTPUT))
    make.add_argument("--no-download", action="store_true")
    connection_flags(make)
    make.set_defaults(handler=render)

    preview = commands.add_parser("brief", help="只校验并输出本页提示词")
    brief_flags(preview)
    preview.set_defaults(handler=brief)

    task = commands.add_parser("status", help="查询生成任务")
    task.add_argument("--task-id", required=True)
    connection_flags(task)
    task.set_defaults(handler=status)

    save = commands.add_parser("auth", help="保存 AI Hive API Key")
    save.add_argument("--api-key", required=True)
    save.set_defaults(handler=auth)
    return root


def main():
    args = build_cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
