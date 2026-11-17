# -*- coding: utf-8 -*-
"""
双色球报告「真实图片」抓取器（一次性抓取 + 本地缓存）。

设计原则（诚实 / 合规 / fail-safe）：
1. 只从「互联网公开检索结果」取图，绝不伪造"某故事中奖人"身份。
2. 图片落盘后由报告带来源署名 + 免责声明：
   "图片来自互联网公开检索结果，仅作示意，非本故事当事人，版权归原作者所有"。
3. 任何失败都静默回退——报告永远不会因为取图失败而崩溃，
   取不到真实图时由 ssq_auto 自动改用已缓存的 AI 氛围插画。
4. 抓取是「一次性」的：缓存目录非空即跳过网络请求，后续运行零耗时。

仅用于增强报告阅读趣味，不构成任何中奖暗示。理性娱乐，量力而行。
"""

import os
import re
import json
import time
import base64
import urllib.request
import urllib.parse
import urllib.error

# 真实图片缓存目录（与 AI 插画 win_illustrations 分开，互不影响）
_PHOTO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "win_photos")
_MANIFEST = os.path.join(_PHOTO_DIR, "manifest.json")

# 检索词：偏向"彩票 / 中奖 / 领奖 / 摇奖"等公开场景图，而非锁定具体个人
_QUERIES = [
    "双色球 中奖 领奖",
    "彩票 大奖 兑奖",
    "福利彩票 开奖 摇奖机",
    " lottery winner celebration",
]

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
_HEADERS = {"User-Agent": _UA, "Referer": "https://image.baidu.com/"}

_MAX_BYTES = 1_200_000  # 单图上限 ~1.2MB，避免超大图拖累报告
_MAX_PHOTOS = 4         # 最多缓存 4 张，轮转使用


def _search_image_urls(query, timeout=12, max_urls=12):
    """从百度图片检索页解析真实图片地址（best-effort）。"""
    urls = []
    try:
        word = urllib.parse.quote(query)
        url = ("https://image.baidu.com/search/index?tn=baiduimage&ipn=rj&ct=201326592"
               "&cl=2&lm=-1&ie=utf-8&oe=utf-8&word=" + word + "&pn=0&rn=30")
        req = urllib.request.Request(url, headers=_HEADERS)
        html = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "ignore")
        # 百度图片页用 data-imgurl / data-objurl 携带原图地址
        found = re.findall(r'data-(?:imgurl|objurl)="(http[^"]+)"', html)
        seen = set()
        for u in found:
            if u in seen:
                continue
            seen.add(u)
            urls.append(u)
            if len(urls) >= max_urls:
                break
    except Exception:
        pass
    return urls


def _download_one(src_url, dest_path, timeout=12):
    """下载单张图片到 dest_path；失败返回 False。"""
    try:
        req = urllib.request.Request(src_url, headers=_HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read(_MAX_BYTES + 1)
        if len(data) > _MAX_BYTES:
            return False
        # 极简类型判断：以常见图片魔数开头
        if data[:8] not in (b"\x89PNG\r\n\x1a\n",) and data[:3] != b"\xff\xd8\xff" \
           and not data[:4] in (b"GIF8",) and not data[:4] == b"RIFF":
            # WebP: RIFF....WEBP
            if not (data[:4] == b"RIFF" and data[8:12] == b"WEBP"):
                return False
        with open(dest_path, "wb") as f:
            f.write(data)
        return True
    except Exception:
        return False


def collect_real_photos(max_n=_MAX_PHOTOS, timeout=12, max_urls=12, offline=True):
    """
    抓取真实彩票相关图片到本地缓存（仅用于增强阅读趣味，不构成中奖暗示）。

    ⚠️ 关键：默认 offline=True —— 只读本地缓存，绝不联网。
    报告生成路径必须 百分之百 不联网，否则在真实网络下（慢 DNS / 握手挂起）会阻塞数分钟，
    表现为"任务卡死 / 停止工作"。真实图片的联网刷新由独立的、带硬超时的维护步骤完成
    （见本模块 __main__，由 ssq_auto 以非阻塞后台子进程触发），不影响报告产出。

    offline=False（仅维护步骤调用）：联网抓取，但全程受 socket 默认超时熔断，
    且单会话总查询数受限，绝不会无限期阻塞。
    """
    try:
        os.makedirs(_PHOTO_DIR, exist_ok=True)
        # 读缓存：清单存在且至少有 1 张有效图即复用
        if os.path.exists(_MANIFEST):
            try:
                with open(_MANIFEST, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                paths = [os.path.join(_PHOTO_DIR, m["file"]) for m in manifest
                         if os.path.exists(os.path.join(_PHOTO_DIR, m["file"]))]
                if paths:
                    return paths
            except Exception:
                pass
        # offline 模式：无缓存就直接空手返回（报告回退到 AI 插画，零阻塞）
        if offline:
            return []
        # ---- 以下为联网刷新（仅维护步骤，受全局 socket 超时保护）----
        import socket
        old_to = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)   # 覆盖 DNS/握手/读取，杜绝挂起
        try:
            collected = []
            used_queries = []
            # 限制总查询数，避免最坏情况下多 query 累积超时
            for q in _QUERIES[:2]:
                if len(collected) >= max_n:
                    break
                urls = _search_image_urls(q, timeout=timeout, max_urls=max_urls)
                for u in urls:
                    if len(collected) >= max_n:
                        break
                    ext = ".jpg"
                    m = re.search(r"\.(png|jpe?g|webp)", u, re.I)
                    if m:
                        ext = "." + m.group(1).lower()
                    dest = os.path.join(_PHOTO_DIR, f"real_{len(collected)+1}{ext}")
                    if _download_one(u, dest, timeout=timeout):
                        collected.append(dest)
                        used_queries.append({"file": os.path.basename(dest),
                                             "source": u, "query": q})
            if collected:
                with open(_MANIFEST, "w", encoding="utf-8") as f:
                    json.dump(used_queries, f, ensure_ascii=False, indent=2)
            else:
                # 抓取失败也写空清单，避免每次报告都重复联网重试
                try:
                    with open(_MANIFEST, "w", encoding="utf-8") as f:
                        json.dump([], f)
                except Exception:
                    pass
            return collected
        finally:
            socket.setdefaulttimeout(old_to)
    except Exception:
        return []


def load_real_photos_b64(offline=True):
    """读取缓存的真实图片，返回 [(b64_data_uri, source_url), ...]。

    默认 offline=True：只读缓存，绝不触发联网。报告路径务必用默认值。
    """
    out = []
    try:
        paths = collect_real_photos(offline=offline)  # 默认只读缓存
        for p in paths:
            try:
                with open(p, "rb") as f:
                    b = f.read()
                ext = p.rsplit(".", 1)[-1].lower()
                mime = {"png": "image/png", "jpg": "image/jpeg",
                        "jpeg": "image/jpeg", "webp": "image/webp"}.get(ext, "image/jpeg")
                out.append((f"data:{mime};base64,{base64.b64encode(b).decode('ascii')}", ""))
            except Exception:
                continue
    except Exception:
        pass
    return out


if __name__ == "__main__":
    # 显式刷新入口：必须 offline=False 才会真正联网抓取（受 socket 超时熔断）。
    # 注意：报告路径调用的是 collect_real_photos(offline=True) 只读缓存，绝不联网。
    t0 = time.time()
    got = collect_real_photos(offline=False)
    print(f"已缓存真实图片 {len(got)} 张，耗时 {time.time()-t0:.1f}s")
    for g in got:
        print("  ", g)
