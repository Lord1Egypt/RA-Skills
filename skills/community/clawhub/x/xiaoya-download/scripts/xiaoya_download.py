#!/usr/bin/env python3
"""
XiaoyaDownload — 小雅影音下载器

搜索小雅/Alist 电影/剧集并通过本地 WebDAV 挂载复制下载。

Usage:
    python3 xiaoya_download.py setup                  # 配置检查
    python3 xiaoya_download.py search <keyword>       # 搜索影视
    python3 xiaoya_download.py copy <remote_path>     # WebDAV 复制到本地
"""

import os, sys, json, time, re, urllib.parse, subprocess
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ 需要 requests 库。安装: pip3 install requests")
    sys.exit(1)

VIDEO_EXTS = {".mp4",".mkv",".avi",".mov",".wmv",".flv",".webm",".m4v",
              ".ts",".iso",".bdmv",".m2ts",".rmvb",".3gp"}


def load_env():
    env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.isfile(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("\"'"))
    return {
        "XIAOYA_HOST": os.environ.get("XIAOYA_HOST", ""),
        "DOWNLOAD_DIR": os.environ.get("DOWNLOAD_DIR", ""),
        "WEBDAV_MOUNT": os.environ.get("WEBDAV_MOUNT", ""),
    }


def fmt_size(s):
    if not s: return "?"
    for u in ["B","KB","MB","GB","TB"]:
        if s < 1024: return f"{s:.1f} {u}"
        s /= 1024
    return f"{s:.1f} PB"


# ── 搜索 ──────────────────────────────────────────────────────────

def _validate_host(host):
    if not host or not host.startswith(("http://", "https://")):
        raise ValueError(f"XIAOYA_HOST 格式无效: {host}")
    return host

def cmd_search(keyword, search_type="video"):
    """通过小雅网页搜索接口搜索"""
    config = load_env()
    host = _validate_host(config.get("XIAOYA_HOST", ""))

    params = urllib.parse.urlencode({"box": keyword, "url": "", "type": search_type})
    url = f"{host}/search?{params}"

    print(f"🔍 正在搜索「{keyword}」...")

    try:
        resp = requests.get(url, timeout=60)
        html = resp.text

        pattern = re.compile(r'<a href=([^>]+)>([^<]+)</a>')
        results = []
        seen = set()
        for m in pattern.finditer(html):
            path = m.group(1).strip()
            name = m.group(2).strip()
            if path.startswith("/") and not path.startswith("//") and path not in seen:
                seen.add(path)
                results.append((name, path))

        if not results:
            print("  ℹ️  没有找到相关内容")
            return

        items = []
        for i, (name, path) in enumerate(results[:50], 1):
            ext = os.path.splitext(name)[1].lower()
            items.append({"idx": i, "name": name, "path": path, "is_dir": ext not in VIDEO_EXTS})

        # 画质/编码提取
        def get_tags(n):
            t = []
            for kw in ["4K","2160p","1080p","720p","UHD","REMUX","原盘","BluRay",
                       "HEVC","x265","x264","Dolby Vision","DoVi","HDR",
                       "Atmos","TrueHD","DTS-HD","DTS","AC3","AAC",
                       "国配","国语","中字","简繁"]:
                if kw in n: t.append(kw)
            return " ".join(t[:5]) if t else "-"
        
        def get_size(n):
            m = re.search(r'[\d.]+[GT]B', n)
            return m.group() if m else "-"
        
        def short_fname(n):
            f = n.split('/')[-1]
            return f[:32] + ".." if len(f) > 32 else f

        print(f"\n📋 搜索结果：共 {len(items)} 个\n")
        print("  ┌───┬──────────────────────────────────┬──────────────────────┬───────┐")
        print("  │ # │ 文件                               │ 画质·编码              │ 大小  │")
        print("  ├───┼──────────────────────────────────┼──────────────────────┼───────┤")
        for item in items[:30]:
            fname = item['name']
            icon = "🎬" if not item['is_dir'] else "📁"
            name_pad = f"{icon} {short_fname(fname):30s}"
            tags = get_tags(fname)
            sz = get_size(fname)
            print(f"  │ {item['idx']:>2d} │ {name_pad:<35s} │ {tags:<20s} │ {sz:<5s} │")
        print("  └───┴──────────────────────────────────┴──────────────────────┴───────┘")

        print("\n---JSON---")
        print(json.dumps(items, ensure_ascii=False))
        print("---END---")
    except Exception as e:
        print(f"  ❌ 搜索失败: {e}")


# ── WebDAV 复制 ──────────────────────────────────────────────────

def cmd_copy(remote_path):
    """通过本地 WebDAV 挂载复制文件/目录"""
    config = load_env()
    webdav_root = config.get("WEBDAV_MOUNT", "")
    dl_dir = config.get("DOWNLOAD_DIR", "/tmp")

    if not webdav_root or not os.path.isdir(webdav_root):
        print("  ❌ WebDAV 挂载路径未配置或不存在")
        print("  请在 .env 中设置 WEBDAV_MOUNT")
        return

    if not dl_dir:
        print("  ❌ 下载目录未配置")
        return

    # ── 路径安全检查（层层设防）────────────────────────────────────

    # Step 1: 拒绝 null byte（防止 C 层级截断攻击）
    if "\0" in remote_path:
        print(f"  ❌ 无效路径：包含 null byte")
        return

    # Step 2: URL 解码（必须在路径拼接之前完成）
    decoded_path = urllib.parse.unquote(remote_path.lstrip("/"))

    # Step 3: 显式拒绝包含 '..' 的路径（realpath 兜底前再加一道防线）
    if ".." in decoded_path.split("/"):
        print(f"  ❌ 路径穿越检测：拒绝包含 '..' 的路径")
        print(f"     请求路径: {remote_path}")
        return

    # Step 4: 拼接并解析为绝对路径
    joined = os.path.join(webdav_root, decoded_path)
    resolved = os.path.realpath(joined)

    # Step 5: 用 pathlib.relative_to() 做严格的 containment 检查
    # 若 resolved 不在 webdav_root_real 内部，relative_to() 会抛 ValueError
    webdav_root_real = os.path.realpath(webdav_root)
    try:
        Path(resolved).relative_to(Path(webdav_root_real).resolve())
    except ValueError:
        print(f"  ❌ 路径越界检测：路径不在 WebDAV 挂载目录内")
        print(f"     请求路径: {remote_path}")
        print(f"     解析结果: {resolved}")
        return

    webdav_path = resolved

    if not os.path.exists(webdav_path):
        print(f"  ❌ WebDAV 路径不存在")
        print(f"     {webdav_path}")
        return

    name = Path(decoded_path).name
    dst = os.path.join(dl_dir, name)

    # ── rsync 调用（路径已 100% 验证，直接用 abspath，不走 shell）────
    if os.path.isdir(webdav_path):
        dst_dir = os.path.join(dl_dir, name)
        print(f"  📁 复制目录: {webdav_path} → {dst_dir}")
        cmd = ["rsync", "-av", "--progress",
               os.path.join(webdav_path, ""),   # trailing / 表示目录内容
               os.path.join(dst_dir, "")]
    else:
        print(f"  📁 复制文件: {webdav_path} → {dst}")
        cmd = ["rsync", "--progress", "--partial", "-av",
               webdav_path,
               dst]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
        if result.returncode == 0:
            final = os.path.getsize(dst) if os.path.isfile(dst) else 0
            print(f"\n  ✅ 复制完成: {fmt_size(final)}")
            print(f"     {dst}")
            return True
        else:
            print(f"  ❌ 复制失败: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ❌ 复制超时（文件过大）")
        return False
    except Exception as e:
        print(f"  ❌ 复制异常: {e}")
        return False


# ── 配置检查 ──────────────────────────────────────────────────────

def cmd_setup():
    print("=" * 50)
    print("  🎬 XiaoyaDownload — 小雅影音下载器")
    print("  " + "=" * 50 + "\n")

    config = load_env()
    host, dl_dir, webdav = config["XIAOYA_HOST"], config["DOWNLOAD_DIR"], config["WEBDAV_MOUNT"]

    missing = []
    if not host: missing.append("XIAOYA_HOST（小雅/Alist 网页地址）")
    if not dl_dir: missing.append("DOWNLOAD_DIR（下载目录）")

    if missing:
        print("❌ 以下配置缺失：")
        for m in missing: print(f"   • {m}")
        print()
        print("请编辑 skills/XiaoyaDownload/.env 文件填入配置。")
        return False

    print("✅ 配置检查通过")
    print(f"   🌐 小雅地址: {host}")
    print(f"   📥 下载目录: {dl_dir}")
    if webdav:
        if os.path.isdir(webdav):
            print(f"   📂 WebDAV挂载: {webdav} ✅")
        else:
            print(f"   ⚠️  WebDAV挂载: {webdav} ❌ 路径不存在")
    else:
        print(f"   📂 WebDAV: 未配置（复制下载不可用）")
    print()

    # 测试搜索接口
    print("🔌 正在测试搜索接口...")
    try:
        resp = requests.get(f"{host}/search?box=测试&type=video", timeout=10)
        if resp.status_code == 200 and "小雅的alist搜索引擎" in resp.text:
            print("   ✅ 搜索接口正常")
        else:
            print(f"   ⚠️  搜索接口返回异常 (HTTP {resp.status_code})")
    except Exception as e:
        print(f"   ❌ 无法连接: {e}")
        return False

    print()
    print("✅ 全部就绪！使用方法：")
    print("   python3 xiaoya_download.py search \"电影名\"")
    print("   python3 xiaoya_download.py copy \"/电影/...路径\"")
    return True


def main():
    import argparse
    p = argparse.ArgumentParser(description="小雅影音下载器")
    s = p.add_subparsers(dest="cmd")
    s.add_parser("setup")
    ps = s.add_parser("search")
    ps.add_argument("keyword")
    ps.add_argument("--type", default="video", choices=["video","music","ebook","all"])
    pc = s.add_parser("copy")
    pc.add_argument("remote_path", help="Alist 远程路径")
    args = p.parse_args()
    if args.cmd == "setup": cmd_setup()
    elif args.cmd == "search": cmd_search(args.keyword, args.type)
    elif args.cmd == "copy": cmd_copy(args.remote_path)
    else: p.print_help()

if __name__ == "__main__":
    main()
