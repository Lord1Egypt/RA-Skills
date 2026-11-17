#!/usr/bin/env python3
"""用世界状态账本提交 AI Hive Seedance 2.5 视频任务。"""

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


API_ROOT = "https://ai-hive.iclip.cn/api/openapi/v1"
KEY_FILE = Path.home() / ".ai-hive" / "config.json"
DEFAULT_OUTPUT = Path.home() / "Downloads" / "AiHive"
MODEL_BY_PHASE = {
    "invent": "public_model_seedance_2_5_t2v",
    "awaken": "public_model_seedance_2_5_i2v",
    "reference": "public_model_seedance_2_5_r2v",
    "repair": "public_model_seedance_2_5_video_edit",
    "continue": "public_model_seedance_2_5_video_extend",
}
MEDIA_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
}


def api_key(explicit=None):
    """Read a key without ever printing it."""
    if explicit:
        return explicit
    value = os.environ.get("AI_HIVE_API_KEY")
    if value:
        return value
    try:
        saved = json.loads(KEY_FILE.read_text(encoding="utf-8"))
        value = saved.get("api_key")
        if value:
            try:
                if KEY_FILE.stat().st_mode & 0o077:
                    KEY_FILE.chmod(0o600)
            except OSError:
                pass
            return value
    except (OSError, ValueError):
        pass
    raise SystemExit(
        "缺少 AI Hive API Key；使用 --api-key、AI_HIVE_API_KEY，"
        "或先运行 sora_world.py configure --api-key sk-api-*"
    )


class WorldClient:
    """Minimal client restricted to AI Hive video endpoints."""

    def __init__(self, key, trace=False):
        self.trace = trace
        self.headers = {
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        }

    def request(self, method, path, **kwargs):
        url = API_ROOT + "/" + path.lstrip("/")
        if self.trace:
            print("[request]", method, url, file=sys.stderr)
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                timeout=30,
                **kwargs,
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

    def model_and_price(self, phase, routing):
        public_id = MODEL_BY_PHASE[phase]
        rows = self.request("GET", "models", params={"modelType": "VIDEO"})
        model = next(
            (row for row in rows if row.get("publicModelId") == public_id),
            None,
        )
        if model is None:
            raise SystemExit("当前模型列表中没有固定能力：" + public_id)
        price = next(
            (
                item
                for item in model.get("pricingSnapshot", [])
                if item.get("routingMode") == routing
            ),
            None,
        )
        if price is None:
            raise SystemExit("固定能力不支持所选路由：" + routing)
        return public_id, price

    def begin_upload(self, path, content_type):
        return self.request(
            "POST",
            "media/upload-token",
            json={
                "filename": path.name,
                "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def finish_upload(self, media_id):
        self.request("POST", "media/{}/complete".format(media_id))

    def create_video(self, phase, routing, prompt, params, price,
                     image_ids, video_ids, first_frame_id=None):
        body = {
            "publicModelId": MODEL_BY_PHASE[phase],
            "routingMode": routing,
            "prompt": prompt,
            "imageMediaIds": image_ids,
            "videoMediaIds": video_ids,
            "audioMediaIds": [],
            "params": params,
            "pricingSnapshot": price,
        }
        if first_frame_id:
            body["firstFrameMediaId"] = first_frame_id
        return self.request("POST", "generation/video", json=body)

    def task(self, task_id):
        return self.request("GET", "generation/tasks/" + task_id)


def local_media(filename, expected):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("素材不存在：" + str(path))
    content_type = MEDIA_TYPES.get(path.suffix.lower())
    if content_type is None:
        raise SystemExit("不支持的素材格式：" + str(path))
    if not content_type.startswith(expected + "/"):
        raise SystemExit("这里需要{}文件：{}".format(expected, path))
    return path, content_type


def upload_media(client, filename, expected):
    path, content_type = local_media(filename, expected)
    ticket = client.begin_upload(path, content_type)
    media_id = ticket["mediaId"]
    upload = ticket["upload"]
    upload_url = upload["url"]
    if urlparse(upload_url).scheme != "https":
        raise SystemExit("对象存储上传地址必须使用 HTTPS")
    try:
        with path.open("rb") as stream:
            response = requests.request(
                upload.get("method", "PUT"),
                upload_url,
                headers=upload.get("headers", {}),
                data=stream,
                timeout=300,
            )
    except requests.RequestException as exc:
        raise SystemExit("素材上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "素材上传失败 {}：{}".format(response.status_code, response.text)
        )
    client.finish_upload(media_id)
    print("[media]", path.name, "->", media_id)
    return media_id


def pairs(values):
    result = {}
    for value in values or []:
        if "=" not in value:
            raise SystemExit("--param 必须使用 key=value：" + value)
        key, raw = value.split("=", 1)
        try:
            parsed = int(raw)
        except ValueError:
            try:
                parsed = float(raw)
            except ValueError:
                parsed = raw
        result[key] = parsed
    return result


def ledger_prompt(args):
    entries = [
        ("起始世界", args.start),
        ("唯一事件", args.event),
        ("结束世界", args.end),
        ("相机连续性", args.camera),
        ("不可变量", args.constants),
        ("补充要求", args.prompt),
    ]
    return "；".join(label + "：" + value for label, value in entries if value)


def validate_ledger(args):
    if not args.start or not args.event or not args.end:
        raise SystemExit("世界状态任务必须同时填写 --start、--event 和 --end")
    if args.phase == "invent":
        if any((args.start_frame, args.reference_image,
                args.reference_video, args.source_video)):
            raise SystemExit("invent 从文字建世界，不接受媒体输入")
    elif args.phase == "awaken":
        if not args.start_frame:
            raise SystemExit("awaken 必须提供一张 --start-frame")
        if any((args.reference_image, args.reference_video, args.source_video)):
            raise SystemExit("awaken 只接受首帧，不接受其他参考或源视频")
    elif args.phase == "reference":
        if not any((args.reference_image, args.reference_video)):
            raise SystemExit("reference 至少提供一项图片或视频参考")
        if args.start_frame or args.source_video:
            raise SystemExit("reference 不接受首帧或编辑源视频")
    else:
        if not args.source_video:
            raise SystemExit(args.phase + " 必须提供一个 --source-video")
        if any((args.start_frame, args.reference_image, args.reference_video)):
            raise SystemExit(args.phase + " 只接受一个源视频")


def submit_world(args):
    validate_ledger(args)
    client = WorldClient(api_key(args.api_key), args.trace)
    _, price = client.model_and_price(args.phase, args.routing)
    first_frame_id = None
    image_ids = []
    video_ids = []
    if args.start_frame:
        first_frame_id = upload_media(client, args.start_frame, "image")
    for filename in args.reference_image or []:
        image_ids.append(upload_media(client, filename, "image"))
    for filename in args.reference_video or []:
        video_ids.append(upload_media(client, filename, "video"))
    if args.source_video:
        video_ids.append(upload_media(client, args.source_video, "video"))
    params = pairs(args.param)
    if args.phase == "continue":
        params["extendDirection"] = "forward"
    response = client.create_video(
        args.phase,
        args.routing,
        ledger_prompt(args),
        params,
        price,
        image_ids,
        video_ids,
        first_frame_id,
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[world]", args.phase, "taskId =", task_id)
    if not args.no_download:
        wait_and_save(client, task_id, Path(args.output_dir))


def save_https(url, target):
    if urlparse(url).scheme != "https":
        raise SystemExit("结果下载地址必须使用 HTTPS")
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=300) as response:
            response.raise_for_status()
            with target.open("wb") as stream:
                for block in response.iter_content(8192):
                    if block:
                        stream.write(block)
    except requests.RequestException as exc:
        raise SystemExit("结果下载失败：" + str(exc))
    print("[saved]", target)


def wait_and_save(client, task_id, output_dir, timeout=1200):
    deadline = time.time() + timeout
    task = None
    while time.time() < deadline:
        task = client.task(task_id)
        items = task.get("items", [])
        statuses = [item.get("status", "UNKNOWN") for item in items]
        print("[status]", task_id, ",".join(statuses) or "PENDING")
        if items and all(value in ("COMPLETED", "FAILED") for value in statuses):
            break
        time.sleep(3)
    else:
        raise SystemExit("任务轮询超时；保留 taskId 后可继续查询")
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            save_https(
                item["resultUrl"],
                output_dir / "{}_{}.mp4".format(task_id, index),
            )


def show_status(args):
    client = WorldClient(api_key(args.api_key), args.trace)
    print(json.dumps(client.task(args.task_id), ensure_ascii=False, indent=2))


def send_media(args):
    client = WorldClient(api_key(args.api_key), args.trace)
    path = Path(args.file)
    content_type = MEDIA_TYPES.get(path.suffix.lower(), "")
    expected = "image" if content_type.startswith("image/") else "video"
    print(upload_media(client, args.file, expected))


def configure(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    KEY_FILE.write_text(
        json.dumps({"api_key": args.api_key}, indent=2),
        encoding="utf-8",
    )
    KEY_FILE.chmod(0o600)
    print("已安全写入", KEY_FILE)


def client_flags(parser):
    parser.add_argument("--api-key")
    parser.add_argument("--trace", action="store_true")


def world_flags(parser, phase):
    parser.set_defaults(phase=phase, handler=submit_world)
    parser.add_argument("--start", required=True, help="事件发生前的世界状态")
    parser.add_argument("--event", required=True, help="唯一改变状态的事件")
    parser.add_argument("--end", required=True, help="事件完成后的世界状态")
    parser.add_argument("--camera", help="相机位置与连续运动")
    parser.add_argument("--constants", help="全程不可改变的数量、身份与关系")
    parser.add_argument("--prompt", help="其他生成要求")
    parser.add_argument("--start-frame")
    parser.add_argument("--reference-image", nargs="*")
    parser.add_argument("--reference-video", nargs="*")
    parser.add_argument("--source-video")
    parser.add_argument("--param", nargs="*")
    parser.add_argument(
        "--routing",
        choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--no-download", action="store_true")
    client_flags(parser)


def parser():
    root = argparse.ArgumentParser(
        description="Sora 替代场景的世界状态账本视频工具"
    )
    commands = root.add_subparsers(dest="command", required=True)
    labels = {
        "invent": "从文字建立并推进世界",
        "awaken": "从批准首帧推进世界",
        "reference": "借用授权参考的身份、场景或运动",
        "repair": "修复源视频中的状态矛盾",
        "continue": "从末帧继续同一世界事件",
    }
    for phase, help_text in labels.items():
        world_flags(commands.add_parser(phase, help=help_text), phase)

    status = commands.add_parser("status", help="查询任务状态")
    status.add_argument("--task-id", required=True)
    client_flags(status)
    status.set_defaults(handler=show_status)

    media = commands.add_parser("media", help="单独上传图片或视频")
    media.add_argument("--file", required=True)
    client_flags(media)
    media.set_defaults(handler=send_media)

    config = commands.add_parser("configure", help="保存 AI Hive API Key")
    config.add_argument("--api-key", required=True)
    config.set_defaults(handler=configure)
    return root


def main():
    args = parser().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
