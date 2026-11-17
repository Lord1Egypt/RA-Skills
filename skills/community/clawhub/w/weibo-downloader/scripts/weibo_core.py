# -*- coding: utf-8 -*-
"""
微博媒体下载器 - 核心模块
纯 Python + requests，无外部依赖。

下载原理：
  1. 提取微博链接中的 status_id
  2. 从 ~/.storage/weibo_cookies.pkl 加载 SUB/SUBP cookie
  3. 失效/不存在时自动走访客系统获取（一年有效）
  4. 请求 weibo.com/ajax/statuses/show 获取图文/视频 JSON
  5. 提取图片大图 URL + 视频直链并下载

支持链接格式：
  - https://weibo.com/USER/STATUS_ID
  - https://m.weibo.cn/status/STATUS_ID
  - https://mapp.api.weibo.cn/fx/UUID.html
"""

import os
import re
import json
import pickle
import requests


COOKIE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "storage", "weibo_cookies.pkl"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/116.0.0.0 Mobile Safari/537.36"
    ),
    "Referer": "https://weibo.com/",
}


def _save_cookies(session):
    """保存 SUB/SUBP cookie 到文件"""
    os.makedirs(os.path.dirname(COOKIE_FILE), exist_ok=True)
    cookies = {}
    for name in ("SUB", "SUBP"):
        if name in session.cookies:
            c = session.cookies[name]
            cookies[name] = {
                "value": c,
                "domain": session.cookies.list_domains(),
            }
    # 保存完整 cookie jar
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(session.cookies, f)
    print(f"[+] cookie 已保存到 {COOKIE_FILE}")


def _load_cookies(session):
    """从文件加载 cookie"""
    if not os.path.exists(COOKIE_FILE):
        return False
    try:
        with open(COOKIE_FILE, "rb") as f:
            jar = pickle.load(f)
        session.cookies.update(jar)
        # 检查 SUB 是否还在有效期内
        if "SUB" in session.cookies:
            print("[+] 从文件加载了微博 cookie ✅")
            return True
    except Exception:
        pass
    return False


def _get_visitor_cookies(session):
    """
    绕过新浪访客系统，获取 SUB/SUBP cookie
    SUB/SUBP 有效期为 365 天
    """
    print("[*] 正在获取访客 cookie...")

    # Step 1: 获取访客凭证
    r = session.post(
        "https://passport.weibo.com/visitor/genvisitor2",
        data={
            "cb": "visitor_gray_callback",
            "ver": "20250916",
            "tid": "",
            "from": "weibo",
            "webdriver": "false",
            "return_url": "https://weibo.com/",
        },
        headers={"Referer": "https://weibo.com/"},
    )
    m = re.search(r'\((.*?)\);\s*$', r.text)
    if not m:
        print("[!] 访客系统绕过失败: 无法解析 genvisitor2 响应")
        return False

    vd = json.loads(m.group(1)).get("data", {})
    if not vd.get("tid"):
        print("[!] 访客系统绕过失败: 未获取到 tid")
        return False

    # Step 2: 用 tid 换取 SUB/SUBP cookie
    session.get(
        "https://passport.weibo.com/visitor/visitor",
        params={
            "a": "crossdomain",
            "t": vd["tid"],
            "sp": vd["subp"],
            "s": vd["sub"],
            "from": "weibo",
            "_rand": str(hash(str(vd)))[:8],
            "url": "https://weibo.com/",
        },
        allow_redirects=False,
    )

    if "SUB" in session.cookies:
        print("[+] 访客 cookie 获取成功 ✅ (有效期 ~365 天)")
        _save_cookies(session)
        return True
    else:
        print("[!] 获取 cookie 失败")
        return False


def _ensure_cookies(session):
    """确保 session 有有效的微博 cookie"""
    if "SUB" in session.cookies and "SUBP" in session.cookies:
        return True
    if _load_cookies(session):
        return True
    return _get_visitor_cookies(session)


def resolve_fx_url(url, session=None):
    """解析 mapp.api.weibo.cn/fx/ 分享链接为真实微博链接"""
    s = session or requests.Session()
    try:
        # 不跟进重定向，直接看 location
        r = s.get(url, headers=HEADERS, allow_redirects=False, timeout=10)
        if r.status_code in (301, 302) and "location" in r.headers:
            real_url = r.headers["location"]
            print(f"  🔗 分享链接 → {real_url}")
            return real_url
        # 如果没重定向，降到 HTML 里找 return_url
        r = s.get(url, headers=HEADERS, timeout=10)
        m = re.search(r'return_url\s*=\s*"([^"]+)"', r.text)
        if m:
            print(f"  🔗 分享链接 → {m.group(1)}")
            return m.group(1)
        return url
    except Exception as e:
        print(f"[!] 解析分享链接失败: {e}")
        return url


def extract_status_id(url):
    """从微博链接中提取 status_id"""
    patterns = [
        r'weibo\.com/\d+/([a-zA-Z0-9]+)',
        r'weibo\.(?:com|cn)/detail/(\d+)',
        r'm\.weibo\.cn/(?:status|detail)/(\d+)',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


def _safe_name(text, max_len=30):
    """去除非法字符、截断"""
    text = re.sub(r'[\\/*?:"<>|\r\n\t]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_len]


def fetch_status(session, status_id):
    """
    获取单条微博的媒体数据
    返回: {"success": bool, "author": str, "text": str, "files": [...]}
    """
    r = session.get(
        f"https://weibo.com/ajax/statuses/show?id={status_id}&isGetLongText=true",
        headers=HEADERS,
        timeout=15,
    )

    if not r.text:
        return {"success": False, "error": "API 返回为空"}

    try:
        data = r.json()
    except json.JSONDecodeError:
        return {"success": False, "error": "API 返回非 JSON"}

    if data.get("ok") != 1:
        return {"success": False, "error": data.get("msg") or data.get("message") or "未知错误"}

    user = data.get("user", {})
    author = user.get("screen_name", "未知")
    text_raw = data.get("text_raw", "")
    prefix = _safe_name(text_raw or author, 20)

    # ---- 解析媒体 ----
    files = []

    # 新版 mix_media_info
    mix = data.get("mix_media_info")
    if mix:
        for item in mix.get("items", []):
            t = item.get("type")
            d = item.get("data", {})
            if t == "pic":
                url = d.get("largest", {}).get("url", "")
                if url:
                    files.append({"url": url, "type": "image"})
            elif t == "video":
                mi = d.get("media_info", {})
                url = mi.get("mp4_hd_url") or mi.get("mp4_720p_mp4") or mi.get("stream_url") or ""
                if url:
                    files.append({"url": url, "type": "video"})

    # 旧版 pic_ids + pic_infos（兜底）
    if not files:
        for pic_id in data.get("pic_ids", []):
            pic = data.get("pic_infos", {}).get(pic_id, {})
            if pic.get("type") == "gif" and pic.get("video"):
                files.append({"url": pic["video"], "type": "video"})
            else:
                url = pic.get("largest", {}).get("url", "")
                if url:
                    files.append({"url": url, "type": "image"})

    # 独立的 page_info 视频
    pi = data.get("page_info", {})
    if pi.get("type") == "video":
        mi = pi.get("media_info", {})
        url = mi.get("mp4_hd_url") or mi.get("mp4_720p_mp4") or mi.get("stream_url") or ""
        if url and not any(f["url"] == url for f in files):
            files.append({"url": url, "type": "video"})

    # 编号文件名
    for i, f in enumerate(files, 1):
        ext = "mp4" if f["type"] == "video" else "jpg"
        f["filename"] = f"{prefix}_{i:02d}.{ext}"

    return {
        "success": True,
        "author": author,
        "text": text_raw,
        "id": status_id,
        "files": files,
    }


def download_file(session, url, filepath):
    """下载单个文件"""
    try:
        print(f"  ⬇ {os.path.basename(filepath)}", end=" ", flush=True)
        r = session.get(url, headers=HEADERS, stream=True, timeout=60)
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = downloaded / total * 100
                        print(f"\r  ⬇ {os.path.basename(filepath)} [{pct:.0f}%]", end="", flush=True)
        size_kb = downloaded / 1024
        print(f"\r  ✅ {os.path.basename(filepath)} ({size_kb:.0f} KB)")
        return True
    except Exception as e:
        print(f"\r  ❌ {os.path.basename(filepath)}: {e}")
        return False


class WeiboDownloader:
    """微博媒体下载器"""

    def download(self, url, output_dir=None):
        """
        主入口：下载微博媒体
        返回: {"success": bool, "files": int, "total": int, "dir": str}
        """
        if output_dir is None:
            output_dir = os.getcwd()
        os.makedirs(output_dir, exist_ok=True)

        session = requests.Session()
        session.headers.update(HEADERS)

        original_url = url

        # 处理 fx 分享链接
        if "mapp.api.weibo.cn/fx/" in url:
            url = resolve_fx_url(url, session)

        # 提取 status_id
        status_id = extract_status_id(url)
        if not status_id:
            print(f"[!] 无法提取微博 ID: {original_url}")
            return {"success": False, "error": "无效的微博链接"}

        print(f"[+] 平台: 微博")
        print(f"[+] Status ID: {status_id}")

        # 确保有 cookie
        if not _ensure_cookies(session):
            print("[!] 无法获取微博访问凭证")
            return {"success": False, "error": "cookie 获取失败"}

        # 获取微博数据
        result = fetch_status(session, status_id)
        if not result["success"]:
            print(f"[!] 获取微博失败: {result.get('error')}")
            return result

        print(f"[+] 作者: {result['author']}")
        text_preview = result['text'][:50].replace('\n', ' ')
        print(f"[+] 内容: {text_preview}{'...' if len(result['text'])>50 else ''}")

        files = result["files"]
        if not files:
            print("[!] 未找到可下载的媒体文件")
            return {"success": False, "files": 0, "total": 0, "dir": output_dir}

        img_n = sum(1 for f in files if f['type'] == 'image')
        vid_n = sum(1 for f in files if f['type'] == 'video')
        print(f"[+] 共 {len(files)} 个文件 ({img_n} 图, {vid_n} 视频)")

        # 子目录
        author_dir = _safe_name(result["author"], 20)
        save_dir = os.path.join(output_dir, f"{author_dir}_{status_id}")
        os.makedirs(save_dir, exist_ok=True)

        # 下载
        success = sum(1 for f in files if download_file(session, f["url"],
                      os.path.join(save_dir, f["filename"])))

        print(f"\n[OK] 全部完成！成功 {success}/{len(files)}")
        print(f"📂 {save_dir}")
        return {"success": success > 0, "files": success, "total": len(files), "dir": save_dir}


def download(url, output_dir=None):
    """便捷函数：一键下载"""
    return WeiboDownloader().download(url, output_dir)
