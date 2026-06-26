#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
视频知识抽取器统一入口。

能力：
- 自动识别 URL / 本地文件 / 本地文件夹 / 批量列表
- 下载音频或直接读取本地媒体文件
- 调用 Whisper 转写
- 调用 OpenAI 兼容 LLM 做后处理
- 固化导出的 Markdown 结构
- 输出批处理报告
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, List, Optional, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT_DIR / "output_templates"

MEDIA_EXTENSIONS = {
    ".aac",
    ".avi",
    ".flac",
    ".m4a",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp3",
    ".mp4",
    ".ogg",
    ".opus",
    ".ts",
    ".wav",
    ".webm",
}

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "").strip()
LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()
LLM_MODEL = os.getenv("LLM_MODEL", "").strip()
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "120"))
LLM_MAX_INPUT_CHARS = int(os.getenv("LLM_MAX_INPUT_CHARS", "45000"))


@dataclass
class MediaItem:
    raw: str
    kind: str  # url / file / folder
    source_root: Optional[str] = None
    source_path: Optional[str] = None
    output_dir: Optional[str] = None
    transcript_dir: Optional[str] = None
    audio_path: Optional[str] = None
    summary_md: Optional[str] = None
    notes_md: Optional[str] = None
    chapters_md: Optional[str] = None
    knowledge_json: Optional[str] = None
    llm_used: bool = False
    llm_model: Optional[str] = None
    llm_error: Optional[str] = None
    status: str = "pending"
    error: Optional[str] = None


@dataclass
class KnowledgePack:
    title: str
    source: str
    kind: str
    duration: str
    language: str
    summary: str
    key_points: List[str]
    notes: List[str]
    chapters: List[dict[str, str]]
    tags: List[str]
    action_items: List[str]
    questions: List[str]
    llm_used: bool = False
    llm_model: Optional[str] = None
    llm_truncated: bool = False
    transcript_chars: int = 0
    llm_error: Optional[str] = None


@dataclass
class ChunkSummary:
    index: int
    start_time: str
    end_time: str
    title: str
    summary: str
    key_points: List[str]
    notes: List[str]
    action_items: List[str]
    questions: List[str]
    raw_chars: int = 0


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def slugify(text: str, max_len: int = 80) -> str:
    text = text.strip()
    text = re.sub(r'[<>:"/\\\\|?*]+', "_", text)
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"_+", "_", text)
    text = text.strip("._ ")
    return (text or "item")[:max_len]


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def truncate_text(text: str, max_len: int) -> str:
    text = clean_text(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def format_seconds(seconds: float) -> str:
    total = max(0, int(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_media_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in MEDIA_EXTENSIONS


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_command(cmd: Sequence[str]) -> None:
    print("执行命令：", " ".join(cmd))
    subprocess.run(list(cmd), check=True)


def collect_media_files(folder: Path) -> List[Path]:
    return [path for path in sorted(folder.rglob("*")) if is_media_file(path)]


def read_list_file(path: Path) -> List[str]:
    items: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        items.append(line)
    return items


def detect_items(inputs: Iterable[str], list_file: Optional[Path]) -> List[MediaItem]:
    raw_items = list(inputs)
    if list_file:
        raw_items.extend(read_list_file(list_file))

    detected: List[MediaItem] = []
    for raw in raw_items:
        raw = raw.strip()
        if not raw:
            continue

        if is_url(raw):
            detected.append(MediaItem(raw=raw, kind="url"))
            continue

        path = Path(raw).expanduser()
        if not path.exists():
            print(f"跳过无法识别的输入：{raw}")
            continue

        if path.is_dir():
            for media_file in collect_media_files(path):
                detected.append(
                    MediaItem(
                        raw=str(media_file),
                        kind="folder",
                        source_root=str(path),
                        source_path=str(media_file),
                    )
                )
            continue

        if is_media_file(path):
            detected.append(MediaItem(raw=str(path), kind="file", source_path=str(path)))
            continue

        print(f"跳过不支持的本地文件：{path}")

    return detected


def source_label(item: MediaItem) -> str:
    if item.source_path:
        return Path(item.source_path).stem
    if is_url(item.raw):
        parsed = urlparse(item.raw)
        stem = Path(parsed.path).stem
        if stem:
            return stem
        return parsed.netloc
    return Path(item.raw).stem or "item"


def resolve_output_dir(output_root: Path, item: MediaItem) -> Path:
    date_dir = datetime.now().strftime("%Y%m%d")
    time_dir = now_stamp()
    return output_root / item.kind / date_dir / slugify(source_label(item)) / time_dir


def download_audio(url: str, output_dir: Path) -> Path:
    ensure_dir(output_dir)
    template = str(output_dir / "downloaded_audio.%(ext)s")
    cmd = [
        "yt-dlp",
        "--force-ipv4",
        "--socket-timeout",
        "60",
        "--retries",
        "5",
        "--fragment-retries",
        "5",
        "-f",
        "bestaudio",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "0",
        "--no-playlist",
        "-o",
        template,
        url,
    ]
    run_command(cmd)

    expected = output_dir / "downloaded_audio.mp3"
    if expected.exists():
        return expected

    candidates = sorted(output_dir.glob("downloaded_audio.*"))
    if not candidates:
        raise FileNotFoundError("未找到下载后的音频文件")
    return candidates[0]


def copy_local_media(source: Path, output_dir: Path) -> Path:
    ensure_dir(output_dir)
    target = output_dir / f"source{source.suffix.lower()}"
    shutil.copy2(source, target)
    return target


def transcribe_media(input_file: Path, output_dir: Path, model: str, language: Optional[str]) -> None:
    ensure_dir(output_dir)
    cmd = [
        "whisper",
        str(input_file),
        "--model",
        model,
        "--output_format",
        "all",
        "--output_dir",
        str(output_dir),
    ]
    if language:
        cmd.extend(["--language", language])
    run_command(cmd)


def load_whisper_artifacts(transcript_dir: Path) -> tuple[str, Optional[dict[str, Any]]]:
    txt_path = next(iter(sorted(transcript_dir.glob("*.txt"))), None)
    json_path = next(iter(sorted(transcript_dir.glob("*.json"))), None)

    transcript_text = ""
    if txt_path and txt_path.exists():
        transcript_text = txt_path.read_text(encoding="utf-8", errors="ignore")

    whisper_json: Optional[dict[str, Any]] = None
    if json_path and json_path.exists():
        try:
            whisper_json = json.loads(json_path.read_text(encoding="utf-8", errors="ignore"))
        except json.JSONDecodeError:
            whisper_json = None

    if not transcript_text and whisper_json:
        segments = whisper_json.get("segments", [])
        transcript_text = "\n".join(
            clean_text(str(seg.get("text", ""))) for seg in segments if clean_text(str(seg.get("text", "")))
        )

    return transcript_text, whisper_json


def extract_whisper_segments(whisper_json: Optional[dict[str, Any]]) -> List[dict[str, Any]]:
    if not whisper_json:
        return []
    segments = whisper_json.get("segments", [])
    return [seg for seg in segments if clean_text(str(seg.get("text", "")))]


def split_segments_into_chunks(
    whisper_json: Optional[dict[str, Any]],
    max_chars: int = 12000,
) -> List[dict[str, Any]]:
    segments = extract_whisper_segments(whisper_json)
    if not segments:
        return []

    chunks: List[List[dict[str, Any]]] = []
    current: List[dict[str, Any]] = []
    current_chars = 0

    for seg in segments:
        text = clean_text(str(seg.get("text", "")))
        if not text:
            continue

        seg_chars = len(text)
        if current and current_chars + seg_chars > max_chars:
            chunks.append(current)
            current = []
            current_chars = 0

        current.append(seg)
        current_chars += seg_chars

    if current:
        chunks.append(current)

    normalized: List[dict[str, Any]] = []
    for index, chunk_segments in enumerate(chunks, start=1):
        start = format_seconds(float(chunk_segments[0].get("start", 0.0)))
        end = format_seconds(float(chunk_segments[-1].get("end", chunk_segments[-1].get("start", 0.0))))
        lines = []
        for seg in chunk_segments:
            seg_start = format_seconds(float(seg.get("start", 0.0)))
            text = clean_text(str(seg.get("text", "")))
            if text:
                lines.append(f"{seg_start} | {text}")
        normalized.append(
            {
                "index": index,
                "start_time": start,
                "end_time": end,
                "text": "\n".join(lines),
                "chars": sum(len(clean_text(str(seg.get("text", "")))) for seg in chunk_segments),
            }
        )

    return normalized


def normalize_string_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [truncate_text(str(item), 240) for item in value if clean_text(str(item))]
    if isinstance(value, str):
        items = [line.strip("-• \t") for line in value.splitlines()]
        return [truncate_text(item, 240) for item in items if clean_text(item)]
    return []


def normalize_chapter_list(value: Any) -> List[dict[str, str]]:
    chapters: List[dict[str, str]] = []
    if isinstance(value, list):
        for item in value:
            if not isinstance(item, dict):
                continue
            chapters.append(
                {
                    "time": clean_text(str(item.get("time", "00:00:00"))) or "00:00:00",
                    "title": truncate_text(str(item.get("title", "章节")), 80),
                    "summary": truncate_text(str(item.get("summary", "")), 240),
                }
            )
    return chapters


def chunk_summary_preview(chunk: dict[str, Any]) -> str:
    text = clean_text(str(chunk.get("text", "")))
    return truncate_text(text, 240)


def build_chunk_fallback_summary(
    item: MediaItem,
    chunk: dict[str, Any],
    language: str,
) -> ChunkSummary:
    text = str(chunk.get("text", ""))
    paragraphs = split_paragraphs(text)
    summary = paragraphs[0] if paragraphs else truncate_text(text, 500)
    key_points = paragraphs[1:4] if len(paragraphs) > 1 else []
    notes = paragraphs[:6] if paragraphs else [truncate_text(text, 800)]
    action_items = build_simple_action_items(paragraphs)
    questions = build_simple_questions(paragraphs)
    if not key_points:
        key_points = [truncate_text(summary, 160)] if summary else []

    title = truncate_text(summary or f"分块 {chunk.get('index', 1)}", 48)
    return ChunkSummary(
        index=int(chunk.get("index", 1)),
        start_time=str(chunk.get("start_time", "00:00:00")),
        end_time=str(chunk.get("end_time", "00:00:00")),
        title=title,
        summary=truncate_text(summary, 800),
        key_points=[truncate_text(point, 160) for point in key_points],
        notes=[truncate_text(note, 240) for note in notes],
        action_items=[truncate_text(item_text, 160) for item_text in action_items],
        questions=[truncate_text(question, 160) for question in questions],
        raw_chars=int(chunk.get("chars", len(text))),
    )


def chunk_summary_to_prompt(chunk_summary: ChunkSummary) -> str:
    return (
        f"[{chunk_summary.start_time}-{chunk_summary.end_time}] {chunk_summary.title}\n"
        f"{chunk_summary.summary}\n"
        f"要点：{'; '.join(chunk_summary.key_points) if chunk_summary.key_points else '无'}"
    )


def whisper_segments_preview(whisper_json: Optional[dict[str, Any]], limit: int = 80) -> str:
    if not whisper_json:
        return ""
    segments = whisper_json.get("segments", [])
    lines: List[str] = []
    for idx, seg in enumerate(segments):
        if idx >= limit:
            lines.append("...（已截断）")
            break
        start = format_seconds(float(seg.get("start", 0.0)))
        text = clean_text(str(seg.get("text", "")))
        if text:
            lines.append(f"{start} | {text}")
    return "\n".join(lines)


def estimate_duration(whisper_json: Optional[dict[str, Any]]) -> str:
    if not whisper_json:
        return "未知"
    segments = whisper_json.get("segments", [])
    if not segments:
        return "未知"
    last_end = segments[-1].get("end")
    try:
        return format_seconds(float(last_end))
    except (TypeError, ValueError):
        return "未知"


def split_paragraphs(text: str) -> List[str]:
    paragraphs = [clean_text(part) for part in re.split(r"\n{2,}|\r\n{2,}", text or "")]
    return [part for part in paragraphs if part]


def derive_tags(item: MediaItem, language: str, whisper_json: Optional[dict[str, Any]]) -> List[str]:
    tags = ["视频知识", "自动整理"]
    if item.kind == "url":
        host = urlparse(item.raw).netloc.lower()
        if "youtube" in host:
            tags.append("YouTube")
        elif "bilibili" in host:
            tags.append("Bilibili")
        elif host:
            tags.append(host)
    if item.kind in {"file", "folder"}:
        tags.append("本地文件")
    if language:
        tags.append(language)
    if whisper_json and whisper_json.get("language"):
        tags.append(str(whisper_json["language"]))
    return list(dict.fromkeys(tag for tag in tags if tag))


def build_fallback_chapters(whisper_json: Optional[dict[str, Any]]) -> List[dict[str, str]]:
    if not whisper_json:
        return [{"time": "00:00:00", "title": "全文", "summary": "未获取到带时间戳的分段信息"}]

    segments = whisper_json.get("segments", [])
    if not segments:
        return [{"time": "00:00:00", "title": "全文", "summary": "未获取到分段信息"}]

    bucket_size = 300
    grouped: List[dict[str, Any]] = []
    current_bucket: Optional[int] = None

    for seg in segments:
        try:
            start = float(seg.get("start", 0.0))
        except (TypeError, ValueError):
            start = 0.0
        bucket = int(start // bucket_size)
        text = clean_text(str(seg.get("text", "")))
        if not text:
            continue

        if current_bucket != bucket:
            grouped.append({"bucket": bucket, "start": start, "texts": [text]})
            current_bucket = bucket
        else:
            grouped[-1]["texts"].append(text)

    chapters: List[dict[str, str]] = []
    for group in grouped:
        first_text = group["texts"][0]
        merged_text = " ".join(group["texts"])
        chapters.append(
            {
                "time": format_seconds(group["bucket"] * bucket_size),
                "title": truncate_text(first_text, 18) or "章节",
                "summary": truncate_text(merged_text, 120),
            }
        )

    if not chapters:
        chapters.append({"time": "00:00:00", "title": "全文", "summary": "未能从分段中提取章节"})

    return chapters


def build_simple_action_items(paragraphs: List[str]) -> List[str]:
    keywords = ("建议", "需要", "应该", "可以", "务必", "必须", "要", "记得")
    actions = [p for p in paragraphs if any(key in p for key in keywords)]
    return actions[:5]


def build_simple_questions(paragraphs: List[str]) -> List[str]:
    questions: List[str] = []
    for paragraph in paragraphs:
        if "?" in paragraph or "？" in paragraph or re.search(r"(为什么|如何|怎么|什么|哪个|哪些)", paragraph):
            questions.append(paragraph)
    return questions[:5]


def build_fallback_pack(item: MediaItem, transcript_text: str, whisper_json: Optional[dict[str, Any]], language: str) -> KnowledgePack:
    paragraphs = split_paragraphs(transcript_text)
    summary = paragraphs[0] if paragraphs else truncate_text(transcript_text, 500)
    key_points = paragraphs[1:6] if len(paragraphs) > 1 else []
    notes = paragraphs[:10] if paragraphs else [truncate_text(transcript_text, 1000)]
    action_items = build_simple_action_items(paragraphs)
    questions = build_simple_questions(paragraphs)
    chapters = build_fallback_chapters(whisper_json)
    duration = estimate_duration(whisper_json)
    tags = derive_tags(item, language, whisper_json)

    if not key_points:
        key_points = [truncate_text(summary, 160)] if summary else []

    return KnowledgePack(
        title=source_label(item),
        source=item.raw,
        kind=item.kind,
        duration=duration,
        language=language or "自动识别",
        summary=truncate_text(summary, 1200),
        key_points=[truncate_text(point, 160) for point in key_points],
        notes=[truncate_text(note, 240) for note in notes],
        chapters=chapters,
        tags=tags,
        action_items=[truncate_text(item_text, 160) for item_text in action_items],
        questions=[truncate_text(question, 160) for question in questions],
    )


def dedupe_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    deduped: List[str] = []
    for item in items:
        value = clean_text(item)
        if not value or value in seen:
            continue
        seen.add(value)
        deduped.append(item)
    return deduped


def build_chunk_messages(
    item: MediaItem,
    chunk: dict[str, Any],
    language: str,
    total_chunks: int,
) -> list[dict[str, str]]:
    system = (
        "你是视频知识抽取器，正在处理长视频的一个分块。"
        "只输出 JSON，不要输出解释、Markdown 或代码块。"
        "JSON 必须包含 title, summary, key_points, notes, action_items, questions。"
        "其中 key_points, notes, action_items, questions 必须是字符串数组。"
        "title 要短，summary 要概括本分块的核心内容。"
    )
    user = f"""
来源：{item.raw}
类型：{item.kind}
语言：{language}
分块：{chunk['index']}/{total_chunks}
时间范围：{chunk['start_time']} - {chunk['end_time']}

请只根据下面这个分块内容进行总结，避免把其他分块的内容混进来。

【分块转写】
{chunk['text']}
"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user.strip()},
    ]


def build_chunk_summary_with_llm(
    item: MediaItem,
    chunk: dict[str, Any],
    language: str,
    total_chunks: int,
) -> ChunkSummary:
    messages = build_chunk_messages(item, chunk, language, total_chunks)
    content = call_openai_compatible_llm(messages)
    payload = extract_json_payload(content)

    title = truncate_text(str(payload.get("title") or f"分块 {chunk['index']}"), 48)
    summary = truncate_text(str(payload.get("summary") or ""), 800)
    key_points = normalize_string_list(payload.get("key_points"))
    notes = normalize_string_list(payload.get("notes"))
    action_items = normalize_string_list(payload.get("action_items"))
    questions = normalize_string_list(payload.get("questions"))

    if not key_points:
        key_points = [truncate_text(summary, 160)] if summary else []
    if not notes:
        notes = [truncate_text(summary, 240)] if summary else []

    return ChunkSummary(
        index=int(chunk["index"]),
        start_time=str(chunk["start_time"]),
        end_time=str(chunk["end_time"]),
        title=title,
        summary=summary or title,
        key_points=key_points,
        notes=notes,
        action_items=action_items,
        questions=questions,
        raw_chars=int(chunk.get("chars", 0)),
    )


def build_chunk_brief_text(chunk_summaries: List[ChunkSummary]) -> str:
    lines: List[str] = []
    for chunk in chunk_summaries:
        lines.append(
            "\n".join(
                [
                    f"[{chunk.start_time}-{chunk.end_time}] {chunk.title}",
                    f"摘要：{chunk.summary}",
                    f"要点：{'; '.join(chunk.key_points) if chunk.key_points else '无'}",
                ]
            )
        )
    return "\n\n".join(lines)


def build_chunked_final_messages(
    item: MediaItem,
    chunk_summaries: List[ChunkSummary],
    language: str,
    whisper_json: Optional[dict[str, Any]],
) -> list[dict[str, str]]:
    system = (
        "你是视频知识抽取器。"
        "你将收到长视频各分块的摘要，请把它们整理成最终知识笔记。"
        "只输出 JSON，不要输出解释、Markdown 或代码块。"
        "JSON 必须包含 title, summary, key_points, notes, chapters, tags, action_items, questions。"
        "其中 chapters 是数组，元素格式为 {time, title, summary}。"
    )
    user = f"""
来源：{item.raw}
类型：{item.kind}
语言：{language}
总分块数：{len(chunk_summaries)}
总时长：{estimate_duration(whisper_json)}

请综合下面的分块摘要，输出最终的整体知识结构。

【分块摘要】
{build_chunk_brief_text(chunk_summaries)}
"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user.strip()},
    ]


def build_chunk_fallback_summary(
    item: MediaItem,
    chunk: dict[str, Any],
    language: str,
) -> ChunkSummary:
    text = str(chunk.get("text", ""))
    paragraphs = split_paragraphs(text)
    summary = paragraphs[0] if paragraphs else truncate_text(text, 500)
    key_points = paragraphs[1:4] if len(paragraphs) > 1 else []
    notes = paragraphs[:6] if paragraphs else [truncate_text(text, 800)]
    action_items = build_simple_action_items(paragraphs)
    questions = build_simple_questions(paragraphs)
    if not key_points:
        key_points = [truncate_text(summary, 160)] if summary else []

    title = truncate_text(summary or f"分块 {chunk.get('index', 1)}", 48)
    return ChunkSummary(
        index=int(chunk.get("index", 1)),
        start_time=str(chunk.get("start_time", "00:00:00")),
        end_time=str(chunk.get("end_time", "00:00:00")),
        title=title,
        summary=truncate_text(summary, 800),
        key_points=[truncate_text(point, 160) for point in key_points],
        notes=[truncate_text(note, 240) for note in notes],
        action_items=[truncate_text(item_text, 160) for item_text in action_items],
        questions=[truncate_text(question, 160) for question in questions],
        raw_chars=int(chunk.get("chars", len(text))),
    )


def build_chunked_llm_pack(
    item: MediaItem,
    transcript_text: str,
    whisper_json: Optional[dict[str, Any]],
    language: str,
) -> KnowledgePack:
    chunks = split_segments_into_chunks(whisper_json, max_chars=min(LLM_MAX_INPUT_CHARS, 12000))
    if not chunks:
        return build_llm_pack(item, transcript_text, whisper_json, language)

    chunk_summaries: List[ChunkSummary] = []
    for chunk in chunks:
        try:
            chunk_summaries.append(build_chunk_summary_with_llm(item, chunk, language, len(chunks)))
        except Exception:
            chunk_summaries.append(build_chunk_fallback_summary(item, chunk, language))

    try:
        messages = build_chunked_final_messages(item, chunk_summaries, language, whisper_json)
        content = call_openai_compatible_llm(messages)
        payload = extract_json_payload(content)
    except Exception:
        payload = {}

    title = clean_text(str(payload.get("title") or source_label(item))) or source_label(item)
    summary = truncate_text(str(payload.get("summary") or ""), 1600)
    key_points = normalize_string_list(payload.get("key_points"))
    notes = normalize_string_list(payload.get("notes"))
    chapters = normalize_chapter_list(payload.get("chapters"))
    tags = normalize_string_list(payload.get("tags"))
    action_items = normalize_string_list(payload.get("action_items"))
    questions = normalize_string_list(payload.get("questions"))

    if not chapters:
        chapters = [
            {
                "time": chunk.start_time,
                "title": chunk.title,
                "summary": chunk.summary,
            }
            for chunk in chunk_summaries
        ]
    if not summary:
        summary = "；".join(chunk.summary for chunk in chunk_summaries[:3])
    if not key_points:
        key_points = []
        for chunk in chunk_summaries:
            key_points.extend(chunk.key_points[:2])
        key_points = dedupe_preserve_order([truncate_text(point, 160) for point in key_points])[:10]
    if not notes:
        notes = []
        for chunk in chunk_summaries:
            notes.extend(chunk.notes[:3])
        notes = dedupe_preserve_order([truncate_text(note, 240) for note in notes])[:12]
    if not action_items:
        action_items = []
        for chunk in chunk_summaries:
            action_items.extend(chunk.action_items[:2])
        action_items = dedupe_preserve_order([truncate_text(item_text, 160) for item_text in action_items])[:10]
    if not questions:
        questions = []
        for chunk in chunk_summaries:
            questions.extend(chunk.questions[:2])
        questions = dedupe_preserve_order([truncate_text(question, 160) for question in questions])[:10]
    if not tags:
        tags = derive_tags(item, language, whisper_json)

    return KnowledgePack(
        title=title,
        source=item.raw,
        kind=item.kind,
        duration=estimate_duration(whisper_json),
        language=language or "自动识别",
        summary=summary or truncate_text(build_chunk_brief_text(chunk_summaries), 1200),
        key_points=key_points,
        notes=notes,
        chapters=chapters,
        tags=tags,
        action_items=action_items,
        questions=questions,
        llm_used=True,
        llm_model=LLM_MODEL,
        llm_truncated=True,
        transcript_chars=len(transcript_text),
    )


def llm_is_configured() -> bool:
    return bool(LLM_BASE_URL and LLM_API_KEY and LLM_MODEL)


def normalize_llm_endpoint(base_url: str) -> str:
    base_url = base_url.rstrip("/")
    if base_url.endswith("/chat/completions"):
        return base_url
    return f"{base_url}/chat/completions"


def extract_json_payload(text: str) -> dict[str, Any]:
    text = text.strip()
    if not text:
        raise ValueError("LLM 返回为空")

    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        data = json.loads(fenced.group(1))
        if isinstance(data, dict):
            return data

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        data = json.loads(text[start : end + 1])
        if isinstance(data, dict):
            return data

    raise ValueError("无法从 LLM 输出中解析 JSON")


def call_openai_compatible_llm(messages: list[dict[str, str]]) -> str:
    url = normalize_llm_endpoint(LLM_BASE_URL)
    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": 0.2,
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLM_API_KEY}",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=LLM_TIMEOUT) as response:
            response_text = response.read().decode("utf-8", errors="ignore")
    except HTTPError as exc:
        raise RuntimeError(f"LLM 请求失败：{exc.code} {exc.reason}") from exc
    except URLError as exc:
        raise RuntimeError(f"LLM 连接失败：{exc.reason}") from exc

    response_data = json.loads(response_text)
    choices = response_data.get("choices", [])
    if not choices:
        raise RuntimeError("LLM 响应中没有 choices")
    message = choices[0].get("message", {})
    content = message.get("content", "")
    if not content:
        raise RuntimeError("LLM 响应内容为空")
    return str(content)


def build_llm_prompt(
    item: MediaItem,
    transcript_text: str,
    whisper_json: Optional[dict[str, Any]],
    language: str,
) -> tuple[list[dict[str, str]], bool]:
    transcript_text = transcript_text.strip()
    preview = whisper_segments_preview(whisper_json)
    truncated = False

    if len(transcript_text) > LLM_MAX_INPUT_CHARS:
        transcript_text = transcript_text[:LLM_MAX_INPUT_CHARS]
        truncated = True

    system = (
        "你是视频知识抽取器。"
        "你的任务是把视频转写整理成可直接入库的知识笔记。"
        "只输出 JSON，不要输出解释、Markdown 或代码块。"
        "JSON 需要包含这些键："
        "title, summary, key_points, notes, chapters, tags, action_items, questions。"
        "其中 chapters 是数组，元素格式为 {time, title, summary}。"
        "key_points, notes, tags, action_items, questions 都必须是字符串数组。"
        "summary 必须是一段完整摘要。"
    )
    user = f"""
来源：{item.raw}
类型：{item.kind}
语言：{language or '自动识别'}
时长：{estimate_duration(whisper_json)}
本地文件：{item.source_path or ''}

请基于下方转写内容生成知识结构：

【转写正文】
{transcript_text}

【时间戳预览】
{preview}
"""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user.strip()},
    ]
    return messages, truncated


def normalize_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [truncate_text(str(item), 240) for item in value if clean_text(str(item))]
    if isinstance(value, str):
        items = [line.strip("-• \t") for line in value.splitlines()]
        return [truncate_text(item, 240) for item in items if clean_text(item)]
    return []


def normalize_chapters(value: Any) -> List[dict[str, str]]:
    chapters: List[dict[str, str]] = []
    if isinstance(value, list):
        for item in value:
            if not isinstance(item, dict):
                continue
            time = clean_text(str(item.get("time", "00:00:00"))) or "00:00:00"
            title = truncate_text(str(item.get("title", "章节")), 80)
            summary = truncate_text(str(item.get("summary", "")), 240)
            chapters.append({"time": time, "title": title, "summary": summary})
    return chapters


def build_llm_pack(
    item: MediaItem,
    transcript_text: str,
    whisper_json: Optional[dict[str, Any]],
    language: str,
) -> KnowledgePack:
    messages, truncated = build_llm_prompt(item, transcript_text, whisper_json, language)
    content = call_openai_compatible_llm(messages)
    payload = extract_json_payload(content)

    title = clean_text(str(payload.get("title") or source_label(item))) or source_label(item)
    summary = truncate_text(str(payload.get("summary") or ""), 1600)
    key_points = normalize_list(payload.get("key_points"))
    notes = normalize_list(payload.get("notes"))
    chapters = normalize_chapters(payload.get("chapters"))
    tags = normalize_list(payload.get("tags"))
    action_items = normalize_list(payload.get("action_items"))
    questions = normalize_list(payload.get("questions"))

    if not chapters:
        chapters = build_fallback_chapters(whisper_json)
    if not key_points:
        key_points = [truncate_text(summary, 160)] if summary else []
    if not notes:
        notes = split_paragraphs(truncate_text(transcript_text, 4000))[:10]

    return KnowledgePack(
        title=title,
        source=item.raw,
        kind=item.kind,
        duration=estimate_duration(whisper_json),
        language=language or "自动识别",
        summary=summary or truncate_text(transcript_text, 1200),
        key_points=key_points,
        notes=notes,
        chapters=chapters,
        tags=tags or derive_tags(item, language, whisper_json),
        action_items=action_items,
        questions=questions,
        llm_used=True,
        llm_model=LLM_MODEL,
        llm_truncated=truncated,
        transcript_chars=len(transcript_text),
    )


def choose_pack(
    item: MediaItem,
    transcript_text: str,
    whisper_json: Optional[dict[str, Any]],
    language: str,
) -> KnowledgePack:
    if llm_is_configured():
        try:
            if len(transcript_text) > LLM_MAX_INPUT_CHARS:
                return build_chunked_llm_pack(item, transcript_text, whisper_json, language)
            return build_llm_pack(item, transcript_text, whisper_json, language)
        except Exception as exc:  # noqa: BLE001
            fallback = build_fallback_pack(item, transcript_text, whisper_json, language)
            fallback.llm_error = str(exc)
            return fallback
    return build_fallback_pack(item, transcript_text, whisper_json, language)


def load_template(name: str, fallback: str) -> str:
    path = TEMPLATE_DIR / name
    if path.exists():
        return path.read_text(encoding="utf-8")
    return fallback


def bullet_list(items: List[str]) -> str:
    if not items:
        return "- 无"
    return "\n".join(f"- {item}" for item in items)


def render_chapter_table(chapters: List[dict[str, str]]) -> str:
    if not chapters:
        return "| 时间 | 标题 | 说明 |\n|------|------|------|\n| 00:00:00 | 全文 | 无 |"

    lines = ["| 时间 | 标题 | 说明 |", "|------|------|------|"]
    for chapter in chapters:
        time = str(chapter.get("time", "00:00:00")).replace("|", "\\|")
        title = str(chapter.get("title", "")).replace("|", "\\|")
        summary = str(chapter.get("summary", "")).replace("|", "\\|")
        lines.append(f"| {time} | {title} | {summary} |")
    return "\n".join(lines)


def render_tags(tags: List[str]) -> str:
    return " ".join(f"#{slugify(tag, 24)}" for tag in tags) if tags else "无"


def render_template(template: str, values: dict[str, str]) -> str:
    class SafeDict(dict):
        def __missing__(self, key: str) -> str:  # pragma: no cover
            return ""

    return template.format_map(SafeDict(values))


def write_knowledge_outputs(output_dir: Path, item: MediaItem, pack: KnowledgePack) -> None:
    ensure_dir(output_dir)

    templates = {
        "summary": load_template(
            "summary.md",
            """# {title}\n\n- 来源：{source}\n- 类型：{kind}\n- 时长：{duration}\n- 语言：{language}\n\n## 摘要\n{summary}\n\n## 关键要点\n{key_points}\n\n## 标签\n{tags}\n""",
        ),
        "notes": load_template(
            "notes.md",
            """# {title}\n\n- 来源：{source}\n- 类型：{kind}\n- 时长：{duration}\n- 语言：{language}\n\n## 结构化笔记\n{notes}\n\n## 行动项\n{action_items}\n\n## 延伸问题\n{questions}\n\n## 标签\n{tags}\n""",
        ),
        "chapters": load_template(
            "chapters.md",
            """# {title}\n\n- 来源：{source}\n- 类型：{kind}\n- 时长：{duration}\n- 语言：{language}\n\n## 章节列表\n{chapters}\n""",
        ),
    }

    context = {
        "title": pack.title,
        "source": item.raw,
        "kind": item.kind,
        "duration": pack.duration,
        "language": pack.language,
        "summary": pack.summary,
        "key_points": bullet_list(pack.key_points),
        "notes": bullet_list(pack.notes),
        "chapters": render_chapter_table(pack.chapters),
        "tags": render_tags(pack.tags),
        "action_items": bullet_list(pack.action_items),
        "questions": bullet_list(pack.questions),
    }

    summary_path = output_dir / "summary.md"
    notes_path = output_dir / "notes.md"
    chapters_path = output_dir / "chapters.md"
    knowledge_json_path = output_dir / "knowledge.json"

    summary_path.write_text(render_template(templates["summary"], context), encoding="utf-8")
    notes_path.write_text(render_template(templates["notes"], context), encoding="utf-8")
    chapters_path.write_text(render_template(templates["chapters"], context), encoding="utf-8")
    knowledge_json_path.write_text(
        json.dumps(asdict(pack), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    item.summary_md = str(summary_path)
    item.notes_md = str(notes_path)
    item.chapters_md = str(chapters_path)
    item.knowledge_json = str(knowledge_json_path)


def write_manifest(item: MediaItem, manifest_path: Path) -> None:
    manifest_path.write_text(
        json.dumps(asdict(item), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_report(items: List[MediaItem]) -> dict[str, Any]:
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total": len(items),
        "success": sum(1 for item in items if item.status == "done"),
        "failed": sum(1 for item in items if item.status == "failed"),
        "items": [asdict(item) for item in items],
    }


def write_report(report: dict[str, Any], output_root: Path) -> None:
    ensure_dir(output_root)
    (output_root / "batch_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# 批处理报告",
        "",
        f"- 总数：{report['total']}",
        f"- 成功：{report['success']}",
        f"- 失败：{report['failed']}",
        "",
        "| 状态 | 来源 | 输出目录 | LLM | 错误 |",
        "|------|------|----------|-----|------|",
    ]
    for item in report["items"]:
        raw = str(item["raw"]).replace("|", "\\|")
        output_dir = str(item.get("output_dir") or "").replace("|", "\\|")
        llm_state = "是" if item.get("llm_used") else "否"
        error = str(item.get("error") or item.get("llm_error") or "").replace("|", "\\|")
        lines.append(f"| {item['status']} | {raw} | {output_dir} | {llm_state} | {error} |")

    (output_root / "batch_report.md").write_text("\n".join(lines), encoding="utf-8")


def process_item(
    item: MediaItem,
    output_root: Path,
    model: str,
    language: Optional[str],
    keep_audio: bool,
) -> MediaItem:
    output_dir = resolve_output_dir(output_root, item)
    transcript_dir = ensure_dir(output_dir / "transcript")
    audio_dir = ensure_dir(output_dir / "audio")

    item.output_dir = str(output_dir)
    item.transcript_dir = str(transcript_dir)

    try:
        if item.kind == "url":
            audio_path = download_audio(item.raw, audio_dir)
        else:
            source_path = Path(item.source_path or item.raw)
            audio_path = copy_local_media(source_path, audio_dir)

        item.audio_path = str(audio_path)

        transcribe_media(audio_path, transcript_dir, model=model, language=language)

        transcript_text, whisper_json = load_whisper_artifacts(transcript_dir)
        pack = choose_pack(item, transcript_text, whisper_json, language or "自动识别")
        item.llm_used = pack.llm_used
        item.llm_model = pack.llm_model
        item.llm_error = pack.llm_error
        if not pack.llm_used and llm_is_configured() and not item.llm_error:
            item.llm_error = "LLM 后处理失败，已回退到本地规则"

        write_knowledge_outputs(output_dir, item, pack)

        if not keep_audio and audio_path.exists():
            audio_path.unlink()

        item.status = "done"
        write_manifest(item, output_dir / "manifest.json")
        return item

    except Exception as exc:  # noqa: BLE001
        item.status = "failed"
        item.error = str(exc)
        try:
            write_manifest(item, output_dir / "manifest.json")
        except Exception:  # noqa: BLE001
            pass
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="视频知识抽取器统一入口")
    parser.add_argument("inputs", nargs="*", help="视频 URL、本地文件或本地文件夹")
    parser.add_argument("--list-file", type=Path, help="包含多个输入项的文本文件")
    parser.add_argument("--output-root", type=Path, default=Path("outputs"), help="输出根目录")
    parser.add_argument("--model", default="base", help="Whisper 模型名")
    parser.add_argument("--language", default=None, help="指定语言，例如 zh、en")
    parser.add_argument("--keep-audio", action="store_true", help="保留下载/复制后的音频文件")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    items = detect_items(args.inputs, args.list_file)

    if not items:
        print("没有可处理的输入。")
        return 1

    ensure_dir(args.output_root)

    processed: List[MediaItem] = []
    for index, item in enumerate(items, start=1):
        print(f"\n[{index}/{len(items)}] 处理：{item.raw}")
        try:
            processed.append(
                process_item(
                    item=item,
                    output_root=args.output_root,
                    model=args.model,
                    language=args.language,
                    keep_audio=args.keep_audio,
                )
            )
        except Exception as exc:  # noqa: BLE001
            print(f"处理失败：{exc}")
            processed.append(item)

    report = build_report(processed)
    write_report(report, args.output_root)
    print(f"\n批处理完成，报告已输出到：{args.output_root}")
    return 0 if report["failed"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
