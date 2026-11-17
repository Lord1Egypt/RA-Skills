#!/usr/bin/env python3
"""用 Seedance 2.5 生成可追溯的电商 Listing/PDP 模块短片。"""

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
CONFIG = Path.home() / ".ai-hive" / "config.json"
OUTPUT = Path.home() / "Downloads" / "AiHive"
I2V_MODEL = "public_model_seedance_2_5_i2v"
R2V_MODEL = "public_model_seedance_2_5_r2v"
PLATFORMS = (
    "taobao", "tmall", "jd", "pinduoduo", "douyin-shop", "xiaohongshu-shop",
    "kuaishou-shop", "wechat-shop", "amazon", "tiktok-shop", "shopify",
    "temu", "shopee", "lazada", "aliexpress", "other",
)
MODULES = (
    "in-box", "dimension", "compatibility", "assembly", "use-step", "material",
    "variant", "care", "feature-proof",
)
STEP_MODULES = ("assembly", "use-step", "care")
IMAGE_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif",
}
VIDEO_TYPES = {
    ".mp4": "video/mp4", ".mov": "video/quicktime", ".webm": "video/webm",
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
        "或运行 listing_clips.py auth --api-key sk-api-*"
    )


class ListingAPI:
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

    def pricing(self, model_id, routing):
        models = self.request("GET", "models", params={"modelType": "VIDEO"})
        model = next(
            (row for row in models if row.get("publicModelId") == model_id), None
        )
        if model is None:
            raise SystemExit("当前模型列表没有固定能力：" + model_id)
        snapshot = next(
            (row for row in model.get("pricingSnapshot", [])
             if row.get("routingMode") == routing),
            None,
        )
        if snapshot is None:
            raise SystemExit("固定模型不支持所选路由：" + routing)
        return snapshot

    def upload_ticket(self, path, content_type):
        return self.request(
            "POST", "media/upload-token",
            json={
                "filename": path.name,
                "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def complete_upload(self, media_id):
        self.request("POST", "media/{}/complete".format(media_id))

    def generate(self, model_id, routing, snapshot, prompt, images, videos,
                 params, first_frame=None):
        body = {
            "publicModelId": model_id,
            "routingMode": routing,
            "prompt": prompt,
            "imageMediaIds": images,
            "videoMediaIds": videos,
            "audioMediaIds": [],
            "params": params,
            "pricingSnapshot": snapshot,
        }
        if first_frame:
            body["firstFrameMediaId"] = first_frame
        return self.request("POST", "generation/video", json=body)

    def task(self, task_id):
        return self.request("GET", "generation/tasks/" + task_id)


def validate_id(value, flag):
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", value):
        raise SystemExit(flag + " 只能包含字母、数字、点、下划线和连字符")


def validate(args):
    validate_id(args.listing_id, "--listing-id")
    validate_id(args.slot_id, "--slot-id")
    if not args.product_source or len(args.product_source) > 8:
        raise SystemExit("必须提供 1 到 8 张批准的商品事实图")
    if len(args.product_source) != len(args.product_role):
        raise SystemExit("每张 --product-source 必须对应一条 --product-role")
    if len(args.continuity_lock) < 5:
        raise SystemExit("每个Listing短片至少提供 5 条 --continuity-lock")
    if args.module == "in-box" and not args.included_count:
        raise SystemExit("in-box 模块必须提供 --included-count")
    if args.module == "compatibility" and not args.compatibility_basis:
        raise SystemExit("compatibility 模块必须提供 --compatibility-basis")
    if args.module in STEP_MODULES:
        if args.step_number is None or args.step_total is None:
            raise SystemExit("assembly/use-step/care 必须提供步骤编号与总数")
        if not 1 <= args.step_number <= args.step_total <= 20:
            raise SystemExit("步骤必须满足 1 <= step-number <= step-total <= 20")
    elif args.step_number is not None or args.step_total is not None:
        raise SystemExit("只有 assembly/use-step/care 可以提供步骤编号")


def clip_prompt(args):
    roles = "；".join(
        "商品事实图{}={}".format(index, role)
        for index, role in enumerate(args.product_role, 1)
    )
    step = None
    if args.step_number is not None:
        step = "第{}/{}步".format(args.step_number, args.step_total)
    fields = [
        ("Listing", args.listing_id), ("槽位", args.slot_id),
        ("平台", args.platform), ("模块", args.module),
        ("交付规格", args.delivery), ("目标购买者", args.shopper),
        ("购买问题", args.shopper_question), ("视觉回答", args.visual_answer),
        ("SKU主档", args.sku_record), ("商品事实素材", roles),
        ("本模块事实", args.fact), ("事实批准来源", args.fact_source),
        ("随箱数量", args.included_count),
        ("兼容性依据", args.compatibility_basis), ("步骤", step),
        ("起始状态", args.start_state), ("唯一动作", args.action),
        ("结束状态", args.end_state), ("相机", args.camera),
        ("跨槽位连续性", "；".join(args.continuity_lock)),
        ("后期文字地图", args.overlay_map), ("平台规则保护", args.policy_guard),
        ("排除项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；只生成这个Listing/PDP槽位的单一事实短片，不补齐整条带货视频或品牌片；"
        "画面只能回答指定购买问题，不加入情绪Hook、促销、竞品对比或额外卖点；"
        "商品、包装、配件、数量、尺寸、接口、材质、颜色、兼容性和步骤以批准来源为准；"
        "不得用视觉效果暗示未批准性能，不得展示未提供的内部结构；"
        "尺寸线、单位、步骤、价格、声明、标签和CTA使用批准稿后期排版，画面内不自动生字；"
        "开头和结尾保持稳定，便于详情页自动播放、循环和人工加信息层"
    )


def typed_file(filename, kind):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("素材不存在：" + str(path))
    table = IMAGE_TYPES if kind == "image" else VIDEO_TYPES
    content_type = table.get(path.suffix.lower())
    if content_type is None:
        raise SystemExit("{}素材格式不支持：{}".format(kind, path))
    return path, content_type


def upload(api, filename, kind):
    path, content_type = typed_file(filename, kind)
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
            value = json.loads(value)
        except json.JSONDecodeError:
            pass
        result[key] = value
    return result


def run_clip(args):
    validate(args)
    prompt = clip_prompt(args)
    params = parse_params(args.param)
    model_id = R2V_MODEL if args.motion_reference else I2V_MODEL
    if args.preview:
        print(json.dumps({
            "publicModelId": model_id,
            "listingId": args.listing_id,
            "slotId": args.slot_id,
            "module": args.module,
            "prompt": prompt,
            "productSources": args.product_source,
            "motionReference": args.motion_reference,
            "firstFrame": None if args.motion_reference else args.product_source[0],
            "params": params,
        }, ensure_ascii=False, indent=2))
        return
    api = ListingAPI(load_key(args.api_key), args.verbose)
    snapshot = api.pricing(model_id, args.routing)
    image_ids = [upload(api, item, "image") for item in args.product_source]
    if args.motion_reference:
        videos = [upload(api, args.motion_reference, "video")]
        request_images = image_ids
        first_frame = None
    else:
        videos = []
        request_images = image_ids[1:]
        first_frame = image_ids[0]
    response = api.generate(
        model_id, args.routing, snapshot, prompt, request_images, videos,
        params, first_frame,
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[listing-clip]", args.listing_id, args.slot_id, "taskId =", task_id)
    if not args.no_download:
        wait_and_download(
            api, task_id, Path(args.output_dir), args.listing_id, args.slot_id
        )


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "slot"


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


def wait_and_download(api, task_id, output_dir, listing_id, slot_id):
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
        raise SystemExit("任务轮询超时；请用 status 查询原 taskId")
    stem = "{}-{}".format(safe_name(listing_id), safe_name(slot_id))
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"], output_dir / "{}-{}.mp4".format(stem, index)
            )


def status(args):
    api = ListingAPI(load_key(args.api_key), args.verbose)
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


def build_cli():
    root = argparse.ArgumentParser(description="Seedance 2.5 电商Listing模块短片")
    commands = root.add_subparsers(dest="command", required=True)

    clip = commands.add_parser("clip", help="生成一个回答单一购买问题的Listing短片")
    clip.add_argument("--listing-id", required=True)
    clip.add_argument("--slot-id", required=True)
    clip.add_argument("--platform", choices=PLATFORMS, required=True)
    clip.add_argument("--module", choices=MODULES, required=True)
    clip.add_argument("--delivery", required=True)
    clip.add_argument("--shopper", required=True)
    clip.add_argument("--shopper-question", required=True)
    clip.add_argument("--visual-answer", required=True)
    clip.add_argument("--sku-record", required=True)
    clip.add_argument("--product-source", nargs="+", required=True)
    clip.add_argument("--product-role", nargs="+", required=True)
    clip.add_argument("--fact", required=True)
    clip.add_argument("--fact-source", required=True)
    clip.add_argument("--included-count")
    clip.add_argument("--compatibility-basis")
    clip.add_argument("--step-number", type=int)
    clip.add_argument("--step-total", type=int)
    clip.add_argument("--start-state", required=True)
    clip.add_argument("--action", required=True)
    clip.add_argument("--end-state", required=True)
    clip.add_argument("--camera", required=True)
    clip.add_argument("--continuity-lock", action="append", required=True)
    clip.add_argument("--overlay-map", required=True)
    clip.add_argument("--policy-guard", required=True)
    clip.add_argument("--reject")
    clip.add_argument("--motion-reference")
    clip.add_argument("--preview", action="store_true")
    clip.add_argument("--param", action="append")
    clip.add_argument(
        "--routing", choices=("COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"),
        default="COST_FIRST",
    )
    clip.add_argument("--output-dir", default=str(OUTPUT))
    clip.add_argument("--no-download", action="store_true")
    clip.add_argument("--api-key")
    clip.add_argument("--verbose", action="store_true")
    clip.set_defaults(handler=run_clip)

    task = commands.add_parser("status", help="查询生成任务")
    task.add_argument("--task-id", required=True)
    task.add_argument("--api-key")
    task.add_argument("--verbose", action="store_true")
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
