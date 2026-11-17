#!/usr/bin/env python3
"""用 Nano Banana Pro 生成获授权成年模特的服装试穿商品图。"""

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


OPENAPI = "https://ai-hive.iclip.cn/api/openapi/v1"
TRYON_MODEL = "public_model_nano_banana_pro"
KEY_FILE = Path.home() / ".ai-hive" / "config.json"
RESULTS = Path.home() / "Downloads" / "AiHive"
GARMENT_TYPES = ("top", "bottom", "dress", "outerwear", "set")
VIEWS = ("front", "back", "left-side", "right-side", "three-quarter")
IMAGE_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}


def credential(value=None):
    if value:
        return value
    environment = os.environ.get("AI_HIVE_API_KEY")
    if environment:
        return environment
    try:
        stored = json.loads(KEY_FILE.read_text(encoding="utf-8"))
        value = stored.get("api_key")
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
        "或运行 authorized_tryon.py auth --api-key sk-api-*"
    )


class TryOnAPI:
    def __init__(self, key, trace=False):
        self.trace = trace
        self.headers = {
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        }

    def request(self, method, resource, **kwargs):
        url = OPENAPI + "/" + resource.lstrip("/")
        if self.trace:
            print("[api]", method, url, file=sys.stderr)
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

    def price(self, routing):
        catalog = self.request("GET", "models", params={"modelType": "IMAGE"})
        model = next(
            (item for item in catalog if item.get("publicModelId") == TRYON_MODEL),
            None,
        )
        if model is None:
            raise SystemExit("当前模型列表没有固定能力：" + TRYON_MODEL)
        snapshot = next(
            (
                item
                for item in model.get("pricingSnapshot", [])
                if item.get("routingMode") == routing
            ),
            None,
        )
        if snapshot is None:
            raise SystemExit("Nano Banana Pro 不支持路由：" + routing)
        return snapshot

    def reserve(self, path, content_type):
        return self.request(
            "POST",
            "media/upload-token",
            json={
                "filename": path.name,
                "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def finish(self, media_id):
        self.request("POST", "media/{}/complete".format(media_id))

    def submit(self, routing, price, prompt, media_ids, batch, params):
        return self.request(
            "POST",
            "generation/image",
            json={
                "publicModelId": TRYON_MODEL,
                "routingMode": routing,
                "prompt": prompt,
                "batchSize": batch,
                "imageMediaIds": media_ids,
                "params": params,
                "pricingSnapshot": price,
            },
        )

    def task(self, task_id):
        return self.request("GET", "generation/tasks/" + task_id)


def local_image(filename):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("参考图不存在：" + str(path))
    content_type = IMAGE_TYPES.get(path.suffix.lower())
    if not content_type:
        raise SystemExit("试穿参考素材必须是常见图片：" + str(path))
    return path, content_type


def upload(api, filename, role):
    path, content_type = local_image(filename)
    ticket = api.reserve(path, content_type)
    media_id = ticket["mediaId"]
    transfer = ticket["upload"]
    url = transfer["url"]
    if urlparse(url).scheme != "https":
        raise SystemExit("参考图上传地址必须使用 HTTPS")
    try:
        with path.open("rb") as stream:
            response = requests.request(
                transfer.get("method", "PUT"),
                url,
                headers=transfer.get("headers", {}),
                data=stream,
                timeout=300,
            )
    except requests.RequestException as exc:
        raise SystemExit("参考图上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "参考图上传失败 {}：{}".format(response.status_code, response.text)
        )
    api.finish(media_id)
    print("[{}]".format(role), path.name, "->", media_id)
    return media_id


def params(values):
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


def validate_tryon(args):
    if not args.adult_confirmed:
        raise SystemExit("只处理成年人；必须确认 --adult-confirmed")
    if not args.person_authorized:
        raise SystemExit("必须确认人物素材授权 --person-authorized")
    if not args.garment_authorized:
        raise SystemExit("必须确认服装素材授权 --garment-authorized")
    if not args.garment_reference:
        raise SystemExit("必须提供至少一张 --garment-reference")
    if len(args.garment_reference) > 3:
        raise SystemExit("服装参考图最多 3 张")
    if len(args.background_reference or []) > 1:
        raise SystemExit("背景参考图最多 1 张")
    required = (
        args.identity_keep,
        args.body_keep,
        args.garment_keep,
        args.fit,
        args.pose,
        args.framing,
        args.background,
        args.occlusion,
    )
    if not all(value and value.strip() for value in required):
        raise SystemExit(
            "身份、身体、服装、合身描述、姿态、景别、背景和遮挡规则均不能为空"
        )
    if args.batch < 1 or args.batch > 2:
        raise SystemExit("为便于逐张核对，--batch 只能是 1 或 2")


def tryon_prompt(args):
    fields = [
        ("人物素材编号", args.person_id),
        ("服装 SKU", args.garment_sku),
        ("服装类别", args.garment_type),
        ("目标视角", args.view),
        ("身份必须保持", args.identity_keep),
        ("身体必须保持", args.body_keep),
        ("服装必须保持", args.garment_keep),
        ("合身与垂坠", args.fit),
        ("姿态", args.pose),
        ("景别", args.framing),
        ("背景", args.background),
        ("光线", args.lighting),
        ("层叠关系", args.underlayer),
        ("遮挡与接触", args.occlusion),
        ("禁止改变", args.do_not_change),
    ]
    prompt = "；".join(label + "：" + value for label, value in fields if value)
    return (
        prompt
        + "；图1只锁定获授权成年人物身份，后续服装图只锁定指定 SKU，最后一张可选图只提供背景；"
        + "不得改变人物年龄、脸、发型、肤色、身体比例、体型或可识别特征；"
        + "不得改变服装版型、领口、袖长、下摆、口袋、扣件、图案、颜色、纹理、Logo 或数量；"
        + "试穿图只展示视觉搭配，不代表真实尺码、合身度、面料性能或购买承诺"
    )


def create_tryon(args):
    validate_tryon(args)
    api = TryOnAPI(credential(args.api_key), args.trace)
    price = api.price(args.routing)
    media_ids = [upload(api, args.person_reference, "person")]
    for filename in args.garment_reference:
        media_ids.append(upload(api, filename, "garment"))
    for filename in args.background_reference or []:
        media_ids.append(upload(api, filename, "background"))
    response = api.submit(
        args.routing,
        price,
        tryon_prompt(args),
        media_ids,
        args.batch,
        params(args.param),
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[try-on]", args.person_id, args.garment_sku, "taskId =", task_id)
    if not args.no_download:
        wait(api, task_id, Path(args.output_dir))


def preview(args):
    validate_tryon(args)
    print(tryon_prompt(args))


def download(url, destination):
    if urlparse(url).scheme != "https":
        raise SystemExit("结果下载地址必须使用 HTTPS")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=300) as response:
            response.raise_for_status()
            with destination.open("wb") as stream:
                for chunk in response.iter_content(8192):
                    if chunk:
                        stream.write(chunk)
    except requests.RequestException as exc:
        raise SystemExit("结果下载失败：" + str(exc))
    print("[saved]", destination)


def wait(api, task_id, output_dir, timeout=1200):
    deadline = time.time() + timeout
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
        raise SystemExit("任务轮询超时；可使用 status 命令继续查询")
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            download(
                item["resultUrl"],
                output_dir / "{}_{}.png".format(task_id, index),
            )


def show_status(args):
    api = TryOnAPI(credential(args.api_key), args.trace)
    print(json.dumps(api.task(args.task_id), ensure_ascii=False, indent=2))


def upload_one(args):
    api = TryOnAPI(credential(args.api_key), args.trace)
    print(upload(api, args.file, "reference"))


def save_auth(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    KEY_FILE.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    KEY_FILE.chmod(0o600)
    print("已安全写入", KEY_FILE)


def api_flags(parser):
    parser.add_argument("--api-key")
    parser.add_argument("--trace", action="store_true")


def tryon_flags(parser):
    parser.add_argument("--adult-confirmed", action="store_true")
    parser.add_argument("--person-authorized", action="store_true")
    parser.add_argument("--garment-authorized", action="store_true")
    parser.add_argument("--person-id", required=True)
    parser.add_argument("--person-reference", required=True)
    parser.add_argument("--garment-sku", required=True)
    parser.add_argument("--garment-type", choices=GARMENT_TYPES, required=True)
    parser.add_argument("--garment-reference", nargs="+", required=True)
    parser.add_argument("--background-reference", nargs="*")
    parser.add_argument("--view", choices=VIEWS, required=True)
    parser.add_argument("--identity-keep", required=True)
    parser.add_argument("--body-keep", required=True)
    parser.add_argument("--garment-keep", required=True)
    parser.add_argument("--fit", required=True)
    parser.add_argument("--pose", required=True)
    parser.add_argument("--framing", required=True)
    parser.add_argument("--background", required=True)
    parser.add_argument("--lighting")
    parser.add_argument("--underlayer")
    parser.add_argument("--occlusion", required=True)
    parser.add_argument("--do-not-change")
    parser.add_argument("--batch", type=int, default=1)


def cli():
    root = argparse.ArgumentParser(
        description="Nano Banana Pro 获授权成年模特服装试穿商品图工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    create = commands.add_parser("try-on", help="提交一组授权试穿商品图")
    tryon_flags(create)
    create.add_argument("--param", nargs="*")
    create.add_argument(
        "--routing",
        choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    create.add_argument("--output-dir", default=str(RESULTS))
    create.add_argument("--no-download", action="store_true")
    api_flags(create)
    create.set_defaults(handler=create_tryon)

    check = commands.add_parser("preview", help="只检查试穿说明")
    tryon_flags(check)
    check.set_defaults(handler=preview)

    query = commands.add_parser("status", help="查询试穿任务")
    query.add_argument("--task-id", required=True)
    api_flags(query)
    query.set_defaults(handler=show_status)

    media = commands.add_parser("upload", help="单独上传已授权参考图")
    media.add_argument("--file", required=True)
    api_flags(media)
    media.set_defaults(handler=upload_one)

    auth = commands.add_parser("auth", help="保存 AI Hive API Key")
    auth.add_argument("--api-key", required=True)
    auth.set_defaults(handler=save_auth)
    return root


def main():
    args = cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
