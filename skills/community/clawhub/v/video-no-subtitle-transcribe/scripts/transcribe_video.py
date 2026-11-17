#!/usr/bin/env python3
"""无字幕视频转写兜底工具：yt-dlp 下载音频 + faster-whisper 本地转写。

用法:
    python3 transcribe_video.py <URL> [--lang zh] [--out transcript.txt]

依赖: yt-dlp, faster-whisper, ffmpeg；模型 ~/.local/share/whisper-small（缺失自动下载）
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile

MODEL_DIR = os.path.expanduser("~/.local/share/whisper-small")
MODEL_BIN = os.path.join(MODEL_DIR, "model.bin")
MODEL_URL = "https://modelscope.cn/models/Systran/faster-whisper-small/resolve/master/model.bin"
MODEL_EXPECTED_BYTES = 483546902


def get_proxy(explicit=""):
    """获取代理。优先级：--proxy 参数 > 环境变量 HTTPS_PROXY/HTTP_PROXY
    > OpenClaw 配置（~/.openclaw/openclaw.json，国内环境常用）。
    """
    if explicit:
        return explicit
    for var in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        v = os.environ.get(var)
        if v:
            return v
    try:
        with open(os.path.expanduser("~/.openclaw/openclaw.json")) as f:
            cfg = json.load(f)
        return cfg.get("channels", {}).get("telegram", {}).get("proxy", "")
    except Exception:
        return ""


def ensure_model():
    """模型缺失或损坏时从 ModelScope 下载。"""
    if os.path.exists(MODEL_BIN) and os.path.getsize(MODEL_BIN) == MODEL_EXPECTED_BYTES:
        return
    if os.path.exists(MODEL_BIN):
        print(f"[model] size mismatch ({os.path.getsize(MODEL_BIN)}), re-downloading", flush=True)
        os.remove(MODEL_BIN)
    os.makedirs(MODEL_DIR, exist_ok=True)
    print(f"[model] downloading from ModelScope -> {MODEL_BIN}", flush=True)
    import urllib.request
    part = MODEL_BIN + ".part"
    req = urllib.request.Request(MODEL_URL)
    with urllib.request.urlopen(req, timeout=900) as r, open(part, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    os.rename(part, MODEL_BIN)
    got = os.path.getsize(MODEL_BIN)
    if got != MODEL_EXPECTED_BYTES:
        print(f"[model] WARNING: {got} != expected {MODEL_EXPECTED_BYTES}", flush=True)
    print(f"[model] ready ({got} bytes)", flush=True)


def run_ytdlp(cmd, proxy=""):
    """跑 yt-dlp，返回 (returncode, stderr)。"""
    env = dict(os.environ)
    proxy = get_proxy(proxy)
    if proxy:
        env["HTTPS_PROXY"] = proxy
        env["HTTP_PROXY"] = proxy
    base = ["yt-dlp"]
    if proxy:
        base += ["--proxy", proxy]
    r = subprocess.run(base + cmd, env=env, capture_output=True, text=True)
    return r.returncode, r.stderr


def download_audio(url, workdir, proxy=""):
    """按序尝试客户端下载音频，返回音频文件路径。"""
    # tv_embedded 最稳（能绕过 DRM/SABR 实验），android/ios 次之，最后默认
    for client in ["tv_embedded", "android", "ios"]:
        out = os.path.join(workdir, f"audio_{client}.%(ext)s")
        print(f"[dl] trying client={client} ...", flush=True)
        rc, err = run_ytdlp([
            "--extractor-args", f"youtube:player_client={client}",
            "-f", "bestaudio/best", "-o", out, url,
        ], proxy)
        if rc == 0:
            files = glob.glob(os.path.join(workdir, f"audio_{client}.*"))
            if files:
                return files[0]
        print(f"  failed: {err.strip().splitlines()[-1] if err.strip() else '?'}", flush=True)
    # 默认客户端兜底（B 站等其他站点）
    out = os.path.join(workdir, "audio_default.%(ext)s")
    rc, err = run_ytdlp(["-f", "bestaudio/best", "-o", out, url], proxy)
    if rc == 0:
        files = glob.glob(os.path.join(workdir, "audio_default.*"))
        if files:
            return files[0]
    sys.exit(f"[dl] FAILED, last error: {err[-600:]}")


def transcribe(audio_path, lang, out_path):
    """faster-whisper 本地转写，输出带时间戳文稿。"""
    from faster_whisper import WhisperModel
    print(f"[whisper] loading model ...", flush=True)
    model = WhisperModel(MODEL_DIR, device="cpu", compute_type="int8")
    print(f"[whisper] transcribing {audio_path} (lang={lang}) ...", flush=True)
    segments, _ = model.transcribe(audio_path, language=lang, vad_filter=True)
    lines = []
    with open(out_path, "w", encoding="utf-8") as f:
        for s in segments:
            line = f"[{s.start:.1f}-{s.end:.1f}] {s.text}"
            lines.append(line)
            f.write(line + "\n")
    print(f"[done] {len(lines)} segments -> {out_path}", flush=True)


def main():
    ap = argparse.ArgumentParser(description="无字幕视频转写（yt-dlp + faster-whisper）")
    ap.add_argument("url", help="视频 URL 或本地音视频文件路径")
    ap.add_argument("--lang", default="zh", help="语言代码，默认 zh")
    ap.add_argument("--out", default="transcript.txt", help="输出文件，默认 transcript.txt")
    ap.add_argument("--proxy", default="", help="代理地址，如 http://127.0.0.1:7890（默认读环境变量/OpenClaw 配置）")
    args = ap.parse_args()

    ensure_model()
    # 本地文件直接转写，不下载
    if os.path.exists(args.url):
        transcribe(args.url, args.lang, args.out)
        return
    with tempfile.TemporaryDirectory() as workdir:
        audio = download_audio(args.url, workdir, args.proxy)
        transcribe(audio, args.lang, args.out)


if __name__ == "__main__":
    main()
