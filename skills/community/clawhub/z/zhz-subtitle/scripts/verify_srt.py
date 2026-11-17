#!/usr/bin/env python3
"""验证 SRT 文件格式和双语结构。"""

import sys
import re
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


def verify_srt(srt_path: str) -> dict:
    """验证 SRT 文件格式、时间戳和双语结构。

    返回:
        包含 'valid'（是否通过）、'warnings'（警告）、'errors'（错误）、'stats'（统计）的字典。
    """
    path = Path(srt_path)
    if not path.exists():
        return {"valid": False, "errors": [f"文件不存在：{srt_path}"], "warnings": [], "stats": {}}

    with open(path, "r", encoding="utf-8-sig") as f:
        content = f.read().strip()

    errors = []
    warnings = []

    blocks = re.split(r"\n\n+", content)
    if not blocks:
        return {"valid": False, "errors": ["SRT 文件为空"], "warnings": [], "stats": {}}

    prev_end_ts = None
    entry_count = 0
    bilingual_count = 0
    total_text_len = 0
    has_chinese = False
    has_english = False

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            errors.append(f"格式错误的段落（需要至少 3 行）：{block[:80]}")
            continue

        # 检查序号
        try:
            idx = int(lines[0].strip())
            entry_count += 1
        except ValueError:
            errors.append(f"无效的序号：'{lines[0].strip()}'")
            continue

        # 检查时间戳格式
        time_match = re.match(
            r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})",
            lines[1].strip()
        )
        if not time_match:
            errors.append(f"第 {idx} 条时间戳格式错误：'{lines[1].strip()}'")
            continue

        # 将时间戳转换为毫秒，用于检查重叠
        def ts_to_ms(h, m, s, ms):
            return int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms)

        start_ms = ts_to_ms(*time_match.groups()[:4])
        end_ms = ts_to_ms(*time_match.groups()[4:])

        # 检查结束时间是否晚于开始时间
        if end_ms <= start_ms:
            errors.append(f"第 {idx} 条：结束时间早于或等于开始时间")

        # 检查是否与上一条字幕重叠
        if prev_end_ts is not None and start_ms < prev_end_ts:
            warnings.append(f"第 {idx} 条：与上一条字幕存在时间重叠")
        prev_end_ts = end_ms

        # 检查文本行数（双语应有至少 2 行）
        text_lines = lines[2:]
        if len(text_lines) >= 2:
            bilingual_count += 1

        text = " ".join(text_lines)
        total_text_len += len(text)

        # 检测中文和英文字符
        if re.search(r"[\u4e00-\u9fff]", text):
            has_chinese = True
        if re.search(r"[a-zA-Z]", text):
            has_english = True

    # 判断是否为双语字幕
    is_bilingual = has_chinese and has_english
    total_duration_s = prev_end_ts / 1000 if prev_end_ts else 0

    stats = {
        "entries": entry_count,
        "bilingual_entries": bilingual_count,
        "is_bilingual": is_bilingual,
        "has_chinese": has_chinese,
        "has_english": has_english,
        "total_duration": f"{total_duration_s:.1f}s",
        "avg_text_length": round(total_text_len / max(entry_count, 1), 1)
    }

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings, "stats": stats}


if __name__ == "__main__":
    _reconfigure_stdout()
    _setup_logging()
    if len(sys.argv) < 2:
        fatal("用法：python verify_srt.py <srt文件路径>")

    result = verify_srt(sys.argv[1])

    if result["valid"]:
        LOG.info("✅ SRT 验证通过！")
    else:
        LOG.info("❌ SRT 验证失败！")

    stats = result["stats"]
    LOG.info("")
    LOG.info("📊 统计信息：")
    LOG.info("  字幕条目：%d 条", stats.get("entries", 0))
    LOG.info("  双语字幕：%s", "是" if stats.get("is_bilingual") else "否")
    langs = []
    if stats.get("has_chinese"):
        langs.append("中文")
    if stats.get("has_english"):
        langs.append("英文")
    LOG.info("  包含语言：%s", "、".join(langs) if langs else "未知")
    LOG.info("  总时长：%s", stats.get("total_duration", "N/A"))
    LOG.info("  平均文本长度：%s 字符", stats.get("avg_text_length", 0))

    if result["warnings"]:
        LOG.info("")
        LOG.info("⚠️ 警告（%d 条）：", len(result["warnings"]))
        for w in result["warnings"]:
            LOG.info("  - %s", w)

    if result["errors"]:
        LOG.info("")
        LOG.error("❌ 错误（%d 条）：", len(result["errors"]))
        for e in result["errors"]:
            LOG.error("  - %s", e)
        sys.exit(1)
