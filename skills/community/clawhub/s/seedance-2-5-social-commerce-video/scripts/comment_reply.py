#!/usr/bin/env python3
"""用 Seedance 2.5 把社交电商问题变成可追溯回复短片。"""

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
    "douyin", "xiaohongshu", "kuaishou", "wechat-channels", "bilibili",
    "instagram-reels", "tiktok-shop", "youtube-shorts", "facebook", "other",
)
INTENTS = (
    "sizing", "compatibility", "how-to", "in-box", "material", "color",
    "price", "availability", "care", "objection", "other",
)
PERMISSIONS = ("public-comment", "customer-provided", "synthetic-question")
TIME_SENSITIVE = ("price", "availability")
SCOPE_SENSITIVE = ("sizing", "compatibility")
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
        "或运行 comment_reply.py auth --api-key sk-api-*"
    )


class ReplyAPI:
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
    validate_id(args.thread_id, "--thread-id")
    validate_id(args.reply_id, "--reply-id")
    if not args.product_source or len(args.product_source) > 8:
        raise SystemExit("必须提供 1 到 8 张批准的商品事实图")
    if len(args.product_source) != len(args.product_role):
        raise SystemExit("每张 --product-source 必须对应一条 --product-role")
    if len(args.continuity_lock) < 5:
        raise SystemExit("回复短片至少提供 5 条 --continuity-lock")
    if args.intent in TIME_SENSITIVE and not (args.market and args.valid_until):
        raise SystemExit("price/availability 必须提供 --market 与 --valid-until")
    if args.intent in SCOPE_SENSITIVE and not args.scope_limit:
        raise SystemExit("sizing/compatibility 必须提供 --scope-limit")
    if args.permission == "public-comment" and not args.privacy_redaction:
        raise SystemExit("public-comment 必须说明 --privacy-redaction")
    if args.permission == "synthetic-question" and args.comment_source != "synthetic":
        raise SystemExit("synthetic-question 的 --comment-source 必须为 synthetic")


def reply_prompt(args):
    sources = "；".join(
        "商品事实图{}={}".format(index, role)
        for index, role in enumerate(args.product_role, 1)
    )
    fields = [
        ("互动线程", args.thread_id), ("回复", args.reply_id),
        ("平台", args.platform), ("问题权限", args.permission),
        ("原问题", args.question), ("问题来源", args.comment_source),
        ("隐私处理", args.privacy_redaction), ("问题意图", args.intent),
        ("目标受众", args.audience), ("批准答案", args.answer),
        ("答案来源", args.answer_source), ("适用范围", args.scope_limit),
        ("市场", args.market), ("有效期", args.valid_until),
        ("商品事实素材", sources), ("商业披露", args.disclosure_plan),
        ("回复结构", args.reply_structure), ("可视证据动作", args.proof_action),
        ("起始状态", args.start_state), ("相机", args.camera),
        ("结束状态", args.end_state),
        ("连续性锁定", "；".join(args.continuity_lock)),
        ("字幕与界面安全", args.caption_safe), ("平台合规", args.commerce_safe),
        ("排除项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；这是对一个真实或明确标注为合成的问题的单条回复，不生成整支带货广告；"
        "先承接问题，再只展示一个批准答案和一个可视动作，结尾回到商品；"
        "不得暴露用户名、头像、订单、联系方式、地址或其他个人信息；"
        "商品、包装、数量、尺寸、兼容性、材质、颜色、价格和库存只能来自批准来源；"
        "不得把模型画面当作测试证据，不得扩大答案适用范围；"
        "商业合作、赠品、联盟链接或品牌身份按披露计划由后期叠加；"
        "画面内不自动生成评论截图、价格、日期、标签、CTA、字幕或平台界面"
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


def run_reply(args):
    validate(args)
    prompt = reply_prompt(args)
    params = parse_params(args.param)
    model_id = R2V_MODEL if args.motion_reference else I2V_MODEL
    if args.preview:
        print(json.dumps({
            "publicModelId": model_id,
            "threadId": args.thread_id,
            "replyId": args.reply_id,
            "intent": args.intent,
            "prompt": prompt,
            "productSources": args.product_source,
            "motionReference": args.motion_reference,
            "firstFrame": None if args.motion_reference else args.product_source[0],
            "params": params,
        }, ensure_ascii=False, indent=2))
        return
    api = ReplyAPI(load_key(args.api_key), args.verbose)
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
    print("[comment-reply]", args.thread_id, args.reply_id, "taskId =", task_id)
    if not args.no_download:
        wait_and_download(
            api, task_id, Path(args.output_dir), args.thread_id, args.reply_id
        )


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "reply"


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


def wait_and_download(api, task_id, output_dir, thread_id, reply_id):
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
    stem = "{}-{}".format(safe_name(thread_id), safe_name(reply_id))
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"], output_dir / "{}-{}.mp4".format(stem, index)
            )


def status(args):
    api = ReplyAPI(load_key(args.api_key), args.verbose)
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
    root = argparse.ArgumentParser(description="Seedance 2.5 社交电商评论回复短片")
    commands = root.add_subparsers(dest="command", required=True)

    reply = commands.add_parser("reply", help="把一个问题变成可追溯回复短片")
    reply.add_argument("--thread-id", required=True)
    reply.add_argument("--reply-id", required=True)
    reply.add_argument("--platform", choices=PLATFORMS, required=True)
    reply.add_argument("--permission", choices=PERMISSIONS, required=True)
    reply.add_argument("--question", required=True)
    reply.add_argument("--comment-source", required=True)
    reply.add_argument("--privacy-redaction")
    reply.add_argument("--intent", choices=INTENTS, required=True)
    reply.add_argument("--audience", required=True)
    reply.add_argument("--answer", required=True)
    reply.add_argument("--answer-source", required=True)
    reply.add_argument("--scope-limit")
    reply.add_argument("--market")
    reply.add_argument("--valid-until")
    reply.add_argument("--product-source", nargs="+", required=True)
    reply.add_argument("--product-role", nargs="+", required=True)
    reply.add_argument("--disclosure-plan", required=True)
    reply.add_argument("--reply-structure", required=True)
    reply.add_argument("--proof-action", required=True)
    reply.add_argument("--start-state", required=True)
    reply.add_argument("--camera", required=True)
    reply.add_argument("--end-state", required=True)
    reply.add_argument("--continuity-lock", action="append", required=True)
    reply.add_argument("--caption-safe", required=True)
    reply.add_argument("--commerce-safe", required=True)
    reply.add_argument("--reject")
    reply.add_argument("--motion-reference")
    reply.add_argument("--preview", action="store_true")
    reply.add_argument("--param", action="append")
    reply.add_argument(
        "--routing", choices=("COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"),
        default="COST_FIRST",
    )
    reply.add_argument("--output-dir", default=str(OUTPUT))
    reply.add_argument("--no-download", action="store_true")
    reply.add_argument("--api-key")
    reply.add_argument("--verbose", action="store_true")
    reply.set_defaults(handler=run_reply)

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
