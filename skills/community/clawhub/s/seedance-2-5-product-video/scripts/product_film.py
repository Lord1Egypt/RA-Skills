#!/usr/bin/env python3
"""用 Seedance 2.5 生产受产品事实约束的宣传片镜头包。"""

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
SHOT_ROLES = (
    "establish", "hero", "material", "mechanism", "interaction", "scale",
    "transition", "end-frame",
)
FACT_ROLES = ("mechanism", "interaction", "scale")
IMAGE_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif",
}
VIDEO_TYPES = {
    ".mp4": "video/mp4", ".mov": "video/quicktime", ".webm": "video/webm",
}


def key_from(explicit=None):
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
        "或运行 product_film.py auth --api-key sk-api-*"
    )


class FilmAPI:
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

    def snapshot(self, model_id, routing):
        models = self.request("GET", "models", params={"modelType": "VIDEO"})
        model = next(
            (item for item in models if item.get("publicModelId") == model_id),
            None,
        )
        if model is None:
            raise SystemExit("当前模型列表没有固定能力：" + model_id)
        price = next(
            (item for item in model.get("pricingSnapshot", [])
             if item.get("routingMode") == routing),
            None,
        )
        if price is None:
            raise SystemExit("固定模型不支持所选路由：" + routing)
        return price

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
        payload = {
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
            payload["firstFrameMediaId"] = first_frame
        return self.request("POST", "generation/video", json=payload)

    def task(self, task_id):
        return self.request("GET", "generation/tasks/" + task_id)


def identifier(value, flag):
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", value):
        raise SystemExit(flag + " 只能包含字母、数字、点、下划线和连字符")


def validate(args):
    identifier(args.film_id, "--film-id")
    identifier(args.shot_id, "--shot-id")
    if not args.product_source or len(args.product_source) > 8:
        raise SystemExit("必须提供 1 到 8 张批准的产品事实图")
    if len(args.product_source) != len(args.product_role):
        raise SystemExit("每张 --product-source 必须对应一条 --product-role")
    if len(args.continuity_lock) < 4:
        raise SystemExit("每个镜头至少提供 4 条 --continuity-lock")
    if args.shot_role in FACT_ROLES and not (
        args.demonstrated_fact and args.fact_source
    ):
        raise SystemExit(
            "mechanism/interaction/scale 必须提供 --demonstrated-fact 与 --fact-source"
        )
    if args.shot_role == "end-frame" and "停" not in args.edit_handles:
        raise SystemExit("end-frame 的 --edit-handles 必须明确稳定停留")


def prompt_for(args):
    sources = "；".join(
        "产品事实图{}={}".format(index, role)
        for index, role in enumerate(args.product_role, 1)
    )
    fields = [
        ("影片", args.film_id), ("镜头", args.shot_id),
        ("镜头职责", args.shot_role), ("交付规格", args.delivery),
        ("目标观众", args.audience), ("影片命题", args.film_thesis),
        ("产品主档", args.product_record), ("产品事实素材", sources),
        ("视觉场景", args.set_design), ("色彩系统", args.palette),
        ("灯光系统", args.lighting), ("镜头与景深", args.lens),
        ("起始构图", args.camera_start), ("相机运动", args.camera_move),
        ("结束构图", args.camera_end), ("主体动作", args.subject_action),
        ("本镜头演示事实", args.demonstrated_fact),
        ("事实批准来源", args.fact_source),
        ("全片连续性锁定", "；".join(args.continuity_lock)),
        ("剪辑把手", args.edit_handles), ("字幕与排版安全", args.copy_safe),
        ("排除项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；只制作这个独立宣传片镜头，不自动生成整支广告；"
        "真实产品图和产品主档优先于风格、运镜与动作参考；"
        "不得改变SKU、结构、材质、比例、接口、配件、包装、Logo或批准文字；"
        "不得揭示未提供的内部结构，不得用特效暗示未批准性能；"
        "画面内不生成价格、参数、认证、奖项或营销文案，文字留给后期排版；"
        "镜头开始和结束都要有可剪辑的稳定画面"
    )


def media_file(filename, kind):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("素材不存在：" + str(path))
    table = IMAGE_TYPES if kind == "image" else VIDEO_TYPES
    content_type = table.get(path.suffix.lower())
    if content_type is None:
        raise SystemExit("{}素材格式不支持：{}".format(kind, path))
    return path, content_type


def upload(api, filename, kind):
    path, content_type = media_file(filename, kind)
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


def params_from(values):
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


def make_shot(args):
    validate(args)
    prompt = prompt_for(args)
    params = params_from(args.param)
    model_id = R2V_MODEL if args.motion_reference else I2V_MODEL
    if args.preview:
        print(json.dumps({
            "publicModelId": model_id,
            "filmId": args.film_id,
            "shotId": args.shot_id,
            "shotRole": args.shot_role,
            "prompt": prompt,
            "productSources": args.product_source,
            "motionReference": args.motion_reference,
            "firstFrame": None if args.motion_reference else args.product_source[0],
            "params": params,
        }, ensure_ascii=False, indent=2))
        return
    api = FilmAPI(key_from(args.api_key), args.verbose)
    snapshot = api.snapshot(model_id, args.routing)
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
    print("[product-film]", args.film_id, args.shot_id, "taskId =", task_id)
    if not args.no_download:
        wait_and_download(
            api, task_id, Path(args.output_dir), args.film_id, args.shot_id
        )


def clean_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "shot"


def download(url, destination):
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


def wait_and_download(api, task_id, output_dir, film_id, shot_id):
    deadline = time.time() + 1200
    task = None
    while time.time() < deadline:
        task = api.task(task_id)
        items = task.get("items", [])
        states = [item.get("status", "UNKNOWN") for item in items]
        print("[task]", task_id, ",".join(states) or "PENDING")
        if items and all(value in ("COMPLETED", "FAILED") for value in states):
            break
        time.sleep(3)
    else:
        raise SystemExit("任务轮询超时；请使用 status 查询原 taskId")
    stem = "{}-{}".format(clean_name(film_id), clean_name(shot_id))
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            download(
                item["resultUrl"], output_dir / "{}-{}.mp4".format(stem, index)
            )


def show_status(args):
    api = FilmAPI(key_from(args.api_key), args.verbose)
    print(json.dumps(api.task(args.task_id), ensure_ascii=False, indent=2))


def save_auth(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    CONFIG.chmod(0o600)
    print("已安全写入", CONFIG)


def build_cli():
    root = argparse.ArgumentParser(
        description="Seedance 2.5 产品宣传片镜头包工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    shot = commands.add_parser("shot", help="生成一个受产品事实约束的宣传片镜头")
    shot.add_argument("--film-id", required=True)
    shot.add_argument("--shot-id", required=True)
    shot.add_argument("--shot-role", choices=SHOT_ROLES, required=True)
    shot.add_argument("--delivery", required=True)
    shot.add_argument("--audience", required=True)
    shot.add_argument("--film-thesis", required=True)
    shot.add_argument("--product-record", required=True)
    shot.add_argument("--product-source", nargs="+", required=True)
    shot.add_argument("--product-role", nargs="+", required=True)
    shot.add_argument("--set-design", required=True)
    shot.add_argument("--palette", required=True)
    shot.add_argument("--lighting", required=True)
    shot.add_argument("--lens", required=True)
    shot.add_argument("--camera-start", required=True)
    shot.add_argument("--camera-move", required=True)
    shot.add_argument("--camera-end", required=True)
    shot.add_argument("--subject-action", required=True)
    shot.add_argument("--demonstrated-fact")
    shot.add_argument("--fact-source")
    shot.add_argument("--continuity-lock", action="append", required=True)
    shot.add_argument("--edit-handles", required=True)
    shot.add_argument("--copy-safe", required=True)
    shot.add_argument("--reject")
    shot.add_argument("--motion-reference")
    shot.add_argument("--preview", action="store_true")
    shot.add_argument("--param", action="append")
    shot.add_argument(
        "--routing", choices=("COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"),
        default="COST_FIRST",
    )
    shot.add_argument("--output-dir", default=str(OUTPUT))
    shot.add_argument("--no-download", action="store_true")
    shot.add_argument("--api-key")
    shot.add_argument("--verbose", action="store_true")
    shot.set_defaults(handler=make_shot)

    status = commands.add_parser("status", help="查询生成任务")
    status.add_argument("--task-id", required=True)
    status.add_argument("--api-key")
    status.add_argument("--verbose", action="store_true")
    status.set_defaults(handler=show_status)

    auth = commands.add_parser("auth", help="保存 AI Hive API Key")
    auth.add_argument("--api-key", required=True)
    auth.set_defaults(handler=save_auth)
    return root


def main():
    args = build_cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
