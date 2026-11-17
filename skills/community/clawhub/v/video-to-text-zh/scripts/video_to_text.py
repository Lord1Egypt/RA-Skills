# -*- coding: utf-8 -*-
"""
视频语音转文字管道：video_to_text.py <视频链接> [输出目录]

流程：
1. 展开短链接（v.douyin.com / b23.tv 等）
2. 获取媒体地址：优先 yt-dlp；抖音等需要 Cookie/签名的站点自动回退到
   无头 Chromium 捕获（见 discover_media.py）
3. 下载音频轨道或视频（优先纯音频，体积小）
4. ffmpeg 转成 16kHz 单声道 WAV
5. faster-whisper 转写为中文文字稿（带时间轴 + 纯文字两版）

依赖：requests、imageio-ffmpeg（完整版 ffmpeg 二进制）、faster-whisper、
      yt-dlp、playwright + Chromium（仅抖音类站点回退时需要）
"""
import sys, os, re, json, subprocess, argparse, warnings
from pathlib import Path
from urllib.parse import urlparse

warnings.filterwarnings("ignore")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Referer": "https://www.douyin.com/"}

VIDEO_HOST_HINTS = ("douyinvod.com", "bytecdn", "yximgs", "zijieapi",
                    "hdslb.com", "googlevideo.com", "bili")


def log(*a):
    print("[video-to-text]", *a)


def expand_short_url(url: str) -> str:
    """跟随 302 展开短链接"""
    import requests
    r = requests.head(url, headers={"User-Agent": UA}, allow_redirects=True,
                      timeout=30, verify=False)
    return r.url


def resolve_canonical(url: str) -> tuple[str, str]:
    """返回 (站点标识, 规范化URL)。站点: douyin/bilibili/youtube/other"""
    url = expand_short_url(url)
    host = urlparse(url).netloc.lower()
    if "douyin.com" in host:
        m = re.search(r"video/(\d+)", url)
        if m:
            return "douyin", f"https://www.douyin.com/video/{m.group(1)}"
        return "douyin", url
    if "bilibili.com" in host or "b23.tv" in host:
        m = re.search(r"(BV\w+)", url)
        if m:
            return "bilibili", f"https://www.bilibili.com/video/{m.group(1)}"
        return "bilibili", url
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube", url
    return "other", url


def try_ytdlp(url: str, out_dir: Path) -> dict | None:
    """用 yt-dlp 直接下载音频。成功返回 {title, audio}, 失败返回 None"""
    audio = out_dir / "source_audio"
    # 只下载不转码（imageio-ffmpeg 不带 ffprobe，yt-dlp 的 -x 后处理会失败），
    # 统一交给 to_wav() 用 ffmpeg 转 16kHz WAV
    cmd = [sys.executable, "-m", "yt_dlp", "-f", "bestaudio/best",
           "-o", str(audio) + ".%(ext)s", "--no-playlist",
           "--socket-timeout", "30", url]
    log("尝试 yt-dlp 下载:", url)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        log("yt-dlp 失败:", (r.stderr or r.stdout).strip().splitlines()[-1][:200])
        return None
    # 找到产出的 wav（-x --audio-format wav 可能仍输出原格式，再用 ffmpeg 转）
    for f in out_dir.glob("source_audio.*"):
        return {"title": "", "audio": f}
    return None


def find_chrome() -> str | None:
    """跨平台自动发现 Playwright Chromium 可执行文件"""
    import glob as _glob
    pats = []
    if sys.platform == "win32":
        la = os.environ.get("LOCALAPPDATA", "")
        if la:
            pats.append(os.path.join(la, r"ms-playwright\chromium-*\chrome-win*\chrome.exe"))
    else:
        home = os.path.expanduser("~")
        pats.append(os.path.join(home, ".cache/ms-playwright/chromium-*/chrome-linux/chrome"))
        pats.append(os.path.join(home, ".cache/ms-playwright/chromium-*/chrome-linux64/chrome"))
        pats.append(os.path.join(home, "Library/Caches/ms-playwright/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium"))
    cands = []
    for pat in pats:
        cands += _glob.glob(pat)
    cands += _glob.glob(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/nonexistent") + "/chromium-*/*/chrome*")
    return sorted(cands)[-1] if cands else None


def try_playwright(url: str, out_dir: Path, timeout_s: int = 90) -> dict | None:
    """无头 Chromium 打开页面捕获媒体 URL（针对抖音等反爬站点）"""
    from playwright.sync_api import sync_playwright

    chrome = find_chrome()
    if not chrome:
        log("未找到 Playwright Chromium，跳过浏览器回退（可运行: python -m playwright install chromium）")
        return None
    log("用无头 Chromium 捕获媒体地址:", chrome)

    media, title = [], ""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=chrome, headless=True,
            args=["--disable-blink-features=AutomationControlled"])
        ctx = browser.new_context(user_agent=UA, locale="zh-CN",
                                  viewport={"width": 1280, "height": 800})
        page = ctx.new_page()

        def on_response(resp):
            u = resp.url
            if ("douyinvod" in u or "media-audio" in u or "media-video" in u or ".mp4" in u) and u not in media:
                media.append(u)

        page.on("response", on_response)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
        except Exception as e:
            log("页面加载告警（可忽略）:", str(e)[:100])
        page.wait_for_timeout(6000)
        try:
            page.mouse.click(640, 400)  # 触发播放
            page.wait_for_timeout(4000)
        except Exception:
            pass
        # 回退：直接从 <video> 元素读取已解析的媒体地址（响应事件可能因时机错过）
        try:
            srcs = page.evaluate("""() => {
                const out = [];
                document.querySelectorAll('video').forEach(v => {
                    if (v.src) out.push(v.src);
                    if (v.currentSrc) out.push(v.currentSrc);
                });
                return out;
            }""")
            for s in srcs or []:
                if s and s not in media:
                    media.append(s)
        except Exception:
            pass
        try:
            title = page.title()
        except Exception:
            pass
        browser.close()

    audio_urls = [u for u in media if "media-audio" in u or ".m4a" in u]
    video_urls = [u for u in media
                  if ("douyinvod" in u or "media-video" in u or ".mp4" in u)
                  and "douyinstatic" not in u  # 排除播放器占位视频
                  and "uuu_" not in u]
    if not audio_urls and not video_urls:
        log("浏览器未捕获到媒体地址")
        return None
    # 优先下载纯音频轨
    import requests
    pick = (audio_urls or video_urls)[0]
    suffix = ".m4a" if audio_urls else ".mp4"
    dest = out_dir / ("source_audio" + suffix)
    log("下载媒体:", pick[:120], "...")
    r = requests.get(pick, headers=HEADERS, timeout=180, verify=False, stream=True)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(1 << 18):
            f.write(chunk)
    return {"title": title, "audio": dest}


def to_wav(src: Path, wav: Path):
    """用 imageio-ffmpeg 的完整版 ffmpeg 统一转成 16kHz 单声道 WAV"""
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    r = subprocess.run([ff, "-y", "-i", str(src), "-vn",
                        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
                        str(wav)], capture_output=True, text=True, timeout=300,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0 or not wav.exists():
        raise RuntimeError("ffmpeg 转码失败: " + r.stderr[-300:])


def transcribe(wav: Path, out_txt: Path, model_size: str = "small",
               prompt: str = "以下是普通话视频语音内容。"):
    from faster_whisper import WhisperModel
    log(f"加载 faster-whisper 模型 {model_size} ...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(wav), language="zh", beam_size=5, vad_filter=True,
        initial_prompt=prompt)
    segs = list(segments)
    lines_ts, lines_pure = [], []
    for s in segs:
        m1, s1 = int(s.start // 60), int(s.start % 60)
        lines_ts.append(f"[{m1:02d}:{s1:02d}] {s.text.strip()}")
        lines_pure.append(s.text.strip())
    text_ts = "\n".join(lines_ts)
    text_pure = "".join(lines_pure)
    out_txt.write_text(
        f"识别语言: {info.language} (置信度 {info.language_probability:.2f})\n\n"
        f"【带时间轴】\n{text_ts}\n\n【纯文字版】\n{text_pure}\n",
        encoding="utf-8")
    log(f"文字稿已保存: {out_txt}")
    return text_ts, text_pure


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("outdir", nargs="?", default=".")
    ap.add_argument("--model", default="small", help="whisper 模型大小")
    ap.add_argument("--keep-media", action="store_true", help="保留下载的音视频文件")
    args = ap.parse_args()

    out_dir = Path(args.outdir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    site, canon = resolve_canonical(args.url)
    log(f"站点: {site}  规范化: {canon}")

    got = try_ytdlp(canon, out_dir)
    title = ""
    if got is None and site == "douyin":
        got = try_playwright(canon, out_dir)
    if got is None:
        # 其他站点也尝试一次浏览器回退（可能是未识别的站点）
        got = try_playwright(canon, out_dir)
    if got is None:
        log("ERROR: 所有下载方式均失败")
        sys.exit(1)

    title = got.get("title") or ""
    wav = out_dir / "audio_16k.wav"
    if got["audio"].suffix == ".wav":
        wav = got["audio"]
    else:
        to_wav(got["audio"], wav)

    out_txt = out_dir / "文字稿.txt"
    text_ts, text_pure = transcribe(wav, out_txt, model_size=args.model)

    # 元数据
    (out_dir / "meta.json").write_text(json.dumps(
        {"url": args.url, "canonical": canon, "site": site, "title": title,
         "model": args.model}, ensure_ascii=False, indent=1), encoding="utf-8")

    if not args.keep_media:
        for f in {got["audio"], wav}:
            try:
                Path(f).unlink(missing_ok=True)
            except Exception:
                pass

    print("\n===== 文字稿 =====")
    print(text_ts)


if __name__ == "__main__":
    main()
