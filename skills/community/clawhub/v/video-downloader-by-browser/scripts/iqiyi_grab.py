#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爱奇艺（含奇巴布儿童版）一键下载。

原理见 references/iqiyi.md，核心四步：
    1. baseinfo 接口拿 tvid / playUrl / payMark（判断是否需要会员）
    2. 无头浏览器打开播放页，从网络请求里截获正片 m3u8 与带签名的 ts CDN 地址
    3. 把 ts 的 start/end 改成整文件范围，一次性 curl 下载完整流
       （爱奇艺所有分片其实是同一个 ts 文件的不同字节区间；
        而 data.video.iqiyi.com 直连会 405，必须用浏览器拿到的带 key 签名的 CDN 地址）
    4. ffmpeg -c copy 无损转封装为 mp4，并校验时长是否吻合

用法:
    python iqiyi_grab.py "<爱奇艺视频页URL>" [输出.mp4]

依赖: playwright（pip install playwright && playwright install chromium）、curl、ffmpeg
注意: 免费内容（payMark=0）无需登录；若需会员/登录，脚本会提示并停止。
"""
import asyncio
import json
import os
import re
import subprocess
import sys
import urllib.parse as up
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
REF = "https://www.iqiyi.com/"


# ---------- 步骤 1：基础信息 ----------
def base_info(tvid):
    """调 baseinfo 接口拿 playUrl / 标题 / payMark。失败返回 None。"""
    url = f"https://pcw-api.iqiyi.com/video/video/baseinfo/{tvid}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": REF})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.loads(r.read().decode("utf-8", "ignore"))
        return d.get("data") or None
    except Exception as e:
        print(f"  [baseinfo] 失败：{str(e)[:80]}")
        return None


def tvid_from_url(u):
    """从分享页 URL 里提取 tv_id / tvid / album_id。"""
    q = up.parse_qs(up.urlparse(u).query)
    for k in ("tv_id", "tvid", "tvId", "album_id"):
        if k in q and q[k][0].isdigit():
            return q[k][0]
    return None


# ---------- 步骤 2：浏览器抓 m3u8 与带签名 ts ----------
async def grab_async(page_url, want_tvid=True):
    from playwright.async_api import async_playwright

    m3u8, ts_url, meta = [], {}, {}

    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox", "--disable-dev-shm-usage", "--mute-audio",
            "--autoplay-policy=no-user-gesture-required"])
        ctx = await b.new_context(user_agent=UA, viewport={"width": 1280, "height": 720})
        await ctx.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
        page = await ctx.new_page()

        async def on_resp(r):
            u = r.url
            if ".m3u8" in u and r.status == 200:
                m3u8.append(u)
            elif ".ts" in u and r.status == 200 and "start=" in u:
                ts_url.setdefault("u", u)          # 带 key 签名的真实 CDN 地址
            elif "playervideoinfo" in u and r.status == 200:
                m = re.search(r"[?&]id=(\d+)", u)
                if m:
                    meta["tvid"] = m.group(1)
                if want_tvid:
                    try:
                        meta["info"] = json.loads((await r.text())[:20000])
                    except Exception:
                        pass
            elif "accelerator.js" in u and r.status == 200:
                try:                                # 拿到 videoDuration 便于校验
                    t = await r.text()
                    m = re.search(r'"videoDuration":(\d+)', t)
                    if m:
                        meta["duration"] = int(m.group(1))
                except Exception:
                    pass

        page.on("response", lambda r: asyncio.create_task(on_resp(r)))
        await page.goto(page_url, wait_until="domcontentloaded", timeout=60000)

        # 加速播放，尽快把流请求都引出来
        for _ in range(30):
            await page.wait_for_timeout(2000)
            await page.evaluate("""() => {
                const v = document.querySelector('video');
                if (v) { v.muted = true; v.playbackRate = 8;
                         if (v.paused) v.play().catch(()=>{}); }
            }""")
            if m3u8 and ts_url:
                break
        await b.close()

    return (m3u8[0] if m3u8 else None), ts_url.get("u"), meta


# ---------- 步骤 3：下载整文件 ----------
def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": REF})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "ignore")


def parse_m3u8(text):
    """返回 (总字节, 分片数, 总时长秒)"""
    segs = [(int(a), int(b)) for a, b in re.findall(r"start=(\d+)&end=(\d+)", text)]
    segs.sort()
    dur = sum(float(x) for x in re.findall(r"#EXTINF:([0-9.]+)", text))
    if not segs:
        raise SystemExit("m3u8 里解析不到 start/end 分片，格式可能已变，请检查")
    return segs[-1][1], len(segs), dur


def download_full(ts_url, total, out_ts):
    """把 start/end 换成整文件范围，一次下载完整流。"""
    u = re.sub(r"start=\d+", "start=0", ts_url)
    u = re.sub(r"end=\d+", f"end={total - 1}", u)
    u = re.sub(r"contentlength=\d+", f"contentlength={total}", u)
    print(f"  下载整文件（{total / 1048576:.1f} MB）...")
    r = subprocess.run(
        ["curl", "-s", "-A", UA, "-e", REF, "-o", out_ts, "--max-time", "600",
         "-w", "%{http_code} %{size_download}", u],
        capture_output=True, text=True)
    code, size = (r.stdout.split() + ["0", "0"])[:2]
    if code != "200":
        raise SystemExit(f"下载失败 HTTP {code}（签名可能已过期或绑定区间，"
                         f"参考 references/iqiyi.md 的逐片回退方案）")
    print(f"  已下载 {int(size) / 1048576:.1f} MB")
    return int(size)


# ---------- 步骤 4：转封装 + 校验 ----------
def to_mp4(ts_path, out_mp4):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", ts_path,
                    "-c", "copy", "-movflags", "+faststart", out_mp4], check=True)


def probe(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,width,height",
         "-of", "default=noprint_wrappers=1", path],
        capture_output=True, text=True)
    d = r.stdout
    dur = float(re.search(r"duration=([\d.]+)", d).group(1)) if "duration=" in d else 0
    res = re.search(r"width=(\d+)[\s\S]*?height=(\d+)", d)
    wh = f"{res.group(1)}×{res.group(2)}" if res else "?"
    return dur, wh, "audio" in d


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    page_url = sys.argv[1]
    out_mp4 = sys.argv[2] if len(sys.argv) > 2 else "iqiyi_out.mp4"
    tmp = "/tmp/iqy_full.ts"

    print("步骤 1/4：解析视频信息")
    tvid = tvid_from_url(page_url)
    target = page_url
    if tvid:
        info = base_info(tvid)
        if info:
            print(f"  标题：{info.get('name', '?')[:60]}")
            if info.get("payMark"):
                raise SystemExit("该视频为付费/VIP 内容，需人工登录。"
                                 "按项目首选项，建议用户在“本地任务”模式下新建会话。")
            target = (info.get("playUrl") or page_url).replace("http://", "https://")
            print(f"  播放页：{target}")
    else:
        print("  URL 里没有 tvid，直接用浏览器打开原页面")

    print("步骤 2/4：无头浏览器抓取 m3u8 与签名 CDN 地址")
    m3u8_url, ts_url, meta = asyncio.run(grab_async(target))
    if not m3u8_url or not ts_url:
        raise SystemExit("未抓到 m3u8 或 ts 地址：可能需要登录/会员，"
                         "或页面结构已变，请用浏览器手动确认")
    print(f"  m3u8：{m3u8_url[:90]}...")

    print("步骤 3/4：解析分片并下载完整流")
    text = fetch_text(m3u8_url)
    total, nseg, mdur = parse_m3u8(text)
    print(f"  分片 {nseg} 个 / 声明时长 {mdur:.0f}s / 总字节 {total}")
    size = download_full(ts_url, total, tmp)

    print("步骤 4/4：转封装并校验")
    to_mp4(tmp, out_mp4)
    dur, wh, has_audio = probe(out_mp4)
    ok = abs(dur - mdur) < 2
    print(f"\n=== 完成 ===")
    print(f"文件：{out_mp4}  ({os.path.getsize(out_mp4) / 1048576:.1f} MB)")
    print(f"分辨率：{wh}   时长：{dur:.1f}s（声明 {mdur:.0f}s）{'✓ 吻合' if ok else '⚠ 偏差大，请检查'}")
    print(f"音轨：{'有' if has_audio else '无（需确认原视频是否本就无声）'}")
    os.path.exists(tmp) and os.remove(tmp)
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
