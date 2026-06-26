#!/usr/bin/env python3
"""
tt_download.py — 提取素材中心 video_player 页面中的真实视频地址并下载。

流程：
    1. 用本机 Chrome 无头模式渲染 https://ad.oceanengine.com/material_center/outer/video_player?token=...
       （该页是 SPA，真实视频地址由 JS 注入到 <video> 标签里）。
    2. 从渲染后的 DOM 中提取 <video src="https://cc.oceanengine.com/anm/..."> 的 src。
    3. 跟随 cc.oceanengine.com 的 302 重定向，拿到 video-cn.oceanengine.com 上的最终视频 URL。
    4. 若指定 -o，则把视频流写到该文件；否则只打印最终 URL。

注意：返回的 video-cn URL 中带签名 / 时间戳，生命周期很短（分钟级），
      所以提取和下载必须一气呵成，不能保存 URL 之后再下载。
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from html.parser import HTMLParser
from typing import Iterable, Optional


UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def _program_files(*sub: str) -> list[str]:
    """Windows 上返回 Program Files / Program Files (x86) 下的候选路径。"""
    candidates: list[str] = []
    for env in ("ProgramFiles", "ProgramFiles(x86)", "ProgramW6432"):
        base = os.environ.get(env)
        if base:
            candidates.append(os.path.join(base, *sub))
    return candidates


# Chrome / Chromium / Edge 在 macOS / Linux / Windows 上的常见路径
CHROME_CANDIDATES: list[str] = [
    # macOS
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    # Linux
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/snap/bin/chromium",
]
# Windows（拆开拼，因为依赖环境变量）
CHROME_CANDIDATES += _program_files("Google", "Chrome", "Application", "chrome.exe")
CHROME_CANDIDATES += _program_files("Google", "Chrome Beta", "Application", "chrome.exe")
CHROME_CANDIDATES += _program_files("Microsoft", "Edge", "Application", "msedge.exe")
CHROME_CANDIDATES += _program_files("Chromium", "Application", "chrome.exe")


def find_chrome() -> str:
    """返回可用的浏览器可执行文件路径。"""
    for path in CHROME_CANDIDATES:
        if os.path.isfile(path):
            return path
    # PATH 里找常见的可执行名（Windows 上也能命中，前提是装在 PATH 里）
    for name in (
        "google-chrome", "google-chrome-stable", "chrome", "chromium",
        "chromium-browser", "chrome.exe", "msedge.exe",
    ):
        found = shutil.which(name)
        if found:
            return found
    raise RuntimeError(
        "未找到 Chrome / Chromium / Edge。请安装 Google Chrome 或 Microsoft Edge，"
        "或修改 CHROME_CANDIDATES 增加自定路径。"
    )


def render_with_chrome(url: str, timeout: int = 60) -> str:
    """用 headless Chrome 渲染页面并返回完整 DOM HTML。"""
    chrome = find_chrome()
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--disable-dev-shm-usage",
        "--virtual-time-budget=30000",  # 给 SPA 足够时间发起请求并渲染
        "--dump-dom",
        url,
    ]
    # Windows 下避免弹出额外的控制台窗口
    popen_kwargs = dict(capture_output=True, timeout=timeout)
    if sys.platform.startswith("win"):
        si = subprocess.STARTUPINFO()  # type: ignore[attr-defined]
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # type: ignore[attr-defined]
        popen_kwargs["startupinfo"] = si
        popen_kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    proc = subprocess.run(cmd, **popen_kwargs)
    if proc.returncode not in (0, 1):  # Chrome 在 --dump-dom 时偶尔返回 1
        raise RuntimeError(
            f"Chrome 运行失败 rc={proc.returncode}:\n"
            f"stderr: {proc.stderr.decode('utf-8', 'replace')[:1000]}"
        )
    # Chrome 在 Windows 上默认按 GBK 输出，但 --dump-dom 写的是 UTF-8；
    # 标准库默认按 locale 解码可能出错，这里强制 utf-8 + replace 兜底。
    html = proc.stdout.decode("utf-8", "replace")
    if not html:
        raise RuntimeError("Chrome 输出为空，无法解析 DOM。")
    return html


class VideoSrcExtractor(HTMLParser):
    """从 HTML 中抽取 <video> 的 src 属性。"""

    _VIDEO_SRC_RE = re.compile(r"<video\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)

    def __init__(self) -> None:
        super().__init__()
        self.srcs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag.lower() != "video":
            return
        for k, v in attrs:
            if k.lower() == "src" and v:
                self.srcs.append(v)

    @classmethod
    def extract_first(cls, html: str) -> str:
        parser = cls()
        parser.feed(html)
        if parser.srcs:
            return parser.srcs[0]
        # fallback：用正则再扫一遍（HTMLParser 对畸形 HTML 偶尔漏抓）
        m = cls._VIDEO_SRC_RE.search(html)
        if m:
            return m.group(1)
        raise RuntimeError("页面渲染后未找到 <video src=...> 标签，token 可能已失效或页面改版。")


def resolve_video_url(page_url: str) -> tuple[str, str, str]:
    """返回 (中间 cc.oceanengine.com src, 最终 video-cn 视频地址, cookie 字符串)。

    注意：cc URL 在 302 时会下发 vck_xxx cookie，这个 cookie 是后续下载 video-cn
    资源所必需的（缺它会返回 403 / X-Moat-Code 4119）。
    """
    html = render_with_chrome(page_url)
    cc_url = VideoSrcExtractor.extract_first(html)

    # cc.oceanengine.com URL 302 跳转到 video-cn 真实地址；不能跟随 body，只取 Location + Set-Cookie。
    req = urllib.request.Request(
        cc_url,
        headers={
            "User-Agent": UA,
            "Referer": "https://ad.oceanengine.com/",
            "Range": "bytes=0-1",  # 只想要 redirect header，不下载内容
        },
        method="GET",
    )
    opener = urllib.request.build_opener(NoRedirectHandler)
    try:
        opener.open(req, timeout=30)
    except urllib.error.HTTPError as e:
        location = e.headers.get("Location")
        if location:
            # 收集所有 Set-Cookie（可能多条）
            cookies = e.headers.get_all("Set-Cookie") or []
            cookie_str = "; ".join(
                c.split(";", 1)[0].strip() for c in cookies if "=" in c
            )
            return cc_url, location, cookie_str
        raise RuntimeError(f"cc URL 返回 HTTP {e.code} 但没有 Location 头。")
    raise RuntimeError("cc URL 未发生重定向，无法解析真实视频地址。")


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """禁止 urllib 自动跟随 302/301，让我们能拿到 Location 头。"""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        return None


def download(url: str, dest: str, cookie_str: str = "", chunk: int = 1 << 16) -> int:
    """把 url 流式写到 dest，返回写入字节数。"""
    headers = {
        "User-Agent": UA,
        "Referer": "https://ad.oceanengine.com/",
    }
    if cookie_str:
        headers["Cookie"] = cookie_str
    req = urllib.request.Request(url, headers=headers)
    written = 0
    with urllib.request.urlopen(req, timeout=60) as resp, open(dest, "wb") as f:
        while True:
            buf = resp.read(chunk)
            if not buf:
                break
            f.write(buf)
            written += len(buf)
    return written


def humanize(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="从素材中心 video_player 页面提取真实视频地址并下载",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  python3 tt_download.py 'https://ad.oceanengine.com/material_center/outer/video_player?token=...'\n"
            "  python3 tt_download.py '...token=...' -o video.mp4\n"
            "  python3 tt_download.py @url -o video.mp4   # 从文件读取 URL"
        ),
    )
    parser.add_argument("url", help="video_player 完整 URL，可用 @path 形式从文件读取")
    parser.add_argument(
        "-o", "--output", dest="output",
        help="保存为该文件；不传则只打印最终视频地址",
    )
    parser.add_argument(
        "--show-intermediate", action="store_true",
        help="同时打印 cc.oceanengine.com 中间 src 地址",
    )
    args = parser.parse_args()

    # 支持 @path 从文件读取 URL（更方便长 token）
    if args.url.startswith("@"):
        with open(args.url[1:], "r", encoding="utf-8") as f:
            page_url = f.read().strip()
    else:
        page_url = args.url.strip()
    if not page_url:
        print("URL 不能为空", file=sys.stderr)
        return 2

    try:
        cc_url, video_url, cookie_str = resolve_video_url(page_url)
    except Exception as e:
        print(f"❌ 提取视频地址失败：{e}", file=sys.stderr)
        return 1

    if args.show_intermediate:
        print(f"intermediate: {cc_url}", file=sys.stderr)
    print(video_url)

    if args.output:
        try:
            n = download(video_url, args.output, cookie_str=cookie_str)
            print(f"✅ 已下载 {humanize(n)} → {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"❌ 下载失败：{e}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
