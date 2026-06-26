#!/usr/bin/env python3
"""OpenClaw 回收 Skill 调用脚本。"""

import argparse
import base64
import json
import mimetypes
import os
import re
import subprocess
import sys
import tempfile
from urllib import request
from urllib.error import HTTPError

STATE_DIR = os.path.expanduser("~/.openclaw/state/zhuanzhuan-recycle-estimator")
STATE_FILE = os.path.join(STATE_DIR, ".skill_state.json")
THREAD_ENV_KEYS = (
    "CLAUDE_CONVERSATION_ID",
    "CLAUDE_SESSION_ID",
    "CLAUDE_THREAD_ID",
    "ANTHROPIC_SESSION_ID",
    "CODEX_THREAD_ID",
)


def parse_bool(value):
    """解析布尔字符串。"""
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError("无效的布尔值: {0}".format(value))


def resolve_thread_scope():
    """解析当前会话标识，用于对话级状态隔离。"""
    for key in THREAD_ENV_KEYS:
        value = os.getenv(key, "").strip()
        if value:
            return value
    return None


def resolve_state_file():
    """解析当前请求应使用的状态文件路径。"""
    thread_scope = resolve_thread_scope()
    if not thread_scope:
        return STATE_FILE

    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", thread_scope).strip("_")
    if not normalized:
        return STATE_FILE
    return os.path.join(STATE_DIR, ".skill_state_{0}.json".format(normalized))


def load_state():
    """加载最近一次调用状态。"""
    state_file = resolve_state_file()
    if not os.path.exists(state_file):
        return {}
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def ensure_parent_dir(path):
    """兼容旧版本 Python 的目录创建。"""
    parent_dir = os.path.dirname(path)
    if parent_dir and not os.path.isdir(parent_dir):
        os.makedirs(parent_dir)


def save_state(state):
    """保存最近一次调用状态。"""
    state_file = resolve_state_file()
    ensure_parent_dir(state_file)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def parse_json_argument(raw, argument_name):
    """解析命令行中的 JSON 对象参数。"""
    try:
        parsed = json.loads(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "{0} 必须是合法 JSON: {1}".format(argument_name, exc)
        )
    if not isinstance(parsed, dict):
        raise argparse.ArgumentTypeError("{0} 必须是 JSON 对象".format(argument_name))
    return parsed


_MIME_FALLBACK = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
}
FILE_SIZE_WARN_BYTES = 5 * 1024 * 1024
COMPRESS_THRESHOLD_BYTES = 1 * 1024 * 1024
COMPRESS_MAX_DIMENSION = 2048


def _has_command(cmd):
    """检查系统命令是否可用。"""
    try:
        subprocess.run([cmd, "--version"], capture_output=True)
        return True
    except FileNotFoundError:
        return False


def _compress_with_sips(image_path, tmp_path, max_dim, quality):
    """macOS sips 压缩。"""
    subprocess.run(
        [
            "sips",
            "-s", "format", "jpeg",
            "-s", "formatOptions", str(quality),
            "--resampleHeightWidthMax", str(max_dim),
            image_path,
            "--out", tmp_path,
        ],
        capture_output=True,
        check=True,
    )


def _compress_with_convert(image_path, tmp_path, max_dim, quality):
    """ImageMagick convert 压缩（Linux 常用）。"""
    subprocess.run(
        [
            "convert",
            image_path,
            "-resize", "{0}x{0}>".format(max_dim),
            "-quality", str(quality),
            "-auto-orient",
            tmp_path,
        ],
        capture_output=True,
        check=True,
    )


def _compress_image(image_path):
    """自动检测可用工具压缩图片，支持 macOS(sips) 和 Linux(ImageMagick)。

    返回 (压缩后字节, mime_type) 或 None。
    """
    # 检测可用的压缩工具
    if _has_command("sips"):
        compress_fn = _compress_with_sips
        tool_name = "sips"
    elif _has_command("convert"):
        compress_fn = _compress_with_convert
        tool_name = "convert"
    else:
        print(
            "警告: 未找到图片压缩工具（需要 macOS sips 或 ImageMagick convert）",
            file=sys.stderr,
        )
        return None

    original_size = os.path.getsize(image_path)
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".jpg")
    os.close(tmp_fd)
    try:
        # 第一轮：质量 70，最大边 2048
        compress_fn(image_path, tmp_path, COMPRESS_MAX_DIMENSION, 70)

        # 如果还是太大，第二轮：质量 40，最大边 1600
        if os.path.getsize(tmp_path) > COMPRESS_THRESHOLD_BYTES:
            compress_fn(image_path, tmp_path, 1600, 40)

        with open(tmp_path, "rb") as f:
            compressed_bytes = f.read()

        print(
            "图片压缩({0}): {1} {2:.1f}MB -> {3:.1f}MB".format(
                tool_name,
                os.path.basename(image_path),
                original_size / 1024.0 / 1024.0,
                len(compressed_bytes) / 1024.0 / 1024.0,
            ),
            file=sys.stderr,
        )
        return compressed_bytes, "image/jpeg"
    except (subprocess.CalledProcessError, OSError) as exc:
        print("警告: {0} 压缩失败: {1}".format(tool_name, exc), file=sys.stderr)
        return None
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def resolve_image_source(image_value):
    """URL 直接返回；本地文件读取后返回 data URI，大于 1MB 自动压缩。"""
    if image_value.startswith(("http://", "https://")):
        return image_value, None

    if not os.path.isfile(image_value):
        return image_value, None  # 保持向后兼容

    file_size = os.path.getsize(image_value)

    # 大于 1MB 时自动压缩
    if file_size > COMPRESS_THRESHOLD_BYTES:
        result = _compress_image(image_value)
        if result:
            compressed_bytes, mime_type = result
            b64_str = base64.b64encode(compressed_bytes).decode("ascii")
            return "data:{0};base64,{1}".format(mime_type, b64_str), mime_type
        print(
            "警告: 图片压缩失败，使用原图 ({0:.1f}MB)".format(file_size / 1024.0 / 1024.0),
            file=sys.stderr,
        )

    if file_size > FILE_SIZE_WARN_BYTES:
        print(
            "警告: 图片 {0} 大小 {1:.1f} MB，base64 后约 {2:.1f} MB".format(
                os.path.basename(image_value),
                file_size / 1024.0 / 1024.0,
                file_size * 4.0 / 3.0 / 1024.0 / 1024.0,
            ),
            file=sys.stderr,
        )

    mime_type, _ = mimetypes.guess_type(image_value)
    if not mime_type:
        ext = os.path.splitext(image_value)[1].lower()
        mime_type = _MIME_FALLBACK.get(ext, "application/octet-stream")

    with open(image_value, "rb") as f:
        b64_str = base64.b64encode(f.read()).decode("ascii")

    return "data:{0};base64,{1}".format(mime_type, b64_str), mime_type


def build_structured_attachments(args):
    """构造图片和结构化选项附件。"""
    attachments = []

    for index, image_value in enumerate(args.image):
        media_id = args.image_media_id[index] if index < len(args.image_media_id) else None
        resolved_url, mime_type = resolve_image_source(image_value)
        payload_dict = {
            "url": resolved_url,
            "signed_url": resolved_url,
            "media_id": media_id,
            "source": args.image_source,
        }
        if mime_type:
            payload_dict["mime_type"] = mime_type
        attachments.append({"type": "image", "payload": payload_dict})

    for raw_attrs in args.attrs:
        attachments.append(
            {
                "type": "attrs",
                "payload": parse_json_argument(raw_attrs, "--attrs"),
            }
        )

    for raw_model_option in args.model_option:
        attachments.append(
            {
                "type": "model_option",
                "payload": parse_json_argument(raw_model_option, "--model-option"),
            }
        )

    return attachments


def build_payload(args):
    """构造请求体。"""
    state = load_state()
    attachments = build_structured_attachments(args)

    message = {
        "role": "user",
        "content": args.text,
    }
    if attachments:
        message["attachments"] = attachments

    client_info = {
        "user_agent": "claude-code-openclaw-recycle-skill",
    }
    resolved_client_ip = args.client_ip or state.get("client_ip")
    if resolved_client_ip:
        client_info["ip"] = resolved_client_ip

    payload = {
        "messages": [message],
        "context_control": {
            "allow_auto_resume": args.allow_auto_resume,
            "force_new_session": args.force_new_session,
        },
        "client_info": client_info,
    }

    resolved_skill_token = args.skill_token or state.get("skill_token")
    resolved_session_id = args.session_id or state.get("session_id")

    if resolved_skill_token:
        payload["skill_token"] = resolved_skill_token
    if resolved_session_id:
        payload["session_id"] = resolved_session_id

    return payload


def format_request_error(exc):
    """格式化请求异常，优先透传后端错误码和错误信息。"""
    if isinstance(exc, HTTPError):
        error_message = "HTTP {0}: {1}".format(exc.code, exc.reason)
        try:
            response_body = exc.read().decode("utf-8")
            parsed = json.loads(response_body)
            backend_code = parsed.get("error_code")
            backend_message = parsed.get("error_message")
            if backend_code or backend_message:
                details = " | ".join(part for part in [backend_code, backend_message] if part)
                return "{0} | {1}".format(error_message, details)
        except Exception:
            return error_message
        return error_message
    return str(exc)


def main():
    """脚本入口。"""
    parser = argparse.ArgumentParser(description="调用 OpenClaw 回收估价接口")
    parser.add_argument("--text", required=True, help="用户输入文本")
    parser.add_argument(
        "--image", action="append", default=[], help="图片 URL 或本地文件路径，可传多次；本地文件会自动 base64 编码"
    )
    parser.add_argument(
        "--image-media-id", action="append", default=[], help="图片 media_id，可传多次并与 --image 对齐"
    )
    parser.add_argument("--image-source", default="openclaw_im", help="图片来源标识")
    parser.add_argument("--attrs", action="append", default=[], help='核心属性附件 JSON，如 {"capacityId":"678742"}')
    parser.add_argument(
        "--model-option",
        action="append",
        default=[],
        help='型号选项附件 JSON，如 {"selected_id":"1011385","selected_name":"iPhone 17 Pro"}',
    )
    parser.add_argument("--skill-token", help="上一轮返回的 skill_token")
    parser.add_argument("--session-id", help="上一轮返回的 session_id")
    parser.add_argument("--client-ip", help="透传给接口的测试 IP，未传时默认复用本地状态")
    parser.add_argument("--reset-state", action="store_true", help="清空本地缓存的 skill_token/session_id")
    parser.add_argument("--allow-auto-resume", type=parse_bool, default=True, help="是否允许自动续接")
    parser.add_argument("--force-new-session", type=parse_bool, default=False, help="是否强制新建 session")
    parser.add_argument(
        "--base-url",
        default="https://zai.zhuanzhuan.com/zai/find_mate/v1/openclaw/recycle-skill/valuate",
        help="接口地址",
    )
    args = parser.parse_args()

    state_file = resolve_state_file()
    if args.reset_state and os.path.exists(state_file):
        os.remove(state_file)

    payload = build_payload(args)
    body = json.dumps(payload).encode("utf-8")
    http_request = request.Request(
        url=args.base_url,
        data=body,
        headers={"Content-Type": "application/json"},
    )

    try:
        with request.urlopen(http_request, timeout=60) as response:
            response_body = response.read().decode("utf-8")
            parsed = json.loads(response_body)
            if parsed.get("success"):
                save_state(
                    {
                        "skill_token": parsed.get("skill_token"),
                        "session_id": parsed.get("session_id"),
                        "valuation_context_id": parsed.get("valuation_context_id"),
                        "client_ip": payload.get("client_info", {}).get("ip"),
                    }
                )
                # 如果是最终价格报告（有 reply 字段），拼接免责声明
                reply = parsed.get("reply")
                if reply:
                    parsed["reply"] = "{0}\n\n----\n本次评估来自转转，如需回收请到转转APP".format(reply.rstrip())

                # 拼接图片 CDN 前缀并生成型号选项文本
                cdn_prefix = "https://pic5.zhuanstatic.com/zhuanzh/"
                clarification = parsed.get("clarification")
                if clarification:
                    # 生成型号选项文本
                    markdown_lines = []
                    # 1. 处理核心属性选项（容量、颜色等）
                    core_attrs = clarification.get("core_attribute_options", [])
                    for attr in core_attrs:
                        attr_name = attr.get("attribute_name", "")
                        display_type = attr.get("display_type", 1)

                        if attr_name:
                            if display_type == 2:
                                markdown_lines.append(f"**{attr_name}**")
                            else:
                                markdown_lines.append(f"\n请选择{attr_name}：")

                        for option in attr.get("options", []):
                            option_id = option.get("id", "")
                            option_name = option.get("name", "")
                            if option_name:
                                markdown_lines.append(f"- {option_name}")
                    for group in clarification.get("model_option_groups", []):
                        group_name = group.get("group_name", "")
                        if group_name:
                            markdown_lines.append(f"**{group_name}**")

                        for option in group.get("options", []):
                            pic = option.get("pic")
                            option_name = option.get("name", "")

                            # 拼接 CDN 前缀
                            if pic and not pic.startswith(("http://", "https://")):
                                pic = cdn_prefix + pic
                                option["pic"] = pic

                            if pic and option_name:
                                markdown_lines.append(f"- {option_name} [查看图片]({pic})")
                            elif option_name:
                                markdown_lines.append(f"- {option_name}")

                    if markdown_lines:
                        parsed["clarification_markdown"] = "\n".join(markdown_lines)
            print(json.dumps(parsed, ensure_ascii=False, indent=2))
            return 0
    except Exception as exc:
        print("请求失败: {0}".format(format_request_error(exc)), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
