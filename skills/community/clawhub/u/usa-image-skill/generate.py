#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "customtkinter>=5.2.2",
#     "requests>=2.28.0",
# ]
# ///
"""Generate or edit images through the usa0.top OpenAI-compatible Images API."""

import argparse
import base64
import binascii
import datetime
import os
import re
import sys
import webbrowser
from pathlib import Path
from urllib.parse import unquote, urlparse

try:
    import requests
except ImportError:
    print("Error: requests 库未安装", file=sys.stderr)
    print("Run: uv run generate.py --help", file=sys.stderr)
    sys.exit(1)


DEFAULT_BASE_URL = "https://usa0.top"
DEFAULT_MODEL = "gpt-image-2"
MAX_INPUT_IMAGES = 16
MAX_INPUT_IMAGE_BYTES = 50 * 1024 * 1024
MAX_OUTPUT_IMAGE_BYTES = 100 * 1024 * 1024
SUPPORTED_IMAGE_TYPES = {
    "png": "image/png",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
}
OUTPUT_EXTENSIONS = {
    "png": ".png",
    "jpeg": ".jpg",
    "webp": ".webp",
}


class ImageGenerationError(Exception):
    """A user-facing image generation error."""


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="通过 usa0.top 的 OpenAI 兼容接口生成或编辑 GPT 图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 文生图
  uv run generate.py --prompt "可爱柴犬头像" --size 1024x1024

  # 使用本地图片编辑
  uv run generate.py --prompt "转换为油画风格" --input-image ./photo.png

  # 使用多张 URL 参考图
  uv run generate.py --prompt "融合两张图的风格" \\
    --input-image https://example.com/a.png \\
    --input-image https://example.com/b.jpg
        """,
    )
    parser.add_argument("--prompt", "-p", default=None, help="图片生成或编辑提示词")
    parser.add_argument(
        "--configure-key",
        action="store_true",
        help="打开本机弹窗，安全配置生图分组的 USA_API_KEY（Windows）",
    )
    parser.add_argument(
        "--api-key",
        "-k",
        default=None,
        help="USA API Key；未提供时读取 USA_API_KEY 环境变量",
    )
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"模型（默认：{DEFAULT_MODEL}）")
    parser.add_argument(
        "--input-image",
        "-i",
        action="append",
        dest="input_images",
        metavar="PATH_OR_URL",
        help="参考图的本地路径或 HTTP/HTTPS URL，可重复使用，最多 16 张",
    )
    parser.add_argument("--size", default="1024x1024", help="输出尺寸，格式 WIDTHxHEIGHT（默认：1024x1024）")
    parser.add_argument(
        "--quality",
        choices=["auto", "low", "medium", "high"],
        default="auto",
        help="输出质量（默认：auto）",
    )
    parser.add_argument(
        "--output-format",
        choices=["png", "jpeg", "webp"],
        default="png",
        help="输出格式（默认：png）",
    )
    parser.add_argument(
        "--background",
        choices=["auto", "opaque"],
        default="auto",
        help="背景模式（默认：auto）",
    )
    parser.add_argument(
        "--input-fidelity",
        choices=["low", "high"],
        default=None,
        help="参考图保真度，仅图生图时使用",
    )
    parser.add_argument("--n", type=int, default=1, help="生成数量，1-10（默认：1）")
    parser.add_argument("--filename", "-f", default=None, help="输出文件名，不得包含目录；多图会追加序号")
    parser.add_argument("--output-dir", default="./generated", help="输出目录（默认：./generated）")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"API 基础 URL（默认：{DEFAULT_BASE_URL}）；自定义地址会收到你的 API Key",
    )
    return parser.parse_args(argv)


def read_windows_user_api_key():
    if sys.platform != "win32":
        return None
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, "USA_API_KEY")
            return str(value).strip() or None
    except (FileNotFoundError, OSError):
        return None


def resolve_api_key(cli_api_key=None):
    return cli_api_key or os.environ.get("USA_API_KEY") or read_windows_user_api_key()


def save_windows_user_api_key(api_key):
    import winreg

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
        winreg.SetValueEx(key, "USA_API_KEY", 0, winreg.REG_SZ, api_key)
    os.environ["USA_API_KEY"] = api_key


def configure_api_key():
    if sys.platform != "win32":
        raise ImageGenerationError(
            "弹窗配置目前仅支持 Windows；请前往 https://usa0.top 获取生图分组密钥，"
            "并使用 export USA_API_KEY=\"你的密钥\" 配置环境变量"
        )

    try:
        import customtkinter as ctk
        import tkinter as tk
    except ImportError as exc:
        raise ImageGenerationError(
            "当前 Python 缺少 CustomTkinter 图形组件；请使用 uv run generate.py --configure-key，"
            "或手动配置 USA_API_KEY 环境变量"
        ) from exc

    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    try:
        root = ctk.CTk()
        root.title("USA GPT 生图密钥")
        root.geometry("560x610")
        root.resizable(False, False)
        root.configure(fg_color=("#F1F5F9", "#0F172A"))
        root.attributes("-topmost", True)
    except tk.TclError as exc:
        raise ImageGenerationError(
            "当前会话无法打开图形弹窗；请在 Windows 桌面会话中重试，或手动配置 USA_API_KEY"
        ) from exc

    result = {"code": 1}
    key_visible = tk.BooleanVar(value=False)
    group_confirmed = tk.BooleanVar(value=False)

    root.grid_columnconfigure(0, weight=1)

    container = ctk.CTkFrame(root, fg_color="transparent")
    container.grid(row=0, column=0, padx=36, pady=30, sticky="nsew")
    container.grid_columnconfigure(0, weight=1)

    brand = ctk.CTkLabel(
        container,
        text="USA GPT",
        font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
        text_color=("#2563EB", "#60A5FA"),
    )
    brand.grid(row=0, column=0, sticky="w")

    title = ctk.CTkLabel(
        container,
        text="配置生图分组密钥",
        font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
        text_color=("#0F172A", "#F8FAFC"),
    )
    title.grid(row=1, column=0, pady=(8, 4), sticky="w")

    subtitle = ctk.CTkLabel(
        container,
        text="密钥只保存在当前 Windows 用户环境变量中，不会出现在聊天或终端输出里。",
        font=ctk.CTkFont(family="Segoe UI", size=13),
        text_color=("#64748B", "#94A3B8"),
        justify="left",
        wraplength=480,
    )
    subtitle.grid(row=2, column=0, pady=(0, 18), sticky="w")

    notice = ctk.CTkFrame(
        container,
        corner_radius=8,
        border_width=1,
        border_color=("#FDBA74", "#9A5B24"),
        fg_color=("#FFF7ED", "#2B2118"),
    )
    notice.grid(row=3, column=0, sticky="ew")
    notice.grid_columnconfigure(0, weight=1)

    notice_title = ctk.CTkLabel(
        notice,
        text="仅支持“生图分组”密钥",
        font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
        text_color=("#9A3412", "#FDBA74"),
    )
    notice_title.grid(row=0, column=0, padx=16, pady=(12, 2), sticky="w")

    notice_text = ctk.CTkLabel(
        notice,
        text="聊天、视频或其他分组的 API Key 无法用于本技能。",
        font=ctk.CTkFont(family="Segoe UI", size=12),
        text_color=("#7C2D12", "#FED7AA"),
    )
    notice_text.grid(row=1, column=0, padx=16, pady=(0, 12), sticky="w")

    def open_provider_site():
        webbrowser.open("https://usa0.top")
        status_label.configure(text="已打开 usa0.top，请获取生图分组密钥后返回此窗口。", text_color=("#0369A1", "#7DD3FC"))

    site_button = ctk.CTkButton(
        container,
        text="前往 usa0.top 获取密钥",
        command=open_provider_site,
        height=38,
        corner_radius=6,
        fg_color="transparent",
        hover_color=("#E2E8F0", "#1E293B"),
        border_width=1,
        border_color=("#94A3B8", "#475569"),
        text_color=("#1E40AF", "#93C5FD"),
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
    )
    site_button.grid(row=4, column=0, pady=(14, 20), sticky="ew")

    field_label = ctk.CTkLabel(
        container,
        text="生图分组 API Key",
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        text_color=("#334155", "#E2E8F0"),
    )
    field_label.grid(row=5, column=0, pady=(0, 7), sticky="w")

    key_entry = ctk.CTkEntry(
        container,
        height=46,
        corner_radius=6,
        border_width=1,
        placeholder_text="在此输入密钥",
        show="●",
        font=ctk.CTkFont(family="Consolas", size=13),
    )
    key_entry.grid(row=6, column=0, sticky="ew")

    def toggle_key_visibility():
        key_entry.configure(show="" if key_visible.get() else "●")

    show_key = ctk.CTkCheckBox(
        container,
        text="显示密钥",
        variable=key_visible,
        command=toggle_key_visibility,
        corner_radius=4,
        checkbox_width=20,
        checkbox_height=20,
        font=ctk.CTkFont(family="Segoe UI", size=12),
    )
    show_key.grid(row=7, column=0, pady=(10, 16), sticky="w")

    group_check = ctk.CTkCheckBox(
        container,
        text="我确认这是从 usa0.top 获取的生图分组密钥",
        variable=group_confirmed,
        corner_radius=4,
        checkbox_width=20,
        checkbox_height=20,
        font=ctk.CTkFont(family="Segoe UI", size=12),
    )
    group_check.grid(row=8, column=0, sticky="w")

    status_label = ctk.CTkLabel(
        container,
        text="",
        height=38,
        font=ctk.CTkFont(family="Segoe UI", size=12),
        text_color=("#DC2626", "#FCA5A5"),
        justify="left",
        wraplength=480,
    )
    status_label.grid(row=9, column=0, pady=(8, 4), sticky="ew")

    actions = ctk.CTkFrame(container, fg_color="transparent")
    actions.grid(row=10, column=0, sticky="ew")
    actions.grid_columnconfigure((0, 1), weight=1)

    def close_dialog():
        root.destroy()

    def save_key():
        api_key = key_entry.get().strip()
        if not api_key:
            status_label.configure(text="请输入生图分组的 API Key。", text_color=("#DC2626", "#FCA5A5"))
            key_entry.focus_set()
            return
        if not group_confirmed.get():
            status_label.configure(text="请先确认这是生图分组密钥。", text_color=("#DC2626", "#FCA5A5"))
            return
        try:
            save_windows_user_api_key(api_key)
        except OSError as exc:
            status_label.configure(text=f"保存失败：{exc}", text_color=("#DC2626", "#FCA5A5"))
            return

        key_entry.delete(0, "end")
        key_entry.configure(state="disabled")
        show_key.configure(state="disabled")
        group_check.configure(state="disabled")
        save_button.configure(text="配置成功", state="disabled", fg_color=("#15803D", "#22C55E"))
        status_label.configure(
            text="USA_API_KEY 已保存。现在可以继续生成图片。",
            text_color=("#15803D", "#86EFAC"),
        )
        result["code"] = 0
        root.after(250, root.destroy)

    cancel_button = ctk.CTkButton(
        actions,
        text="取消",
        command=close_dialog,
        height=42,
        corner_radius=6,
        fg_color="transparent",
        hover_color=("#E2E8F0", "#1E293B"),
        border_width=1,
        border_color=("#94A3B8", "#475569"),
        text_color=("#334155", "#E2E8F0"),
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
    )
    cancel_button.grid(row=0, column=0, padx=(0, 6), sticky="ew")

    save_button = ctk.CTkButton(
        actions,
        text="保存并继续",
        command=save_key,
        height=42,
        corner_radius=6,
        fg_color=("#2563EB", "#3B82F6"),
        hover_color=("#1D4ED8", "#2563EB"),
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
    )
    save_button.grid(row=0, column=1, padx=(6, 0), sticky="ew")

    try:
        root.protocol("WM_DELETE_WINDOW", close_dialog)
        root.bind("<Escape>", lambda _event: close_dialog())
        root.bind("<Return>", lambda _event: save_key())
        root.update_idletasks()
        x = max((root.winfo_screenwidth() - root.winfo_width()) // 2, 0)
        y = max((root.winfo_screenheight() - root.winfo_height()) // 2, 0)
        root.geometry(f"+{x}+{y}")
        root.after(350, lambda: root.attributes("-topmost", False))
        key_entry.focus_set()
        root.mainloop()
        if result["code"] == 0:
            print("USA_API_KEY 已安全配置；密钥内容未输出")
        else:
            print("已取消密钥配置")
        return result["code"]
    except tk.TclError as exc:
        raise ImageGenerationError("密钥配置弹窗运行失败，请手动配置 USA_API_KEY") from exc
    finally:
        try:
            if root.winfo_exists():
                root.destroy()
        except tk.TclError:
            pass


def validate_args(args):
    if args.prompt is None:
        raise ImageGenerationError("缺少提示词：请使用 --prompt；配置密钥请使用 --configure-key")
    args.prompt = args.prompt.strip()
    if not args.prompt:
        raise ImageGenerationError("提示词不能为空")

    args.api_key = resolve_api_key(args.api_key)
    if not args.api_key:
        raise ImageGenerationError(
            "缺少 API Key：请前往 https://usa0.top 获取生图分组的 API Key，"
            "然后运行 python generate.py --configure-key 打开安全配置弹窗"
        )

    if not re.fullmatch(r"[1-9]\d*x[1-9]\d*", args.size):
        raise ImageGenerationError("--size 必须使用 WIDTHxHEIGHT 格式，例如 1024x1024")
    if not 1 <= args.n <= 10:
        raise ImageGenerationError("--n 必须在 1 到 10 之间")
    if args.input_images and len(args.input_images) > MAX_INPUT_IMAGES:
        raise ImageGenerationError(f"参考图不能超过 {MAX_INPUT_IMAGES} 张")
    if args.input_fidelity and not args.input_images:
        raise ImageGenerationError("--input-fidelity 只能与 --input-image 一起使用")

    parsed_base_url = urlparse(args.base_url)
    if parsed_base_url.scheme not in {"http", "https"} or not parsed_base_url.netloc:
        raise ImageGenerationError("--base-url 必须是有效的 HTTP/HTTPS 地址")
    args.base_url = args.base_url.rstrip("/")

    if args.filename:
        filename_path = Path(args.filename)
        if filename_path.is_absolute() or filename_path.name != args.filename or args.filename in {".", ".."}:
            raise ImageGenerationError("--filename 只能是文件名，不能包含目录或绝对路径")
        expected_suffix = OUTPUT_EXTENSIONS[args.output_format]
        if filename_path.suffix:
            accepted_suffixes = {expected_suffix}
            if args.output_format == "jpeg":
                accepted_suffixes.add(".jpeg")
            if filename_path.suffix.lower() not in accepted_suffixes:
                raise ImageGenerationError(f"文件扩展名必须与 --output-format {args.output_format} 一致")

    return args


def detect_image_type(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return None


def read_limited_response(response, max_bytes):
    content_length = response.headers.get("Content-Length")
    if content_length:
        try:
            if int(content_length) > max_bytes:
                raise ImageGenerationError(f"图片超过 {max_bytes // (1024 * 1024)} MB 限制")
        except ValueError:
            pass

    chunks = []
    total = 0
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if not chunk:
            continue
        total += len(chunk)
        if total > max_bytes:
            raise ImageGenerationError(f"图片超过 {max_bytes // (1024 * 1024)} MB 限制")
        chunks.append(chunk)
    return b"".join(chunks)


def download_image_bytes(url, max_bytes):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ImageGenerationError(f"无效的图片 URL：{url}")

    try:
        with requests.get(url, stream=True, timeout=(10, 60), allow_redirects=True) as response:
            response.raise_for_status()
            data = read_limited_response(response, max_bytes)
    except ImageGenerationError:
        raise
    except requests.exceptions.RequestException as exc:
        raise ImageGenerationError(f"下载图片失败：{url}：{exc}") from exc

    image_type = detect_image_type(data)
    if not image_type:
        raise ImageGenerationError(f"下载内容不是支持的 PNG、JPEG 或 WebP 图片：{url}")
    return data, image_type


def load_input_image(source, index):
    parsed = urlparse(source)
    is_windows_path = bool(re.match(r"^[A-Za-z]:[\\/]", source))
    if parsed.scheme in {"http", "https"}:
        data, image_type = download_image_bytes(source, MAX_INPUT_IMAGE_BYTES)
        remote_name = Path(unquote(parsed.path)).name
        filename = remote_name or f"reference-{index}{OUTPUT_EXTENSIONS[image_type]}"
    elif parsed.scheme and not is_windows_path:
        raise ImageGenerationError(f"参考图仅支持本地路径或 HTTP/HTTPS URL：{source}")
    else:
        path = Path(source).expanduser()
        if not path.is_file():
            raise ImageGenerationError(f"参考图不存在或不是文件：{source}")
        size = path.stat().st_size
        if size > MAX_INPUT_IMAGE_BYTES:
            raise ImageGenerationError(f"参考图超过 50 MB：{source}")
        try:
            data = path.read_bytes()
        except OSError as exc:
            raise ImageGenerationError(f"读取参考图失败：{source}：{exc}") from exc
        image_type = detect_image_type(data)
        if not image_type:
            raise ImageGenerationError(f"参考图必须是 PNG、JPEG 或 WebP：{source}")
        filename = path.name

    extension = OUTPUT_EXTENSIONS[image_type]
    if Path(filename).suffix.lower() not in {extension, ".jpeg" if image_type == "jpeg" else extension}:
        filename = f"{Path(filename).stem or f'reference-{index}'}{extension}"
    return filename, data, SUPPORTED_IMAGE_TYPES[image_type]


def authorization_headers(api_key):
    return {"Authorization": f"Bearer {api_key}"}


def request_images(args):
    common_fields = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "quality": args.quality,
        "output_format": args.output_format,
        "background": args.background,
        "n": args.n,
    }
    headers = authorization_headers(args.api_key)

    try:
        if args.input_images:
            url = f"{args.base_url}/v1/images/edits"
            files = []
            for index, source in enumerate(args.input_images, start=1):
                filename, data, media_type = load_input_image(source, index)
                files.append(("image[]", (filename, data, media_type)))
            form_fields = {key: str(value) for key, value in common_fields.items()}
            if args.input_fidelity:
                form_fields["input_fidelity"] = args.input_fidelity
            response = requests.post(url, data=form_fields, files=files, headers=headers, timeout=(30, 300))
        else:
            url = f"{args.base_url}/v1/images/generations"
            response = requests.post(url, json=common_fields, headers=headers, timeout=(30, 300))
        response.raise_for_status()
    except ImageGenerationError:
        raise
    except requests.exceptions.RequestException as exc:
        detail = ""
        if exc.response is not None:
            detail = f"；响应：{exc.response.text[:1000]}"
        raise ImageGenerationError(f"API 请求失败：{exc}{detail}") from exc

    try:
        payload = response.json()
    except (ValueError, requests.exceptions.JSONDecodeError) as exc:
        raise ImageGenerationError("API 返回了无效 JSON") from exc

    if isinstance(payload, dict) and payload.get("error"):
        error = payload["error"]
        message = error.get("message") if isinstance(error, dict) else str(error)
        raise ImageGenerationError(f"API 返回错误：{message}")

    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, list) or not data:
        raise ImageGenerationError("API 响应中没有图片数据")

    results = []
    for item in data:
        if not isinstance(item, dict):
            continue
        if item.get("b64_json"):
            results.append(("base64", item["b64_json"]))
        elif item.get("url"):
            results.append(("url", item["url"]))
    if not results:
        raise ImageGenerationError("API 响应中没有可保存的 b64_json 或 url")
    return results


def safe_component(value, fallback):
    cleaned = re.sub(r"[^\w\u4e00-\u9fff-]", "_", value).strip("_")
    return cleaned[:30] or fallback


def base_output_name(args):
    extension = OUTPUT_EXTENSIONS[args.output_format]
    if args.filename:
        filename = Path(args.filename)
        return filename.stem, filename.suffix or extension

    date_str = datetime.datetime.now().strftime("%Y%m%d")
    model = safe_component(args.model, "gpt-image")
    prompt = safe_component(args.prompt, "image")
    return f"{date_str}_{model}_{prompt}", extension


def decode_result(result_type, value):
    if result_type == "url":
        data, _ = download_image_bytes(value, MAX_OUTPUT_IMAGE_BYTES)
        return data
    try:
        data = base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ImageGenerationError("API 返回了无效的 Base64 图片数据") from exc
    if not detect_image_type(data):
        raise ImageGenerationError("API 返回的 Base64 内容不是支持的图片")
    return data


def save_results(args, results):
    output_dir = Path(args.output_dir).expanduser()
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ImageGenerationError(f"无法创建输出目录：{output_dir}：{exc}") from exc

    stem, extension = base_output_name(args)
    paths = []
    multiple = len(results) > 1
    for index, result in enumerate(results, start=1):
        suffix = f"_{index}" if multiple else ""
        output_path = output_dir / f"{stem}{suffix}{extension}"
        try:
            output_path.write_bytes(decode_result(*result))
        except OSError as exc:
            raise ImageGenerationError(f"保存图片失败：{output_path}：{exc}") from exc
        paths.append(output_path.resolve())
    return paths


def main(argv=None):
    try:
        args = parse_args(argv)
        if args.configure_key:
            return configure_api_key()
        args = validate_args(args)
        mode = "图生图" if args.input_images else "文生图"
        print("=" * 60)
        print("USA GPT 图片生成")
        print("=" * 60)
        print(f"模式：{mode}")
        print(f"模型：{args.model}")
        print(f"尺寸：{args.size}")
        print(f"质量：{args.quality}")
        print(f"格式：{args.output_format}")
        if args.input_images:
            print(f"参考图：{len(args.input_images)} 张")
        if args.base_url != DEFAULT_BASE_URL:
            print(f"警告：API Key 将发送到自定义地址 {args.base_url}")
        print("正在请求图片...")

        results = request_images(args)
        paths = save_results(args, results)
        print(f"完成，共保存 {len(paths)} 张图片：")
        for path in paths:
            print(f"MEDIA: {path}")
        return 0
    except ImageGenerationError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
