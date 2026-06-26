"""
图可丽视觉 API Skill — 主调用脚本

支持：通用抠图、人脸变清晰、AI背景更换（异步）。
支持文件上传和图片URL两种输入方式，返回二进制流或Base64编码结果。
AI背景更换为异步接口，需先提交任务再查询结果。

重要：API 请求域名为 picupapi.tukeli.net，与官网 www.tukeli.net 不同。

用法：
    python tukeli.py --api matting --image photo.jpg --output out.png
    python tukeli.py --api matting --url "https://example.com/photo.jpg"
    python tukeli.py --api matting --image photo.jpg --crop --bgcolor FFFFFF
    python tukeli.py --api matting --matting-type 1 --image portrait.jpg
    python tukeli.py --api face-clear --image blurry.jpg --output hd.png
    python tukeli.py --api ai-bg --submit --image-url "https://..." --text "海滩背景"
    python tukeli.py --api ai-bg --query --task-id 12345

版本：1.0.0
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))

from config import (
    API_BASE,
    ENDPOINTS,
    MATTING_TYPE,
    OUTPUT_DIR,
    OUTPUT_SETTINGS,
    USER_AGENT,
    get_api_key,
    validate_image_file,
)


# ── 异常 ──────────────────────────────────────────────────────────────────────


class APIError(Exception):
    """图可丽 API 通用错误。"""
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(APIError):
    """API Key 无效或缺失。"""
    pass


class InsufficientCreditsError(APIError):
    """账户余额不足。"""
    pass


class RateLimitError(APIError):
    """请求频率超限（429）。"""
    pass


# ── API 调用 ──────────────────────────────────────────────────────────────────


def _call_api_upload(
    endpoint: str,
    api_key: str,
    image_path: Path,
    url_params: dict,
    timeout: int = 120,
) -> tuple[bytes | dict, str]:
    """
    文件上传模式 API 调用（POST multipart/form-data）。
    url_params 中的参数附加在 URL 后面（如 mattingType、crop、bgcolor 等）。
    """
    url = f"{API_BASE}{endpoint}"
    headers = {
        "APIKEY": api_key,
        "User-Agent": USER_AGENT,
    }

    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/jpeg")}
        resp = requests.post(
            url,
            params=url_params,
            files=files,
            headers=headers,
            timeout=timeout,
        )

    _raise_for_status(resp)
    content_type = resp.headers.get("Content-Type", "")
    if "application/json" in content_type:
        return resp.json(), "application/json"
    return resp.content, content_type


def _call_api_url_mode(
    endpoint: str,
    api_key: str,
    image_url: str,
    url_params: dict,
    timeout: int = 120,
) -> tuple[dict, str]:
    """图片 URL 模式 API 调用（GET）。"""
    url = f"{API_BASE}{endpoint}"
    headers = {
        "APIKEY": api_key,
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    all_params = {"url": image_url, **url_params}

    resp = requests.get(url, params=all_params, headers=headers, timeout=timeout)
    _raise_for_status(resp)
    return resp.json(), "application/json"


def _call_api_json(
    endpoint: str,
    api_key: str,
    body: dict,
    method: str = "POST",
    timeout: int = 120,
) -> dict:
    """JSON 请求模式（用于 AI背景更换）。"""
    url = f"{API_BASE}{endpoint}"
    headers = {
        "APIKEY": api_key,
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    }

    if method == "POST":
        resp = requests.post(url, json=body, headers=headers, timeout=timeout)
    else:
        resp = requests.get(url, params=body, headers=headers, timeout=timeout)

    _raise_for_status(resp)
    return resp.json()


def _raise_for_status(resp: requests.Response) -> None:
    """根据 HTTP 状态码抛出对应异常。"""
    if resp.status_code == 200:
        return
    try:
        body = resp.json()
        msg = body.get("msg") or json.dumps(body, ensure_ascii=False)
    except Exception:
        msg = resp.text[:300]

    if resp.status_code == 401:
        raise AuthenticationError(f"API Key 无效或缺失：{msg}", resp.status_code)
    if resp.status_code == 429:
        raise RateLimitError(f"请求频率超限：{msg}", resp.status_code)
    try:
        code = resp.json().get("code", 0)
        if code == 1001:
            raise InsufficientCreditsError(f"账户余额不足：{msg}", code)
    except (InsufficientCreditsError, AuthenticationError, RateLimitError):
        raise
    except Exception:
        pass
    raise APIError(f"HTTP {resp.status_code}：{msg}", resp.status_code)


# ── 核心处理 ──────────────────────────────────────────────────────────────────


def process_matting_or_face_clear(
    api: str,
    image_path: str | None = None,
    image_url: str | None = None,
    output_path: Path | None = None,
    use_base64: bool = False,
    matting_type: int = 6,
    crop: bool = False,
    bgcolor: str | None = None,
    output_format: str = "png",
    face_analysis: bool = False,
    api_key: str | None = None,
) -> dict:
    """
    调用通用抠图或人脸变清晰 API。

    返回结果字典：
    {
        "path": Path | None,
        "base64": str | None,
        "face_analysis": dict | None,
        "size_kb": float,
        "time_s": float,
    }
    """
    key = api_key or get_api_key()
    if not key:
        print(
            "\n错误：未找到 TUKELI_API_KEY！\n"
            "请在 .env 文件中配置：TUKELI_API_KEY=你的密钥\n"
            "获取密钥：https://www.tukeli.net\n",
            file=sys.stderr,
        )
        sys.exit(1)

    # 构建 URL 参数
    url_params: dict = {}
    if api == "matting":
        url_params["mattingType"] = matting_type
    else:  # face-clear
        url_params["mattingType"] = MATTING_TYPE["face-clear"]

    if crop:
        url_params["crop"] = "true"
    if bgcolor:
        url_params["bgcolor"] = bgcolor
    if output_format != "png":
        url_params["outputFormat"] = output_format
    if face_analysis and use_base64:
        url_params["faceAnalysis"] = "true"

    # 选择端点
    api_key_map = api.replace("-", "_")
    if image_url:
        endpoint_key = f"{api_key_map}_url"
    elif use_base64:
        endpoint_key = f"{api_key_map}_base64"
    else:
        endpoint_key = f"{api_key_map}_binary"

    endpoint = ENDPOINTS[endpoint_key]

    # 执行调用（带重试）
    max_retries = 3
    start_time = time.time()
    data = None
    content_type = ""

    for attempt in range(max_retries):
        try:
            if image_url:
                data, content_type = _call_api_url_mode(endpoint, key, image_url, url_params)
            else:
                validated = validate_image_file(image_path, api)
                data, content_type = _call_api_upload(endpoint, key, validated, url_params)
            break

        except AuthenticationError as e:
            print(f"错误：{e}", file=sys.stderr)
            sys.exit(1)

        except InsufficientCreditsError as e:
            print(f"错误：{e}", file=sys.stderr)
            sys.exit(1)

        except RateLimitError:
            wait = 15 * (attempt + 1)
            print(f"请求频率超限，{wait}秒后重试...", file=sys.stderr)
            time.sleep(wait)

        except APIError as e:
            if attempt < max_retries - 1:
                wait = 5 * (attempt + 1)
                print(f"请求失败，{wait}秒后重试（{attempt + 1}/{max_retries}）...", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"错误：{e}", file=sys.stderr)
                sys.exit(1)

        except Exception as e:
            print(f"未知错误：{type(e).__name__}: {e}", file=sys.stderr)
            if attempt >= max_retries - 1:
                sys.exit(1)
            time.sleep(5)

    elapsed = time.time() - start_time

    if data is None:
        print("错误：所有重试均失败。", file=sys.stderr)
        sys.exit(1)

    result: dict = {
        "path": None,
        "base64": None,
        "face_analysis": None,
        "size_kb": 0.0,
        "time_s": round(elapsed, 1),
    }

    if isinstance(data, bytes):
        output_dir = output_path.parent if output_path else OUTPUT_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        if output_path:
            filepath = output_path
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = OUTPUT_DIR / f"{api}_{timestamp}.png"

        filepath.write_bytes(data)
        size_kb = len(data) / 1024
        result["path"] = filepath
        result["size_kb"] = round(size_kb, 1)

        if OUTPUT_SETTINGS["save_metadata"]:
            meta = {
                "api": api,
                "image_path": str(image_path) if image_path else None,
                "image_url": image_url,
                "params": url_params,
                "generation_time_seconds": round(elapsed, 2),
                "file_size_kb": round(size_kb, 1),
                "generated_at": datetime.now().isoformat(),
            }
            meta_path = filepath.parent / f"{filepath.name}.meta.json"
            meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    elif isinstance(data, dict):
        resp_data = data.get("data", {})
        img_b64 = resp_data.get("imageBase64", "")
        result["base64"] = img_b64
        result["size_kb"] = round(len(img_b64) * 3 / 4 / 1024, 1)

        if "faceAnalysis" in resp_data:
            result["face_analysis"] = resp_data["faceAnalysis"]

        if output_path and img_b64:
            import base64
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(base64.b64decode(img_b64))
            result["path"] = output_path

    return result


def submit_ai_bg(
    image_url: str | None = None,
    image_base64: str | None = None,
    text: str = "",
    api_key: str | None = None,
) -> dict:
    """提交 AI背景更换任务，返回 task_id。"""
    key = api_key or get_api_key()
    if not key:
        print("\n错误：未找到 TUKELI_API_KEY！", file=sys.stderr)
        sys.exit(1)

    if not image_url and not image_base64:
        print("错误：--image-url 或 --image-base64 至少填一个。", file=sys.stderr)
        sys.exit(1)

    body: dict = {"text": text}
    if image_url:
        body["imgUrl"] = image_url
    if image_base64:
        body["imgBase64"] = image_base64

    try:
        resp = _call_api_json(ENDPOINTS["ai_bg_submit"], key, body, method="POST")
        task_id = resp.get("data")
        return {"task_id": task_id, "raw": resp}
    except (AuthenticationError, InsufficientCreditsError) as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"提交任务失败：{e}", file=sys.stderr)
        sys.exit(1)


def query_ai_bg(task_id: int, api_key: str | None = None) -> dict:
    """查询 AI背景更换任务结果。"""
    key = api_key or get_api_key()
    if not key:
        print("\n错误：未找到 TUKELI_API_KEY！", file=sys.stderr)
        sys.exit(1)

    try:
        resp = _call_api_json(
            ENDPOINTS["ai_bg_query"], key, {"taskId": task_id}, method="GET"
        )
        data = resp.get("data", {})
        return {
            "task_id": task_id,
            "status": data.get("status"),
            "percentage": data.get("percentage", 0),
            "result_url": data.get("resultUrl"),
            "raw": resp,
        }
    except Exception as e:
        print(f"查询任务失败：{e}", file=sys.stderr)
        sys.exit(1)


# ── CLI ───────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="图可丽视觉 API — 通用抠图 / 人脸变清晰 / AI背景更换",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  python tukeli.py --api matting --image photo.jpg --output out.png\n"
            "  python tukeli.py --api matting --url \"https://example.com/photo.jpg\"\n"
            "  python tukeli.py --api matting --image photo.jpg --crop --bgcolor FFFFFF\n"
            "  python tukeli.py --api matting --matting-type 1 --image portrait.jpg\n"
            "  python tukeli.py --api face-clear --image blurry.jpg --output hd.png\n"
            "  python tukeli.py --api ai-bg --submit --image-url \"https://...\" --text \"海滩背景\"\n"
            "  python tukeli.py --api ai-bg --query --task-id 12345\n"
        ),
    )

    parser.add_argument(
        "--api",
        required=True,
        choices=["matting", "face-clear", "ai-bg"],
        help="选择API：matting（通用抠图）、face-clear（人脸变清晰）、ai-bg（AI背景更换）",
    )

    # 输入（matting/face-clear）
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--image", type=str, help="本地图片文件路径（matting/face-clear）")
    input_group.add_argument("--url", type=str, help="图片URL（URL模式，matting/face-clear）")

    # 输出
    parser.add_argument("--output", type=Path, default=None, help="输出文件路径（默认保存到 data/outputs/）")
    parser.add_argument("--base64", action="store_true", help="返回Base64 JSON而非二进制流")
    parser.add_argument("--json", action="store_true", help="以JSON格式输出结果信息")

    # 抠图参数
    parser.add_argument("--matting-type", type=int, default=6, choices=[1, 2, 3, 6],
                        help="抠图类型：1人像、2物体、3头像、6通用（默认6，仅matting）")
    parser.add_argument("--crop", action="store_true", help="裁剪空白区域（仅matting）")
    parser.add_argument("--bgcolor", type=str, default=None, help="背景颜色，十六进制（如FFFFFF）")
    parser.add_argument("--output-format", type=str, default="png",
                        help="输出格式：png、webp、jpg_75等（默认：png）")
    parser.add_argument("--face-analysis", action="store_true",
                        help="返回人脸关键点（仅matting --base64）")

    # AI背景更换参数
    parser.add_argument("--submit", action="store_true", help="提交AI背景更换任务")
    parser.add_argument("--query", action="store_true", help="查询AI背景更换任务结果")
    parser.add_argument("--image-url", type=str, default=None, help="输入图片URL（ai-bg --submit）")
    parser.add_argument("--image-base64", type=str, default=None, help="输入图片Base64（ai-bg --submit）")
    parser.add_argument("--text", type=str, default="", help="背景描述文字（ai-bg --submit）")
    parser.add_argument("--task-id", type=int, default=None, help="任务ID（ai-bg --query）")

    args = parser.parse_args()

    # URL 模式强制使用 Base64
    use_base64 = args.base64 or bool(args.url)

    print("=" * 55)
    print("  图可丽视觉 API")
    print("=" * 55)
    print(f"  API：        {args.api}")

    # ── AI背景更换 ──
    if args.api == "ai-bg":
        if args.submit:
            print(f"  模式：       提交任务")
            if args.image_url:
                print(f"  图片URL：    {args.image_url}")
            print(f"  背景描述：   {args.text}")
            print("=" * 55)
            print()
            result = submit_ai_bg(
                image_url=args.image_url,
                image_base64=args.image_base64,
                text=args.text,
            )
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"✅ 任务已提交！任务ID：{result['task_id']}")
                print(f"   使用以下命令查询结果：")
                print(f"   python tukeli.py --api ai-bg --query --task-id {result['task_id']}")

        elif args.query:
            if not args.task_id:
                print("错误：--query 模式需要提供 --task-id", file=sys.stderr)
                sys.exit(1)
            print(f"  模式：       查询结果")
            print(f"  任务ID：     {args.task_id}")
            print("=" * 55)
            print()
            result = query_ai_bg(args.task_id)
            status_map = {0: "生成中", 1: "已完成", 2: "处理失败", 3: "排队中"}
            status_str = status_map.get(result["status"], f"未知({result['status']})")

            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"  状态：{status_str}（{result['percentage']}%）")
                if result["status"] == 1:
                    print(f"✅ 处理完成！结果图（5分钟内有效）：")
                    print(f"   {result['result_url']}")
                elif result["status"] == 2:
                    print("❌ 处理失败，请重新提交任务。")
                else:
                    print(f"   请稍后再次查询...")
        else:
            print("错误：ai-bg 模式需要指定 --submit 或 --query", file=sys.stderr)
            sys.exit(1)
        return

    # ── 通用抠图 / 人脸变清晰 ──
    if not args.image and not args.url:
        print("错误：matting/face-clear 模式需要提供 --image 或 --url", file=sys.stderr)
        sys.exit(1)

    if args.image:
        print(f"  图片：       {args.image}")
    if args.url:
        print(f"  图片URL：    {args.url}")
    if args.api == "matting":
        print(f"  抠图类型：   {args.matting_type}")
    if args.crop:
        print(f"  裁剪：       是")
    if args.bgcolor:
        print(f"  背景颜色：   {args.bgcolor}")
    print("=" * 55)
    print()

    result = process_matting_or_face_clear(
        api=args.api,
        image_path=args.image,
        image_url=args.url,
        output_path=args.output,
        use_base64=use_base64,
        matting_type=args.matting_type,
        crop=args.crop,
        bgcolor=args.bgcolor,
        output_format=args.output_format,
        face_analysis=args.face_analysis,
    )

    if args.json:
        output_info = {
            "api": args.api,
            "path": str(result["path"]) if result["path"] else None,
            "has_base64": bool(result["base64"]),
            "has_face_analysis": bool(result["face_analysis"]),
            "size_kb": result["size_kb"],
            "time_s": result["time_s"],
        }
        print(json.dumps(output_info, indent=2, ensure_ascii=False))
    else:
        if result["path"]:
            print(f"✅ 图片已保存：{result['path']}")
            print(f"   大小：{result['size_kb']:.1f} KB")
        if result["base64"] and not result["path"]:
            print(f"✅ Base64 数据已获取（{result['size_kb']:.1f} KB）")
            print(f"   前64字符：{result['base64'][:64]}...")
        if result["face_analysis"]:
            fa = result["face_analysis"]
            print(f"   人脸数量：{fa.get('face_num', 0)}")
            print(f"   关键点数：{len(fa.get('point', [[]])[0]) if fa.get('point') else 0}")
        print(f"   处理时间：{result['time_s']}s")


if __name__ == "__main__":
    main()
