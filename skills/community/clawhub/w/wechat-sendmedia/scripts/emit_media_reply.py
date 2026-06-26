#!/usr/bin/env python3
import argparse
import json
import mimetypes
from pathlib import Path
from urllib.parse import quote

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}


def to_file_url(path: Path) -> str:
    return "file://" + quote(str(path))


def guess_media_type(path: Path) -> str:
    if path.suffix.lower() in IMAGE_EXTS:
        return "image"
    mime, _ = mimetypes.guess_type(path.name)
    if mime and mime.startswith("image/"):
        return "image"
    return "file"


def render_reply_text(path: Path, recipient: str, media_type: str, caption: str = "") -> str:
    label = "图片" if media_type == "image" else "文件"
    lines = [
        "发送成功",
        f"- 类型：{label}",
        f"- 路径：{path}",
        f"- 接收人：{recipient}",
    ]
    if caption.strip():
        lines.append(f"- 备注：{caption.strip()}")
    lines.extend(["", f"MEDIA:{to_file_url(path)}"])
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file_path")
    ap.add_argument("--recipient", default="当前会话")
    ap.add_argument("--text", default="")
    ap.add_argument("--json-envelope", action="store_true", help="also emit legacy json envelope fields for debugging only")
    args = ap.parse_args()

    path = Path(args.file_path).expanduser().resolve()
    exists = path.exists()
    result = {
        "ok": exists,
        "file_path": str(path),
        "exists": exists,
        "recipient": args.recipient,
    }
    if not exists:
        result.update({
            "error": "file_not_found",
            "message": f"file not found: {path}",
        })
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    media_type = guess_media_type(path)
    reply_text = render_reply_text(path, args.recipient, media_type, args.text)
    result.update({
        "mediaType": media_type,
        "fileName": path.name,
        "mediaUrl": to_file_url(path),
        "reply_text": reply_text,
        "size": path.stat().st_size,
    })
    if args.json_envelope:
        result["legacy_json_envelope"] = {
            "text": "这是你要的图片" if media_type == "image" else "这是你要的文件",
            "mediaUrl": to_file_url(path),
            "mediaType": media_type,
            "fileName": path.name,
            "recipient": args.recipient,
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
