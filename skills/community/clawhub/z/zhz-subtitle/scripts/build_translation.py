#!/usr/bin/env python3
"""校验并规范化翻译 JSON，生成合法的 _translated.json。

用法：python build_translation.py <转录.json> <翻译.json> [输出.json]
- 读取转录 JSON 的 segments 作为 start/end 基准
- 读取翻译 JSON 的 segments（含翻译后的 text）
- 校验条目数一致，并强制使用转录的 start/end（防止时间戳错位）
- 用 json.dump 重新序列化，保证输出为合法 JSON（自动转义中文引号等特殊字符）

省略输出路径时，原地覆盖翻译 JSON。
"""

import json
import sys
import logging
from pathlib import Path

LOG = logging.getLogger("zhz-subtitle")


def _setup_logging():
    if LOG.handlers:
        return
    LOG.setLevel(logging.INFO)
    h_out = logging.StreamHandler(sys.stdout)
    h_out.setLevel(logging.INFO)
    h_out.addFilter(lambda r: r.levelno < logging.ERROR)
    h_err = logging.StreamHandler(sys.stderr)
    h_err.setLevel(logging.ERROR)
    h_err.setFormatter(logging.Formatter("[错误] %(message)s"))
    LOG.addHandler(h_out)
    LOG.addHandler(h_err)


def _reconfigure_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def fatal(msg):
    LOG.error(msg)
    sys.exit(1)


def load_json(path: str) -> dict:
    """读取 JSON，自动修复中文引号导致的解析问题。"""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        fixed = raw.replace("\u201c", "\\u201c").replace("\u201d", "\\u201d")
        fixed = fixed.replace("\u2018", "\\u2018").replace("\u2019", "\\u2019")
        try:
            data = json.loads(fixed)
            LOG.info("已自动修复 JSON 中的中文引号问题")
            return data
        except json.JSONDecodeError as e:
            fatal(f"JSON 解析失败：{e}。请确认翻译结果符合严格 JSON 格式。")


def build_translation(transcript_path: str, translation_path: str,
                      output_path: str | None = None) -> str:
    """校验翻译 JSON 并输出规范化后的合法 JSON。"""
    transcript = load_json(transcript_path)
    translation = load_json(translation_path)

    t_segs = transcript.get("segments", [])
    x_segs = translation.get("segments", [])

    if not t_segs:
        fatal(f"转录 JSON 中没有 segments：{transcript_path}")

    if len(t_segs) != len(x_segs):
        fatal(f"翻译条目数不一致：转录 {len(t_segs)} 条，翻译 {len(x_segs)} 条，请补齐或删除多余条目")

    out_segments = []
    for t, x in zip(t_segs, x_segs):
        text = x.get("text", "")
        if not isinstance(text, str):
            fatal(f"第 {len(out_segments) + 1} 段的 text 不是字符串")
        out_segments.append({
            "start": t["start"],
            "end": t["end"],
            "text": text.strip(),
        })

    data = {
        "language": translation.get("language", transcript.get("language")),
        "duration": transcript.get("duration", translation.get("duration")),
        "segments": out_segments,
    }

    if output_path is None:
        output_path = translation_path

    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    LOG.info("翻译 JSON 已规范化：%s（%d 段）", output_path, len(out_segments))
    return output_path


if __name__ == "__main__":
    _reconfigure_stdout()
    _setup_logging()
    if len(sys.argv) < 3:
        fatal("用法：python build_translation.py <转录.json> <翻译.json> [输出.json]")

    transcript_path = sys.argv[1]
    translation_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None

    build_translation(transcript_path, translation_path, output_path)
