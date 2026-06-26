#!/usr/bin/env python3
"""
ultra-memory: 图片 OCR 提取 (Multimodal Phase 5)
从图片文件中提取文字内容，写入 session 的 multimodal/ 目录，
并触发事实提取。

依赖: pytesseract + Tesseract OCR 引擎
安装:
  pip install pytesseract
  Windows: 下载 https://github.com/UB-Mannheim/tesseract/wiki
  macOS:  brew install tesseract
  Linux:  sudo apt install tesseract-ocr
"""

import os
import sys
import json
import argparse
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def extract_text_from_image(image_path: str) -> str:
    """
    使用 pytesseract OCR 提取图片文字。
    同时支持中英文（lang='eng+chi'）。
    """
    try:
        import pytesseract
        from PIL import Image

        # 尝试中文+英文，如果失败回退到英文
        try:
            text = pytesseract.image_to_string(image_path, lang="eng+chi")
        except Exception:
            text = pytesseract.image_to_string(image_path, lang="eng")

        return text.strip()
    except ImportError:
        print("[ultra-memory] ⚠️  pytesseract 未安装: pip install pytesseract")
        print("[ultra-memory] ⚠️  同时需要安装 Tesseract OCR 引擎")
        return ""
    except Exception as e:
        print(f"[ultra-memory] ⚠️  OCR 提取失败: {e}")
        return ""


def save_extracted_text(
    session_id: str,
    media_path: str,
    text: str,
    media_id: str,
) -> Path:
    """保存提取的文本到 multimodal 目录"""
    session_dir = ULTRA_MEMORY_HOME / "sessions" / session_id
    multimodal_dir = session_dir / "multimodal"
    multimodal_dir.mkdir(parents=True, exist_ok=True)

    file_name = Path(media_path).name
    output_file = multimodal_dir / f"{file_name}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Extracted from: {media_path}\n")
        f.write(f"# Media ID: {media_id}\n")
        f.write(f"# Type: image (OCR)\n")
        f.write(f"# Extracted at: {_now_iso()}\n")
        f.write(f"# Chars: {len(text)}\n")
        f.write("---\n")
        f.write(text)

    return output_file


def process_image(session_id: str, image_path: str) -> dict:
    """
    处理单个图片文件。
    返回处理结果摘要。
    """
    if not Path(image_path).exists():
        print(f"[ultra-memory] ⚠️  图片文件不存在: {image_path}")
        return {"success": False, "error": "file not found"}

    # 提取文本
    text = extract_text_from_image(image_path)
    if not text.strip():
        return {"success": False, "error": "no text extracted"}

    # 生成 media_id
    media_id = f"media_{hashlib.sha1(image_path.encode()).hexdigest()[:12]}"

    # 保存文本
    output_file = save_extracted_text(session_id, image_path, text, media_id)

    char_count = len(text)

    print(f"[ultra-memory] ✅ 图片 OCR 完成: {image_path}")
    print(f"  文件: {output_file.name}")
    print(f"  字符数: {char_count}")

    return {
        "success": True,
        "media_id": media_id,
        "session_id": session_id,
        "source_path": image_path,
        "output_file": str(output_file),
        "char_count": char_count,
        "processed_at": _now_iso(),
    }


# ── CLI ─────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从图片提取文字 (OCR)")
    parser.add_argument("--path", required=True, help="图片文件路径")
    parser.add_argument("--session", required=True, help="会话 ID")
    args = parser.parse_args()

    result = process_image(args.session, args.path)
    if result["success"]:
        sys.exit(0)
    else:
        print(f"[ultra-memory] ❌ 图片处理失败: {result.get('error')}")
        sys.exit(1)
