#!/usr/bin/env python3
"""Subtitle-only video knowledge report scaffold.

This entrypoint inspects the input, classifies the source, judges subtitle
accessibility, estimates processing time, creates a work directory, records
metadata, and renders a Markdown report scaffold. It is subtitle-only — it
does NOT perform audio extraction, audio transcription, or real-time playback
capture. Actual subtitle fetching, parsing, and summarization are performed
by the LLM directly.

Usage:
    extract_subtitle.py <source> [--output-dir reports] [--work-dir work]
                       [--duration-minutes N] [--file-size-mb N]
                       [--estimate-only] [--verbose-prompts]
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse


SUBTITLE_EXTENSIONS = {".srt", ".vtt", ".txt", ".md", ".json"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".flv", ".m4v"}

# Query parameter name fragments that may carry authentication material.
# Any case-insensitive substring match causes the value to be redacted
# before the URL is persisted to metadata.json, report file names, or
# rendered report content. The raw URL stays only in memory for the
# actual subtitle extraction step and is never written to disk.
SENSITIVE_QUERY_HINTS = (
    "token",
    "session",
    "sid",
    "auth",
    "password",
    "passwd",
    "pwd",
    "secret",
    "credential",
    "apikey",
    "api_key",
    "accesskey",
    "access_key",
    "signature",
    "ticket",
    "oauth",
    "bearer",
    "cookie",
    "authorization",
)


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def sanitize_url(value: str) -> str:
    """Return a URL with authentication-related query parameters redacted.

    Used before persisting a source URL to metadata.json, report file names,
    or rendered report content. Values of sensitive query keys are replaced
    with the literal ``[REDACTED]`` marker; the rest of the URL is preserved.
    If the input is not a parseable absolute URL, a safe placeholder is
    returned so that raw input (which may itself be a credential) is never
    written to disk.
    """
    parsed = urlparse(value)
    if not parsed.scheme or not parsed.netloc:
        return "[unparseable-source]"
    pairs = parse_qsl(parsed.query, keep_blank_values=True)
    redacted: list[tuple[str, str]] = []
    for key, val in pairs:
        if any(hint in key.lower() for hint in SENSITIVE_QUERY_HINTS):
            redacted.append((key, "[REDACTED]"))
        else:
            redacted.append((key, val))
    new_query = urlencode(redacted)
    return urlunparse(parsed._replace(query=new_query))


def classify_source(value: str) -> str:
    if is_url(value):
        host = urlparse(value).netloc.lower()
        lower = value.lower()
        if "bilibili.com" in host or "b23.tv" in host:
            return "bilibili-url"
        if "zhixueyun.com" in host:
            return "zhixueyun-url"
        if lower.endswith(".m3u8"):
            return "hls-url"
        if any(lower.endswith(ext) for ext in VIDEO_EXTENSIONS | AUDIO_EXTENSIONS):
            return "direct-media-url"
        return "public-web-video-url"

    suffix = Path(value).suffix.lower()
    if suffix in SUBTITLE_EXTENSIONS:
        return "subtitle-or-transcript-file"
    if suffix in AUDIO_EXTENSIONS:
        return "local-audio-file"
    if suffix in VIDEO_EXTENSIONS:
        return "local-video-file"
    return "local-or-unknown-file"


def format_minutes(low: float, high: float) -> str:
    low = max(1, round(low))
    high = max(low, round(high))
    if high < 120:
        return f"{low}-{high} 分钟"
    if low < 60:
        return f"{low} 分钟-{high / 60:.1f} 小时"
    return f"{low / 60:.1f}-{high / 60:.1f} 小时"


def estimate_subtitle_extraction(
    source_kind: str,
    duration_minutes: float | None,
    file_size_mb: float | None,
) -> dict:
    """Return judgment + time estimate. This skill is subtitle-only.

    For sources that cannot expose subtitles directly, judgment is set to
    "not-accessible" and the estimate has no numeric range — the caller
    should hand the user the not-accessible guidance instead.
    """

    risk_factors: list[str] = []
    subtitle_method: str
    judgment: str  # accessible | partially-accessible | not-accessible | depends-on-online-page
    low: float
    high: float

    if source_kind == "subtitle-or-transcript-file":
        judgment = "accessible"
        subtitle_method = "读取本地字幕文件"
        low, high = 1.0, 5.0
    elif source_kind in {"local-audio-file", "local-video-file"}:
        judgment = "not-accessible"
        subtitle_method = "无法处理（媒体文件不含字幕，本技能不做音频转写）"
        risk_factors.append("本地媒体文件无字幕轨")
        low, high = 0.0, 0.0
    elif source_kind == "bilibili-url":
        judgment = "depends-on-online-page"
        subtitle_method = "优先读取页面暴露字幕/官方字幕接口；无字幕则改换字幕文件或换源"
        risk_factors.extend(["页面是否暴露字幕", "网络抓取速度", "平台限速"])
        low, high = estimate_from_duration(duration_minutes, plain_subtitle_only, 2.0, 8.0, 2.0, 8.0)
    elif source_kind == "zhixueyun-url":
        judgment = "depends-on-online-page"
        subtitle_method = "智学云是公开网站，优先尝试读取页面暴露字幕；如需登录，使用 Playwright 浏览器自动化（非 headless 模式）让用户手动登录后读取字幕；无字幕则请用户提供字幕文件"
        risk_factors.extend(["用户登录时间", "页面是否暴露字幕", "网络速度"])
        low, high = estimate_from_duration(duration_minutes, plain_subtitle_only, 3.0, 12.0, 3.0, 12.0)
    elif source_kind == "hls-url":
        judgment = "depends-on-online-page"
        subtitle_method = "检测 HLS 播放列表中合法暴露的字幕轨；无则改换字幕文件"
        risk_factors.extend(["HLS 字幕轨是否暴露", "是否加密或受 DRM 保护"])
        low, high = estimate_from_duration(duration_minutes, plain_subtitle_only, 2.0, 10.0, 2.0, 10.0)
    elif source_kind == "direct-media-url":
        judgment = "not-accessible"
        subtitle_method = "无法处理（直链媒体通常不含可读字幕，本技能不做音频转写）"
        risk_factors.append("直链媒体通常无字幕轨")
        low, high = 0.0, 0.0
    else:  # public-web-video-url or local-or-unknown-file
        judgment = "depends-on-online-page"
        subtitle_method = "优先读取页面暴露字幕/transcript 面板；无则改换字幕文件或换源"
        risk_factors.extend(["未知视频时长", "页面是否暴露字幕", "网络速度"])
        low, high = estimate_from_duration(duration_minutes, plain_subtitle_only, 2.0, 8.0, 2.0, 8.0)

    if duration_minutes is None:
        risk_factors.append("未知视频时长")
    if file_size_mb and file_size_mb > 500:
        risk_factors.append("文件较大（虽然本技能不转码）")
    if judgment == "not-accessible":
        risk_factors = risk_factors or ["字幕不可达"]

    risk_factors = list(dict.fromkeys(risk_factors)) or ["无明显额外风险"]
    return {
        "source_kind": source_kind,
        "subtitle_judgment": judgment,
        "acquisition_method_hint": subtitle_method,
        "estimated_range": "无法估时（字幕不可达）" if judgment == "not-accessible" else format_minutes(low, high),
        "estimated_low_minutes": round(low, 1),
        "estimated_high_minutes": round(high, 1),
        "risk_factors": risk_factors,
        "is_slow": high > 30,
    }


def plain_subtitle_only(
    duration_minutes: float | None,
    multiplier_low: float,
    multiplier_high: float,
    fallback_low: float,
    fallback_high: float,
) -> tuple[float, float]:
    """Stub kept for signature compatibility with estimate_from_duration.

    The skill is subtitle-only, so multipliers are ignored — subtitle
    extraction time is roughly constant per source type, not proportional
    to duration. The duration-based branch is preserved only for future
    extension.
    """
    _ = (multiplier_low, multiplier_high)
    if duration_minutes and duration_minutes > 0:
        # Subtitle extraction is near-constant; fall back to source-type range.
        return float(fallback_low), float(max(fallback_high, fallback_low + 1.0))
    return float(fallback_low), float(fallback_high)


def estimate_from_duration(
    duration_minutes: float | None,
    multiplier_fn,
    multiplier_low: float,
    multiplier_high: float,
    fallback_low: float,
    fallback_high: float,
) -> tuple[float, float]:
    return multiplier_fn(duration_minutes, multiplier_low, multiplier_high, fallback_low, fallback_high)


def slugify(value: str) -> str:
    value = re.sub(r"https?://", "", value)
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value)
    return value.strip("-._")[:80] or "video"


def emit(message: str, enabled: bool) -> None:
    if enabled:
        print(message)


def render_report(metadata: dict) -> str:
    limitations = metadata["limitations"] or ["暂无"]
    limitations_text = "；".join(limitations)

    return f"""# 视频字幕知识要点报告

## 基本信息

- 视频/课程：{metadata["title"]}
- 来源：{metadata["source"]}
- 时长：未确认
- 处理时间：{metadata["processed_at"]}

## 来源与限制

- 来源链接：{metadata["source_url"]}
- 字幕获取方式：{metadata["acquisition_method"]}
- 预计处理耗时：{metadata["time_estimate"]["estimated_range"]}
- 估时依据：{metadata["time_estimate"]["source_kind"]}，{metadata["time_estimate"]["acquisition_method_hint"]}
- 主要不确定因素：{"；".join(metadata["time_estimate"]["risk_factors"])}
- 内容完整性：{metadata["completeness"]}
- 已知限制：{limitations_text}
- 准确性说明：本报告基于可提取的字幕/transcript 整理生成；本技能不进行音频转写。

## 一句话总结

待补充：需要先取得字幕/transcript 内容。

## 核心要点

待补充。

## 分段笔记

待补充：取得带时间戳的字幕后按章节整理。

## 方法与流程

待补充。

## 术语表

| 术语 | 解释 |
|---|---|

## 行动清单

- [ ] 提供 SRT/VTT 字幕文件，或在浏览器中打开页面暴露字幕/transcript。

## 待确认问题

- 该视频源是否暴露可读字幕？
- 是否已有字幕或课程 transcript 可用？
"""


def print_judgment_and_estimate(source: str, estimation: dict) -> None:
    print("【判断结果】")
    print(f"- 输入类型：{estimation['source_kind']}")
    print(f"- 字幕可达性：{estimation['subtitle_judgment']}")
    print(f"- 字幕获取方式：{estimation['acquisition_method_hint']}")
    print(f"- 限制因素：{'; '.join(estimation['risk_factors'])}")
    print()
    if estimation["subtitle_judgment"] == "not-accessible":
        print("【预计处理耗时】无法估时（字幕不可达）。本技能不做音频转写。")
        print("建议：1) 提供 SRT/VTT 字幕文件；2) 换用有字幕的视频源；3) 在浏览器中打开页面让助手读取可见 transcript 面板。")
    else:
        print(f"【预计处理耗时】{estimation['estimated_range']}。")
        if estimation["is_slow"]:
            print("提示：预计会超过 30 分钟，可先生成快速版报告。")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a subtitle-only Markdown report scaffold for a video source."
    )
    parser.add_argument("source", help="Video URL, local subtitle path, or local media path.")
    parser.add_argument("--output-dir", default="reports", help="Directory for generated reports.")
    parser.add_argument("--work-dir", default="work", help="Directory for metadata/intermediate files.")
    parser.add_argument(
        "--duration-minutes",
        type=float,
        help="Known video duration in minutes (informational only; subtitle extraction is near-constant).",
    )
    parser.add_argument(
        "--file-size-mb",
        type=float,
        help="Known file size in MB (informational only).",
    )
    parser.add_argument(
        "--estimate-only",
        action="store_true",
        help="Only print the judgment + estimated time without writing report files.",
    )
    parser.add_argument(
        "--verbose-prompts",
        action="store_true",
        help="Print detailed user-facing guidance and boundary prompts.",
    )
    args = parser.parse_args()

    source = args.source
    source_is_url = is_url(source)
    source_kind = classify_source(source)
    estimation = estimate_subtitle_extraction(source_kind, args.duration_minutes, args.file_size_mb)

    emit(
        "我可以帮你归纳这个视频，但仅处理可提取字幕的内容——不做音频转写、播放捕获，"
        "也不会绕过 DRM、付费墙或登录限制。我会先判断字幕是否可达并给出估时；"
        "如果字幕不可达，我会告知原因并建议你提供字幕文件或更换有字幕的视频源。",
        args.verbose_prompts,
    )

    print_judgment_and_estimate(source, estimation)

    if args.estimate_only:
        return 0

    if estimation["subtitle_judgment"] == "not-accessible":
        print("\n已跳过报告脚手架生成：字幕不可达，等待用户提供字幕文件或更换视频源。")
        return 0

    work_dir = Path(args.work_dir)
    output_dir = Path(args.output_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Never persist the raw source URL to disk — it may carry access tokens,
    # session IDs, or other credentials in query parameters. The sanitized
    # form is used for metadata, report file names, and rendered titles.
    display_source = sanitize_url(source) if source_is_url else source
    title = slugify(display_source)
    acquisition_method = "pending-online-subtitle-extraction" if source_is_url else "user-provided-subtitle-file"

    if source_is_url:
        limitations = [
            "尚未接入当前站点的字幕或 transcript 提取结果",
            "如页面需要登录，请用户在浏览器中自行完成授权",
            "URL 中可能的鉴权参数已脱敏后再写入本地文件与报告",
        ]
        completeness = "partial"
    else:
        path = Path(source).expanduser()
        if path.exists():
            limitations = []
            completeness = "unknown"
        else:
            limitations = ["本地文件不存在或当前环境不可访问"]
            completeness = "partial"

    metadata = {
        "title": title,
        "source": "online-url" if source_is_url else "local-file",
        "source_url": display_source if source_is_url else "",
        "input": display_source,
        "processed_at": now,
        "acquisition_method": acquisition_method,
        "completeness": completeness,
        "limitations": limitations,
        "time_estimate": estimation,
    }

    metadata_path = work_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path = output_dir / f"{datetime.now().strftime('%Y%m%d')}-{title}-summary.md"
    report_path.write_text(render_report(metadata), encoding="utf-8")

    print(f"metadata: {metadata_path}")
    print(f"report: {report_path}")

    print("\n提示：Markdown 报告完成后，请向用户问询是否需要导出 docx/pdf/html 等其他格式。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
