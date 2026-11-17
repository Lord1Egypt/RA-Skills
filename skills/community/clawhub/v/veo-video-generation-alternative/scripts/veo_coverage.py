#!/usr/bin/env python3
"""把摄影覆盖单提交为 AI Hive Seedance 2.5 无声视频镜头。"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    raise SystemExit("缺少 requests，请运行 pip3 install requests")


ROOT = "https://ai-hive.iclip.cn/api"
SETTINGS = Path.home() / ".ai-hive" / "config.json"
RENDER_DIR = Path.home() / "Downloads" / "AiHive"
ROUTES = {
    "establish": "public_model_seedance_2_5_t2v",
    "detail": "public_model_seedance_2_5_i2v",
    "track": "public_model_seedance_2_5_r2v",
    "relight": "public_model_seedance_2_5_video_edit",
    "outro": "public_model_seedance_2_5_video_extend",
}
MIMES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
}


def credentials(value=None):
    if value:
        return value
    value = os.environ.get("AI_HIVE_API_KEY")
    if value:
        return value
    try:
        saved = json.loads(SETTINGS.read_text(encoding="utf-8"))
        value = saved.get("api_key")
        if value:
            try:
                if SETTINGS.stat().st_mode & 0o077:
                    SETTINGS.chmod(0o600)
            except OSError:
                pass
            return value
    except (OSError, ValueError):
        pass
    raise SystemExit(
        "缺少 AI Hive API Key。使用 --api-key、AI_HIVE_API_KEY，"
        "或运行 veo_coverage.py setup --api-key sk-api-*"
    )


def endpoint(path):
    return ROOT + "/openapi/v1/" + path.lstrip("/")


class CoverageAPI:
    def __init__(self, key, debug=False):
        self.debug = debug
        self.headers = {
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        }

    def exchange(self, method, path, **kwargs):
        url = endpoint(path)
        if self.debug:
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

    def route_snapshot(self, shot_type, routing):
        public_id = ROUTES[shot_type]
        catalog = self.exchange(
            "GET", "models", params={"modelType": "VIDEO"}
        )
        model = next(
            (item for item in catalog if item.get("publicModelId") == public_id),
            None,
        )
        if model is None:
            raise SystemExit("找不到固定视频能力：" + public_id)
        snapshot = next(
            (
                item
                for item in model.get("pricingSnapshot", [])
                if item.get("routingMode") == routing
            ),
            None,
        )
        if snapshot is None:
            raise SystemExit("当前能力不支持路由：" + routing)
        return public_id, snapshot

    def upload_ticket(self, file_path, mime):
        return self.exchange(
            "POST",
            "media/upload-token",
            json={
                "filename": file_path.name,
                "contentType": mime,
                "sizeBytes": file_path.stat().st_size,
            },
        )

    def confirm_media(self, media_id):
        self.exchange("POST", "media/{}/complete".format(media_id))

    def render(self, public_id, routing, snapshot, prompt, parameters,
               images, videos, first_frame=None):
        request_body = {
            "publicModelId": public_id,
            "routingMode": routing,
            "prompt": prompt,
            "imageMediaIds": images,
            "videoMediaIds": videos,
            "audioMediaIds": [],
            "params": parameters,
            "pricingSnapshot": snapshot,
        }
        if first_frame:
            request_body["firstFrameMediaId"] = first_frame
        return self.exchange("POST", "generation/video", json=request_body)

    def progress(self, task_id):
        return self.exchange("GET", "generation/tasks/" + task_id)


def inspect_local(filename, family):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("素材不存在：" + str(path))
    mime = MIMES.get(path.suffix.lower())
    if not mime:
        raise SystemExit("仅支持常见图片和视频格式：" + str(path))
    if not mime.startswith(family + "/"):
        raise SystemExit("该镜头槽需要{}：{}".format(family, path))
    return path, mime


def attach(api, filename, family):
    path, mime = inspect_local(filename, family)
    ticket = api.upload_ticket(path, mime)
    media_id = ticket["mediaId"]
    transfer = ticket["upload"]
    address = transfer["url"]
    if urlparse(address).scheme != "https":
        raise SystemExit("素材上传地址必须使用 HTTPS")
    try:
        with path.open("rb") as handle:
            response = requests.request(
                transfer.get("method", "PUT"),
                address,
                headers=transfer.get("headers", {}),
                data=handle,
                timeout=300,
            )
    except requests.RequestException as exc:
        raise SystemExit("素材上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "素材上传失败 {}：{}".format(response.status_code, response.text)
        )
    api.confirm_media(media_id)
    print("[attached]", path.name, "->", media_id)
    return media_id


def parameters(values):
    parsed = {}
    for pair in values or []:
        if "=" not in pair:
            raise SystemExit("--param 必须使用 key=value：" + pair)
        key, value = pair.split("=", 1)
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        parsed[key] = value
    return parsed


def coverage_text(args):
    fields = [
        ("镜头用途", args.purpose),
        ("景别", args.framing),
        ("焦点主体", args.subject),
        ("相机位置", args.camera),
        ("运动轨迹", args.motion),
        ("焦点变化", args.focus),
        ("光线", args.light),
        ("可剪辑出点", args.out),
        ("保护项", args.protect),
        ("补充说明", args.prompt),
    ]
    return "；".join(label + "：" + value for label, value in fields if value)


def check_slots(args):
    if not args.purpose or not args.subject or not args.camera:
        raise SystemExit("覆盖单至少需要 --purpose、--subject 和 --camera")
    if args.shot_type == "establish":
        if any((args.start_frame, args.reference_image,
                args.reference_video, args.source_video)):
            raise SystemExit("establish 为纯文字建立镜头，不接受媒体")
    elif args.shot_type == "detail":
        if not args.start_frame:
            raise SystemExit("detail 必须提供一张 --start-frame")
        if any((args.reference_image, args.reference_video, args.source_video)):
            raise SystemExit("detail 只接受首帧图片")
    elif args.shot_type == "track":
        if not any((args.reference_image, args.reference_video)):
            raise SystemExit("track 至少需要一项摄影参考")
        if args.start_frame or args.source_video:
            raise SystemExit("track 不接受首帧或编辑源视频")
    else:
        if not args.source_video:
            raise SystemExit(args.shot_type + " 必须提供一个 --source-video")
        if any((args.start_frame, args.reference_image, args.reference_video)):
            raise SystemExit(args.shot_type + " 只接受一个源视频")


def make_shot(args):
    check_slots(args)
    api = CoverageAPI(credentials(args.api_key), args.debug)
    public_id, snapshot = api.route_snapshot(args.shot_type, args.routing)
    first_frame = None
    image_ids = []
    video_ids = []
    if args.start_frame:
        first_frame = attach(api, args.start_frame, "image")
    for filename in args.reference_image or []:
        image_ids.append(attach(api, filename, "image"))
    for filename in args.reference_video or []:
        video_ids.append(attach(api, filename, "video"))
    if args.source_video:
        video_ids.append(attach(api, args.source_video, "video"))
    options = parameters(args.param)
    if args.shot_type == "outro":
        options["extendDirection"] = "forward"
    response = api.render(
        public_id,
        args.routing,
        snapshot,
        coverage_text(args),
        options,
        image_ids,
        video_ids,
        first_frame,
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[coverage]", args.shot_type, "taskId =", task_id)
    print("[audio] 此任务仅生成无声画面；对白、配乐和音效请在后期制作")
    if not args.no_download:
        collect(api, task_id, Path(args.output_dir))


def fetch_result(url, path):
    if urlparse(url).scheme != "https":
        raise SystemExit("结果下载地址必须使用 HTTPS")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=300) as response:
            response.raise_for_status()
            with path.open("wb") as handle:
                for chunk in response.iter_content(8192):
                    if chunk:
                        handle.write(chunk)
    except requests.RequestException as exc:
        raise SystemExit("结果下载失败：" + str(exc))
    print("[saved]", path)


def collect(api, task_id, output_dir, timeout=1200):
    deadline = time.time() + timeout
    task = None
    while time.time() < deadline:
        task = api.progress(task_id)
        rows = task.get("items", [])
        statuses = [row.get("status", "UNKNOWN") for row in rows]
        print("[progress]", task_id, ",".join(statuses) or "PENDING")
        if rows and all(value in ("COMPLETED", "FAILED") for value in statuses):
            break
        time.sleep(3)
    else:
        raise SystemExit("任务轮询超时；可用 check 命令继续查询")
    for number, row in enumerate(task.get("items", []), 1):
        if row.get("status") == "FAILED":
            print("[failed]", row.get("errorMessage"), file=sys.stderr)
        if row.get("status") == "COMPLETED" and row.get("resultUrl"):
            fetch_result(
                row["resultUrl"],
                output_dir / "{}_{}.mp4".format(task_id, number),
            )


def check_task(args):
    api = CoverageAPI(credentials(args.api_key), args.debug)
    print(json.dumps(api.progress(args.task_id), ensure_ascii=False, indent=2))


def attach_only(args):
    api = CoverageAPI(credentials(args.api_key), args.debug)
    path = Path(args.file)
    mime = MIMES.get(path.suffix.lower(), "")
    family = "image" if mime.startswith("image/") else "video"
    print(attach(api, args.file, family))


def setup(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    SETTINGS.chmod(0o600)
    print("已安全写入", SETTINGS)


def connection_options(command):
    command.add_argument("--api-key")
    command.add_argument("--debug", action="store_true")


def shot_options(command, shot_type):
    command.set_defaults(handler=make_shot, shot_type=shot_type)
    command.add_argument("--purpose", required=True)
    command.add_argument("--framing")
    command.add_argument("--subject", required=True)
    command.add_argument("--camera", required=True)
    command.add_argument("--motion")
    command.add_argument("--focus")
    command.add_argument("--light")
    command.add_argument("--out")
    command.add_argument("--protect")
    command.add_argument("--prompt")
    command.add_argument("--start-frame")
    command.add_argument("--reference-image", nargs="*")
    command.add_argument("--reference-video", nargs="*")
    command.add_argument("--source-video")
    command.add_argument("--param", nargs="*")
    command.add_argument(
        "--routing",
        choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    command.add_argument("--output-dir", default=str(RENDER_DIR))
    command.add_argument("--no-download", action="store_true")
    connection_options(command)


def command_line():
    root = argparse.ArgumentParser(
        description="Veo 替代场景的无声摄影覆盖计划工具"
    )
    actions = root.add_subparsers(dest="command", required=True)
    helps = {
        "establish": "生成建立镜头",
        "detail": "从首帧生成产品或人物细节镜头",
        "track": "使用授权参考规划摄影路径",
        "relight": "修复源片光线连续性",
        "outro": "延长为可剪辑出点",
    }
    for shot_type, text in helps.items():
        shot_options(actions.add_parser(shot_type, help=text), shot_type)

    check = actions.add_parser("check", help="查询镜头任务")
    check.add_argument("--task-id", required=True)
    connection_options(check)
    check.set_defaults(handler=check_task)

    media = actions.add_parser("attach", help="单独上传图片或视频")
    media.add_argument("--file", required=True)
    connection_options(media)
    media.set_defaults(handler=attach_only)

    config = actions.add_parser("setup", help="保存 AI Hive API Key")
    config.add_argument("--api-key", required=True)
    config.set_defaults(handler=setup)
    return root


def main():
    args = command_line().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
