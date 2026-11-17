#!/usr/bin/env python3
"""使用 faster-whisper 将音频转录为 SRT，支持 HF 镜像回退。"""

import os
import sys
import json
import logging
from pathlib import Path

LOG = logging.getLogger("zhz-subtitle")

# 使用 HuggingFace 国内镜像，解决访问问题
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")


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


def _to_simplified(text: str) -> str:
    """将繁体中文转换为简体中文（Whisper 输出中文时默认是繁体）。"""
    try:
        import zhconv
    except ImportError:
        LOG.info("正在安装 zhconv（用于繁体转简体）...")
        os.system(f"{sys.executable} -m pip install zhconv -q")
        import zhconv
    return zhconv.convert(text, "zh-cn")


def format_timestamp(seconds: float) -> str:
    """将秒数转换为 SRT 时间戳格式 HH:MM:SS,mmm。"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def transcribe(audio_path: str, model_size: str = "base",
               language: str | None = None) -> dict:
    """转录音频文件并返回带时间戳的段落。

    参数:
        audio_path: 音频文件路径。
        model_size: Whisper 模型大小（tiny, base, small, medium, large-v3）。
        language: 强制指定语言（zh, en 等）。None 表示自动检测。

    返回:
        包含 'language'、'duration'、'segments'（含 start, end, text 的列表）的字典。
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        LOG.info("正在安装 faster-whisper...")
        os.system(f"{sys.executable} -m pip install faster-whisper -q")
        from faster_whisper import WhisperModel

    audio = Path(audio_path)
    if not audio.exists():
        fatal(f"找不到音频文件：{audio_path}")

    LOG.info("正在加载 Whisper 模型：%s", model_size)
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    LOG.info("正在转录：%s", audio.name)
    kwargs = {}
    if language:
        kwargs["language"] = language

    segments_iter, info = model.transcribe(str(audio), **kwargs)

    detected_lang = info.language
    duration = info.duration
    lang_prob = info.language_probability

    LOG.info("检测到的语言：%s（置信度：%.2f）", detected_lang, lang_prob)
    LOG.info("音频时长：%.1f 秒", duration)

    segments = []
    for seg in segments_iter:
        text = seg.text.strip()
        # Whisper 转写中文时默认输出繁体，统一转为简体
        if detected_lang and detected_lang.startswith("zh"):
            text = _to_simplified(text)
        segments.append({
            "start": seg.start,
            "end": seg.end,
            "text": text
        })

    result = {
        "language": detected_lang,
        "language_probability": lang_prob,
        "duration": duration,
        "segments": segments
    }

    # 保存为 JSON 格式，供后续流程使用
    json_path = str(audio.with_suffix(".transcript.json"))
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    LOG.info("转录结果已保存：%s", json_path)

    # 保存为 SRT 格式，根据检测到的语言自动命名
    stem = audio.stem
    lang_suffix = ".chs" if detected_lang == "zh" else ".en"
    srt_path = str(audio.parent / f"{stem}{lang_suffix}.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n")
            f.write(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}\n")
            f.write(f"{seg['text']}\n\n")
    LOG.info("原始字幕已保存：%s", srt_path)

    return result


if __name__ == "__main__":
    _reconfigure_stdout()
    _setup_logging()
    if len(sys.argv) < 2:
        fatal("用法：python transcribe.py <音频路径> [模型大小] [语言]\n"
              "  模型大小：tiny, base, small, medium, large-v3（默认：base）\n"
              "  语言：zh, en 等（默认：自动检测）")

    audio_path = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    language = sys.argv[3] if len(sys.argv) > 3 else None

    result = transcribe(audio_path, model_size, language)
    LOG.info("转录完成：共 %d 个段落", len(result["segments"]))
