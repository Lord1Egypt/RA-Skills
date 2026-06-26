#!/usr/bin/env python3
"""
ultra-memory: 视频转录 (Multimodal Phase 5)
从视频文件中提取音频并转录为文字，写入 session 的 multimodal/ 目录。

依赖: whisper (OpenAI 本地转录，无需 API)
安装: pip install openai-whisper
      或: pip install whisper

注意: whisper 模型较大（base≈1.5GB, small≈3GB, medium≈5GB, large≈10GB）
首次运行会自动下载模型。建议从 base 开始测试。
"""

import os
import sys
import json
import argparse
import hashlib
import subprocess
import tempfile
import shutil
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))

# whisper 模型大小映射
MODEL_SIZES = ["tiny", "base", "small", "medium", "large"]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def transcribe_video(video_path: str, model_size: str = "base") -> str:
    """
    使用 Whisper 本地转录视频。
    自动检测语言。
    """
    try:
        import whisper
    except ImportError:
        print("[ultra-memory] ⚠️  whisper 未安装: pip install openai-whisper")
        print("[ultra-memory] ⚠️  首次运行会自动下载模型（约 1.5GB for base）")
        return ""

    if model_size not in MODEL_SIZES:
        model_size = "base"

    try:
        print(f"[ultra-memory] 加载 Whisper {model_size} 模型...")
        model = whisper.load_model(model_size)
        print(f"[ultra-memory] 开始转录: {video_path}")
        result = model.transcribe(video_path, language=None, verbose=False)
        return result.get("text", "").strip()
    except Exception as e:
        print(f"[ultra-memory] ⚠️  转录失败: {e}")
        return ""


def save_extracted_text(
    session_id: str,
    media_path: str,
    text: str,
    media_id: str,
    model_size: str,
) -> Path:
    """保存转录文本到 multimodal 目录"""
    session_dir = ULTRA_MEMORY_HOME / "sessions" / session_id
    multimodal_dir = session_dir / "multimodal"
    multimodal_dir.mkdir(parents=True, exist_ok=True)

    file_name = Path(media_path).name
    output_file = multimodal_dir / f"{file_name}.transcript.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Transcribed from: {media_path}\n")
        f.write(f"# Media ID: {media_id}\n")
        f.write(f"# Type: video (Whisper {model_size})\n")
        f.write(f"# Transcribed at: {_now_iso()}\n")
        f.write(f"# Chars: {len(text)}\n")
        f.write("---\n")
        f.write(text)

    return output_file


def process_video(
    session_id: str,
    video_path: str,
    model_size: str = "base",
) -> dict:
    """
    处理单个视频文件。
    返回处理结果摘要。
    """
    if not Path(video_path).exists():
        print(f"[ultra-memory] ⚠️  视频文件不存在: {video_path}")
        return {"success": False, "error": "file not found"}

    # 转录
    text = transcribe_video(video_path, model_size)
    if not text.strip():
        return {"success": False, "error": "transcription failed"}

    # 生成 media_id
    media_id = f"media_{hashlib.sha1(video_path.encode()).hexdigest()[:12]}"

    # 保存文本
    output_file = save_extracted_text(
        session_id, video_path, text, media_id, model_size
    )

    char_count = len(text)

    print(f"[ultra-memory] ✅ 视频转录完成: {video_path}")
    print(f"  文件: {output_file.name}")
    print(f"  字符数: {char_count}")

    return {
        "success": True,
        "media_id": media_id,
        "session_id": session_id,
        "source_path": video_path,
        "output_file": str(output_file),
        "char_count": char_count,
        "model_size": model_size,
        "processed_at": _now_iso(),
    }


# ── CLI ─────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从视频提取文字转录")
    parser.add_argument("--path", required=True, help="视频文件路径")
    parser.add_argument("--session", required=True, help="会话 ID")
    parser.add_argument(
        "--model",
        default="base",
        choices=MODEL_SIZES,
        help="Whisper 模型大小 (默认: base)",
    )
    args = parser.parse_args()

    result = process_video(args.session, args.path, args.model)
    if result["success"]:
        sys.exit(0)
    else:
        print(f"[ultra-memory] ❌ 视频处理失败: {result.get('error')}")
        sys.exit(1)
