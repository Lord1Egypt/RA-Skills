#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地音视频转文字，结果按内容哈希缓存。

用法:
    python transcribe.py <文件路径> [--model base] [--lang auto] [--force] [--device auto] [--cache-dir DIR] [--print]

依赖: faster-whisper (pip install faster-whisper)、ffmpeg。
完全独立于大模型运行，音频不出本机。
"""

import argparse
import hashlib
import json
import logging
import subprocess
import sys
import tempfile
import time
from pathlib import Path

LOG = logging.getLogger("zhz-transcribe")

CACHE_ROOT = Path.home() / ".cache" / "zhz-transcript"

if sys.platform == "win32":
    CREATE_NO_WINDOW = 0x08000000
else:
    CREATE_NO_WINDOW = 0


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
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def fatal(msg):
    LOG.error(msg)
    sys.exit(1)


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_hidden(cmd):
    kw = {}
    if CREATE_NO_WINDOW:
        kw["creationflags"] = CREATE_NO_WINDOW
    return subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kw)


def extract_audio(src, dst_wav, ffmpeg="ffmpeg"):
    cmd = [
        ffmpeg, "-y", "-i", str(src), "-vn",
        "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(dst_wav),
    ]
    r = run_hidden(cmd)
    if r.returncode != 0:
        fatal(f"ffmpeg 提取音频失败: {r.stderr.decode('utf-8', 'replace')[-500:]}")


def pick_device(device):
    if device in ("cpu", "cuda"):
        return device
    try:
        import ctranslate2
        if ctranslate2.get_cuda_device_count() > 0:
            return "cuda"
    except Exception:
        pass
    return "cpu"


def _load_model(model_size, device):
    from faster_whisper import WhisperModel
    # CUDA 优先 float16，失败则回退 int8（兼容不支持高效 float16 的 GPU）
    if device == "cuda":
        for compute_type in ("float16", "int8"):
            try:
                LOG.info(f"加载 Whisper 模型 {model_size} (device={device}, compute={compute_type}) ...")
                return WhisperModel(model_size, device=device, compute_type=compute_type)
            except Exception as e:
                LOG.warning(f"compute={compute_type} 加载失败，尝试回退: {e}")
    LOG.info(f"加载 Whisper 模型 {model_size} (device={device}, compute=int8) ...")
    return WhisperModel(model_size, device=device, compute_type="int8")


def transcribe_audio(audio_path, model_size, lang, device):
    from faster_whisper import WhisperModel
    lang_arg = None if lang in (None, "", "auto") else lang
    # 优先尝试指定/自动检测的设备，失败则回退 CPU（例如 CUDA 运行时缺少 cublas dll）
    for dev in ([device, "cpu"] if device == "cuda" else [device]):
        try:
            model = _load_model(model_size, dev)
            LOG.info("开始转录 ...")
            segments, info = model.transcribe(
                str(audio_path), language=lang_arg, vad_filter=True, beam_size=5
            )
            seg_list = []
            for seg in segments:
                seg_list.append({
                    "start": round(float(seg.start), 3),
                    "end": round(float(seg.end), 3),
                    "text": seg.text.strip(),
                })
            return {
                "duration": round(float(info.duration), 3),
                "language": info.language,
                "language_probability": round(float(info.language_probability), 4),
                "segments": seg_list,
            }
        except Exception as e:
            if dev == "cuda":
                LOG.warning(f"CUDA 转录失败，回退 CPU: {e}")
                continue
            raise
    raise RuntimeError("转录失败")


def main():
    _reconfigure_stdout()
    _setup_logging()
    ap = argparse.ArgumentParser(description="本地音视频转文字（按内容哈希缓存）")
    ap.add_argument("path", help="音视频文件路径")
    ap.add_argument("--model", default="base", help="Whisper 模型: tiny/base/small/medium/large-v3 (默认 base)")
    ap.add_argument("--lang", default="auto", help="强制语言 (zh/en/...；默认 auto 自动检测)")
    ap.add_argument("--force", action="store_true", help="忽略缓存，重新转录")
    ap.add_argument("--device", default="auto", help="auto/cpu/cuda")
    ap.add_argument("--cache-dir", default=None, help="缓存目录（默认 ~/.cache/zhz-transcript）")
    ap.add_argument("--print", dest="print_text", action="store_true", help="把转录全文打印到 stdout")
    args = ap.parse_args()

    src = Path(args.path).expanduser().resolve()
    if not src.is_file():
        fatal(f"文件不存在: {src}")

    cache_root = Path(args.cache_dir).expanduser() if args.cache_dir else CACHE_ROOT
    cache_root.mkdir(parents=True, exist_ok=True)

    content_hash = file_sha256(src)
    model = args.model
    json_path = cache_root / f"{content_hash}-{model}.json"
    txt_path = cache_root / f"{content_hash}-{model}.txt"

    if not args.force and json_path.is_file():
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            fatal(f"缓存损坏，请加 --force 重新转录: {e}")
        LOG.info("✅ 缓存命中（无需重新转录）")
        _report(src, data, json_path, txt_path)
        if args.print_text:
            sys.stdout.write(data.get("text", "") + "\n")
        return

    LOG.info(f"未命中缓存，开始转录: {src.name}")
    LOG.info(f"内容哈希: {content_hash[:16]}...")

    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "audio.wav"
        LOG.info("提取音频 (16kHz mono) ...")
        extract_audio(src, wav)
        result = transcribe_audio(wav, model, args.lang, pick_device(args.device))

    text = " ".join(s["text"] for s in result["segments"]).strip()
    data = {
        "content_hash": content_hash,
        "model": model,
        "source": str(src),
        "source_size": src.stat().st_size,
        "source_mtime": src.stat().st_mtime,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": result["duration"],
        "language": result["language"],
        "language_probability": result["language_probability"],
        "text": text,
        "segments": result["segments"],
    }
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    txt_path.write_text(text, encoding="utf-8")

    _report(src, data, json_path, txt_path)
    if args.print_text:
        sys.stdout.write(text + "\n")


def _report(src, data, json_path, txt_path):
    n = len(data.get("segments", []))
    LOG.info(f"来源: {src.name}")
    LOG.info(f"时长: {_fmt_dur(data.get('duration', 0))}")
    LOG.info(f"语言: {data.get('language')} (置信度 {data.get('language_probability')})")
    LOG.info(f"段落: {n}")
    LOG.info(f"缓存 JSON: {json_path}")
    LOG.info(f"纯文本: {txt_path}")


def _fmt_dur(seconds):
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m}:{sec:02d}"


if __name__ == "__main__":
    main()
