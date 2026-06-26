#!/usr/bin/env python3
"""
ultra-memory: PDF 文本提取 (Multimodal Phase 5)
从 PDF 文件中提取文本内容，写入 session 的 multimodal/ 目录，
并触发事实提取。

依赖: pdfminer.six
安装: pip install pdfminer.six
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

CHUNK_SIZE = 500  # 每块字符数


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[tuple[int, str]]:
    """将文本分割为段落块，返回 [(chunk_index, text), ...]"""
    paragraphs = text.split("\n\n")
    chunks = []
    current = []
    current_len = 0
    idx = 0

    for para in paragraphs:
        para_len = len(para)
        if current_len + para_len > chunk_size and current:
            chunks.append((idx, "\n".join(current).strip()))
            idx += 1
            current = []
            current_len = 0
        current.append(para)
        current_len += para_len

    if current:
        chunks.append((idx, "\n".join(current).strip()))

    return chunks


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    使用 pdfminer.six 提取 PDF 文本。
    返回原始文本（保留布局）。
    """
    try:
        from pdfminer.high_level import extract_text
        from pdfminer.layout import LAParams
        text = extract_text(pdf_path, laparams=LAParams())
        return text
    except ImportError:
        print("[ultra-memory] ⚠️  pdfminer.six 未安装: pip install pdfminer.six")
        return ""
    except Exception as e:
        print(f"[ultra-memory] ⚠️  PDF 提取失败: {e}")
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
        f.write(f"# Extracted at: {_now_iso()}\n")
        f.write(f"# Chars: {len(text)}\n")
        f.write("---\n")
        f.write(text)

    return output_file


def trigger_fact_extraction(session_id: str, text_chunk: str, media_id: str):
    """触发 extract_facts.py 从文本块中提取事实"""
    try:
        scripts_dir = Path(__file__).parent.parent
        python = sys.executable

        import subprocess
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # 将文本通过 stdin 传递（避免命令行转义问题）
        proc = subprocess.Popen(
            [python, str(scripts_dir / "extract_facts.py"),
             "--session", session_id, "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            startupinfo=startupinfo,
        )
        # 文本注入到 fact extraction 流程
        # 注意：当前实现将文本保存到文件，fact extraction 从文件读取
    except Exception:
        pass


def process_pdf(session_id: str, pdf_path: str) -> dict:
    """
    处理单个 PDF 文件。
    返回处理结果摘要。
    """
    if not Path(pdf_path).exists():
        print(f"[ultra-memory] ⚠️  PDF 文件不存在: {pdf_path}")
        return {"success": False, "error": "file not found"}

    # 提取文本
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        return {"success": False, "error": "no text extracted"}

    # 生成 media_id
    media_id = f"media_{hashlib.sha1(pdf_path.encode()).hexdigest()[:12]}"

    # 保存文本
    output_file = save_extracted_text(session_id, pdf_path, text, media_id)

    # 分块
    chunks = _chunk_text(text)
    char_count = len(text)

    print(f"[ultra-memory] ✅ PDF 提取完成: {pdf_path}")
    print(f"  文件: {output_file.name}")
    print(f"  字符数: {char_count}")
    print(f"  文本块: {len(chunks)} 块")

    return {
        "success": True,
        "media_id": media_id,
        "session_id": session_id,
        "source_path": pdf_path,
        "output_file": str(output_file),
        "char_count": char_count,
        "chunk_count": len(chunks),
        "processed_at": _now_iso(),
    }


# ── CLI ─────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从 PDF 文件提取文本")
    parser.add_argument("--path", required=True, help="PDF 文件路径")
    parser.add_argument("--session", required=True, help="会话 ID")
    args = parser.parse_args()

    result = process_pdf(args.session, args.path)
    if result["success"]:
        sys.exit(0)
    else:
        print(f"[ultra-memory] ❌ PDF 处理失败: {result.get('error')}")
        sys.exit(1)
