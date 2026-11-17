#!/usr/bin/env python3
"""
xhs-deep-summary-local / run.py
小红书【视频】笔记本地深度总结 —— 自包含执行脚本（不依赖 xiaohongshu-extract / openai-whisper）。

流程：抽元数据(yt-dlp) -> 下载视频(curl) -> 提音频(imageio-ffmpeg) -> 转写(faster-whisper 本地模型)
产出：xhs_meta.json（元数据） + xhs_temp.txt（逐字稿）

环境变量（可选覆盖）：
  XHS_VENV_PY         managed venv 的 python 路径
  XHS_WHISPER_MODEL   faster-whisper CT2 模型目录
"""
import sys
import os
import json
import subprocess

# ---------- 路径解析（优先环境变量，回退自动探测，不绑定特定用户名） ----------
def _resolve_venv_python():
    if os.environ.get("XHS_VENV_PY"):
        return os.environ["XHS_VENV_PY"]
    candidates = [
        os.path.expanduser("~/.workbuddy/binaries/python/envs/default/bin/python"),
        os.path.expanduser("~/.workbuddy/binaries/python/versions/3.13.12/bin/python3"),
        "python3",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]


def _resolve_model_dir():
    if os.environ.get("XHS_WHISPER_MODEL"):
        return os.environ["XHS_WHISPER_MODEL"]
    return os.path.expanduser("~/.workbuddy/models/faster-whisper-small")


VENV_PY = _resolve_venv_python()
YTDLP = os.path.join(os.path.dirname(VENV_PY), "yt-dlp")
MODEL_DIR = _resolve_model_dir()


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def get_ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def extract_meta(url):
    """用 yt-dlp 抽元数据 + 视频直链。"""
    log("1/4 抽取元数据 (yt-dlp) ...")
    out = subprocess.run(
        [VENV_PY, YTDLP, "--dump-json", "--no-warnings", url],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise RuntimeError("yt-dlp 抽取失败: " + out.stderr[:400])
    # dump-json 可能夹带进度行，取最后一个合法 JSON
    data = None
    for line in reversed(out.stdout.strip().splitlines()):
        try:
            data = json.loads(line)
            break
        except Exception:
            continue
    if data is None:
        raise RuntimeError("无法解析 yt-dlp 元数据 JSON")
    return {
        "title": data.get("title") or "",
        "description": data.get("description") or "",
        "video_stream_url": data.get("url") or "",
        "duration": data.get("duration") or 0,
        "webpage_url": data.get("webpage_url") or url,
        "uploader": data.get("uploader") or "",
        "uploader_id": data.get("uploader_id") or "",
        "like_count": data.get("like_count"),
        "view_count": data.get("view_count"),
        "ext": data.get("ext") or "mp4",
    }


def download_video(video_url):
    log("2/4 下载视频 (curl) ...")
    r = subprocess.run(["curl", "-s", "-L", video_url, "-o", "xhs_temp.mp4"], check=True)
    if not os.path.exists("xhs_temp.mp4") or os.path.getsize("xhs_temp.mp4") < 1024:
        raise RuntimeError("视频下载失败或文件过小")


def extract_audio(ffmpeg):
    log("3/4 提取音频 (ffmpeg) ...")
    subprocess.run(
        [ffmpeg, "-i", "xhs_temp.mp4", "-vn", "-acodec", "libmp3lame",
         "-q:a", "2", "xhs_temp.mp3", "-y", "-loglevel", "error"],
        check=True,
    )


def transcribe():
    log("4/4 本地转写 (faster-whisper) ...")
    if not os.path.isdir(MODEL_DIR):
        raise RuntimeError(
            f"未找到 whisper 模型目录: {MODEL_DIR}\n"
            f"请从 ModelScope 下载 Systran/faster-whisper-small (CT2 格式) 到该路径，"
            f"或用环境变量 XHS_WHISPER_MODEL 指定。"
        )
    from faster_whisper import WhisperModel
    model = WhisperModel(MODEL_DIR, device="cpu", compute_type="int8")
    segments, info = model.transcribe("xhs_temp.mp3", language="zh", beam_size=5)
    text = "".join(s.text for s in segments).strip()
    with open("xhs_temp.txt", "w", encoding="utf-8") as f:
        f.write(text)
    log(f"识别语言: {info.language} (置信度 {info.language_probability:.3f})")
    return text


def main():
    if len(sys.argv) < 2:
        print("用法: python run.py <xhs_video_url>")
        sys.exit(1)
    url = sys.argv[1]

    meta = extract_meta(url)
    if not meta["video_stream_url"]:
        print("错误：未抽到 video_stream_url，可能不是视频笔记或链接已失效。", file=sys.stderr)
        sys.exit(1)
    with open("xhs_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    download_video(meta["video_stream_url"])
    ffmpeg = get_ffmpeg()
    extract_audio(ffmpeg)
    transcribe()

    print("======================================")
    print("完成！产物：")
    print("- 元数据: xhs_meta.json")
    print("- 逐字稿: xhs_temp.txt")


if __name__ == "__main__":
    main()
