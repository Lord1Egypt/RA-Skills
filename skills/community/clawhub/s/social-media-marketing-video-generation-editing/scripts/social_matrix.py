#!/usr/bin/env python3
"""用 Seedance 2.5 建立可追溯的社媒视频版本矩阵。"""

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
HOOK_MODEL = "public_model_seedance_2_5_r2v"
ADAPT_MODEL = "public_model_seedance_2_5_video_edit"
TAIL_MODEL = "public_model_seedance_2_5_video_extend"
PLATFORMS = (
    "douyin", "xiaohongshu", "wechat-channels", "kuaishou", "weibo",
    "bilibili", "instagram-reels", "instagram-feed", "tiktok",
    "youtube-shorts", "facebook", "linkedin", "pinterest", "other",
)
OBJECTIVES = (
    "awareness", "engagement", "traffic", "conversion", "retargeting",
    "community", "launch",
)
TAIL_JOBS = ("loop", "cta-hold", "disclaimer-hold")
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
        "或运行 social_matrix.py auth --api-key sk-api-*"
    )


class SocialAPI:
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

    def generate(self, model_id, routing, snapshot, prompt, images, videos, params):
        return self.request(
            "POST", "generation/video",
            json={
                "publicModelId": model_id,
                "routingMode": routing,
                "prompt": prompt,
                "imageMediaIds": images,
                "videoMediaIds": videos,
                "audioMediaIds": [],
                "params": params,
                "pricingSnapshot": snapshot,
            },
        )

    def task(self, task_id):
        return self.request("GET", "generation/tasks/" + task_id)


def validate_id(value, flag):
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", value):
        raise SystemExit(flag + " 只能包含字母、数字、点、下划线和连字符")


def validate_identity(args):
    validate_id(args.campaign_id, "--campaign-id")
    validate_id(args.variant_id, "--variant-id")


def validate_brand_sources(files, roles):
    if not files or len(files) > 8:
        raise SystemExit("必须提供 1 到 8 张批准的品牌或主体事实图")
    if len(files) != len(roles):
        raise SystemExit("每张 --brand-source 必须对应一条 --brand-role")


def validate_adapt(args):
    validate_identity(args)
    validate_brand_sources(args.brand_source, args.brand_role)
    if len(args.must_keep) < 2:
        raise SystemExit("adapt 至少提供 2 条 --must-keep")
    if len(args.may_trim) < 1:
        raise SystemExit("adapt 至少提供 1 条 --may-trim")
    if len(args.invariant) < 4:
        raise SystemExit("adapt 至少提供 4 条 --invariant")
    if args.hook_deadline <= 0:
        raise SystemExit("--hook-deadline 必须大于 0")


def adapt_prompt(args):
    roles = "；".join(
        "批准事实图{}={}".format(index, role)
        for index, role in enumerate(args.brand_role, 1)
    )
    fields = [
        ("Campaign", args.campaign_id), ("渠道版本", args.variant_id),
        ("平台", args.platform), ("目标", args.objective),
        ("目标受众", args.audience), ("唯一信息", args.one_message),
        ("信息批准来源", args.campaign_source), ("品牌事实素材", roles),
        ("交付格式", args.format), ("目标时长", args.target_duration),
        ("Hook截止", "{}秒前".format(args.hook_deadline)),
        ("必须保留", "；".join(args.must_keep)),
        ("允许删减", "；".join(args.may_trim)),
        ("品牌不变量", "；".join(args.invariant)),
        ("重构逻辑", args.edit_logic), ("字幕计划", args.caption_plan),
        ("CTA计划", args.cta_plan), ("平台安全区", args.safe_zone),
        ("排除项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；源视频是已批准母版，只把它重构成这个单一渠道版本；"
        "允许重新取景、调整节奏和镜头顺序，但不得自动发明新场景、新人物或新主张；"
        "保留品牌、人物、产品、Logo、活动事实和因果关系；"
        "所有字幕、价格、日期、声明、标签与平台按钮由后期使用批准稿排版；"
        "不得为了填满画幅拉伸主体或把横屏母版简单中心裁切"
    )


def validate_hook(args):
    validate_identity(args)
    validate_brand_sources(args.brand_source, args.brand_role)
    if len(args.inherit) < 4:
        raise SystemExit("hook 至少提供 4 条 --inherit")
    if args.hook_seconds <= 0 or args.hook_seconds > 5:
        raise SystemExit("--hook-seconds 必须大于 0 且不超过 5")


def hook_prompt(args):
    roles = "；".join(
        "品牌事实图{}={}".format(index, role)
        for index, role in enumerate(args.brand_role, 2)
    )
    fields = [
        ("Campaign", args.campaign_id), ("开场版本", args.variant_id),
        ("平台", args.platform), ("目标受众", args.audience),
        ("开场时长", "{}秒".format(args.hook_seconds)),
        ("开场任务", args.hook_job), ("第一秒信息", args.first_second),
        ("批准依据", args.proof_source),
        ("关键帧", "参考图1是批准的开场关键帧"),
        ("其他品牌事实素材", roles),
        ("从母版继承", "；".join(args.inherit)),
        ("唯一动作", args.action), ("相机", args.camera),
        ("衔接母版", args.handoff), ("平台安全区", args.safe_zone),
        ("排除项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；只生成一个可替换母版开头的平台原生Hook，不重做整条视频；"
        "动作与节奏可借母版视频，人物、产品、品牌与事实以批准图片为准；"
        "开场必须在规定时间内完成一个信息，并以可剪辑画面衔接原母版；"
        "不生成字幕、标题、价格、界面、夸张数据或未经批准的视觉证明"
    )


def validate_tail(args):
    validate_identity(args)
    if len(args.preserve) < 4:
        raise SystemExit("tail 至少提供 4 条 --preserve")
    if args.extend_seconds <= 0 or args.extend_seconds > 10:
        raise SystemExit("--extend-seconds 必须大于 0 且不超过 10")
    if args.tail_job == "loop" and not args.next_frame_match:
        raise SystemExit("loop 必须提供 --next-frame-match")
    if args.tail_job != "loop" and not args.hold_purpose:
        raise SystemExit("cta-hold/disclaimer-hold 必须提供 --hold-purpose")


def tail_prompt(args):
    fields = [
        ("Campaign", args.campaign_id), ("尾段版本", args.variant_id),
        ("平台", args.platform), ("尾段任务", args.tail_job),
        ("延长时长", "{}秒".format(args.extend_seconds)),
        ("原结尾状态", args.last_frame_state),
        ("循环首帧匹配", args.next_frame_match),
        ("停留用途", args.hold_purpose),
        ("必须保持", "；".join(args.preserve)),
        ("平台安全区", args.safe_zone), ("排除项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；只从源视频最后一帧向后延长，不改写原视频；"
        "动作、光线、相机、人物、产品、Logo与背景必须自然连续；"
        "如果是循环，结尾要在运动方向、构图和亮度上接近指定首帧；"
        "如果是停留，保持画面稳定并为后期批准CTA或免责声明留空；"
        "画面内不自动生成文字、按钮、价格、日期或平台UI"
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


def preview(model_id, prompt, images, videos, params):
    print(json.dumps({
        "publicModelId": model_id,
        "prompt": prompt,
        "imageSources": images,
        "videoSources": videos,
        "params": params,
    }, ensure_ascii=False, indent=2))


def submit(args, model_id, prompt, image_files, video_files, params, label):
    if args.preview:
        preview(model_id, prompt, image_files, video_files, params)
        return
    api = SocialAPI(load_key(args.api_key), args.verbose)
    snapshot = api.pricing(model_id, args.routing)
    image_ids = [upload(api, item, "image") for item in image_files]
    video_ids = [upload(api, item, "video") for item in video_files]
    response = api.generate(
        model_id, args.routing, snapshot, prompt, image_ids, video_ids, params
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[social-matrix]", args.campaign_id, args.variant_id, label,
          "taskId =", task_id)
    if not args.no_download:
        wait_and_download(
            api, task_id, Path(args.output_dir), args.campaign_id,
            args.variant_id, label,
        )


def run_adapt(args):
    validate_adapt(args)
    submit(
        args, ADAPT_MODEL, adapt_prompt(args), args.brand_source,
        [args.source_video], parse_params(args.param), "adapt",
    )


def run_hook(args):
    validate_hook(args)
    submit(
        args, HOOK_MODEL, hook_prompt(args),
        [args.key_frame] + args.brand_source, [args.master_video],
        parse_params(args.param), "hook",
    )


def run_tail(args):
    validate_tail(args)
    params = parse_params(args.param)
    params["extendDirection"] = "forward"
    submit(
        args, TAIL_MODEL, tail_prompt(args), [], [args.source_video], params,
        args.tail_job,
    )


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "variant"


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


def wait_and_download(api, task_id, output_dir, campaign_id, variant_id, label):
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
    stem = "{}-{}-{}".format(
        safe_name(campaign_id), safe_name(variant_id), safe_name(label)
    )
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"], output_dir / "{}-{}.mp4".format(stem, index)
            )


def status(args):
    api = SocialAPI(load_key(args.api_key), args.verbose)
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


def common_identity(parser):
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--variant-id", required=True)
    parser.add_argument("--platform", choices=PLATFORMS, required=True)


def brand_flags(parser):
    parser.add_argument("--brand-source", nargs="+", required=True)
    parser.add_argument("--brand-role", nargs="+", required=True)


def generation_flags(parser):
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--param", action="append")
    parser.add_argument(
        "--routing", choices=("COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"),
        default="COST_FIRST",
    )
    parser.add_argument("--output-dir", default=str(OUTPUT))
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--api-key")
    parser.add_argument("--verbose", action="store_true")


def build_cli():
    root = argparse.ArgumentParser(description="社媒视频跨平台版本矩阵")
    commands = root.add_subparsers(dest="command", required=True)

    adapt = commands.add_parser("adapt", help="把批准母版重构为一个渠道版本")
    common_identity(adapt)
    adapt.add_argument("--source-video", required=True)
    adapt.add_argument("--objective", choices=OBJECTIVES, required=True)
    adapt.add_argument("--audience", required=True)
    adapt.add_argument("--one-message", required=True)
    adapt.add_argument("--campaign-source", required=True)
    brand_flags(adapt)
    adapt.add_argument("--format", required=True)
    adapt.add_argument("--target-duration", required=True)
    adapt.add_argument("--hook-deadline", type=float, required=True)
    adapt.add_argument("--must-keep", action="append", required=True)
    adapt.add_argument("--may-trim", action="append", required=True)
    adapt.add_argument("--invariant", action="append", required=True)
    adapt.add_argument("--edit-logic", required=True)
    adapt.add_argument("--caption-plan", required=True)
    adapt.add_argument("--cta-plan", required=True)
    adapt.add_argument("--safe-zone", required=True)
    adapt.add_argument("--reject")
    generation_flags(adapt)
    adapt.set_defaults(handler=run_adapt)

    hook = commands.add_parser("hook", help="为母版生成平台原生开场")
    common_identity(hook)
    hook.add_argument("--master-video", required=True)
    hook.add_argument("--key-frame", required=True)
    brand_flags(hook)
    hook.add_argument("--audience", required=True)
    hook.add_argument("--hook-seconds", type=float, required=True)
    hook.add_argument("--hook-job", required=True)
    hook.add_argument("--first-second", required=True)
    hook.add_argument("--proof-source", required=True)
    hook.add_argument("--inherit", action="append", required=True)
    hook.add_argument("--action", required=True)
    hook.add_argument("--camera", required=True)
    hook.add_argument("--handoff", required=True)
    hook.add_argument("--safe-zone", required=True)
    hook.add_argument("--reject")
    generation_flags(hook)
    hook.set_defaults(handler=run_hook)

    tail = commands.add_parser("tail", help="延长结尾用于循环或后期停留")
    common_identity(tail)
    tail.add_argument("--source-video", required=True)
    tail.add_argument("--tail-job", choices=TAIL_JOBS, required=True)
    tail.add_argument("--extend-seconds", type=float, required=True)
    tail.add_argument("--last-frame-state", required=True)
    tail.add_argument("--next-frame-match")
    tail.add_argument("--hold-purpose")
    tail.add_argument("--preserve", action="append", required=True)
    tail.add_argument("--safe-zone", required=True)
    tail.add_argument("--reject")
    generation_flags(tail)
    tail.set_defaults(handler=run_tail)

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
