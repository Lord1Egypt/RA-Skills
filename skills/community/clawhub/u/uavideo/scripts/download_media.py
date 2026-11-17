#!/usr/bin/env python3
"""素材下载脚本：支持直链(mp4/m3u8等)与平台页面链接(封装 yt-dlp)。

用法:
    python3 download_media.py <URL|本地文件列表txt> [-o 输出目录]

行为:
- 直链: 直接下载; m3u8 自动用 ffmpeg 合并成 mp4。
- 平台页面链接(抖音/B站/小红书等): 调用 yt-dlp; 未安装时给出安装提示。
- 同名冲突自动追加序号, 不覆盖已有文件。
- 传 txt 文件时按行批量下载, # 开头为注释行。
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

PAGE_HOSTS = ("douyin.com", "iesdouyin.com", "bilibili.com", "b23.tv",
              "xiaohongshu.com", "xhslink.com", "kuaishou.com", "v.kuaishou.com")


def is_page_url(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return any(host.endswith(h) or host == h for h in PAGE_HOSTS)


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    i = 1
    while True:
        cand = path.with_name(f"{path.stem}_{i}{path.suffix}")
        if not cand.exists():
            return cand
        i += 1


def download_direct(url: str, out_dir: Path) -> Path:
    name = Path(urlparse(url).path).name or "media.mp4"
    # 去掉 query, 保留可读文件名
    name = name.split("?")[0] or "media.mp4"
    dest = unique_path(out_dir / name)
    tmp = dest.with_suffix(dest.suffix + ".part")
    cmd = ["curl", "-L", "--fail", "--retry", "3", "-o", str(tmp), url]
    subprocess.run(cmd, check=True)
    shutil.move(str(tmp), str(dest))
    return dest


def download_m3u8(url: str, out_dir: Path) -> Path:
    dest = unique_path(out_dir / "stream.mp4")
    tmp = dest.with_suffix(".part.mp4")
    cmd = ["ffmpeg", "-y", "-i", url, "-c", "copy", "-bsf:a", "aac_adtstoasc", str(tmp)]
    subprocess.run(cmd, check=True)
    shutil.move(str(tmp), str(dest))
    return dest


def download_page(url: str, out_dir: Path) -> Path:
    if not shutil.which("yt-dlp"):
        print("[提示] 平台页面链接需要 yt-dlp。安装: pip install -U yt-dlp", file=sys.stderr)
        print("[降级] 可改用浏览器工具捕获页面网络请求, 从视频CDN域名(douyinvod/bilivideo等)取直链后重试。",
              file=sys.stderr)
        sys.exit(2)
    dest_tpl = str(out_dir / "douyin_%(id)s_%(title).40s.%(ext)s")
    cmd = ["yt-dlp", "--no-playlist", "-o", dest_tpl, url]
    subprocess.run(cmd, check=True)
    # 找最新的文件
    files = sorted(out_dir.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else out_dir


def process_url(url: str, out_dir: Path) -> Path:
    url = url.strip()
    if not url or url.startswith("#"):
        return None
    print(f"==> {url}")
    path_lower = urlparse(url).path.lower()
    if is_page_url(url):
        return download_page(url, out_dir)
    if ".m3u8" in path_lower:
        return download_m3u8(url, out_dir)
    return download_direct(url, out_dir)


def main():
    ap = argparse.ArgumentParser(description="素材下载: 直链/平台页面链接")
    ap.add_argument("source", help="URL 或包含 URL 列表的 txt 文件")
    ap.add_argument("-o", "--out", default=".", help="输出目录(默认当前目录)")
    args = ap.parse_args()

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    src = Path(args.source).expanduser()
    urls = src.read_text(encoding="utf-8").splitlines() if src.suffix == ".txt" and src.exists() else [args.source]

    ok, fail = 0, 0
    for u in urls:
        try:
            p = process_url(u, out_dir)
            if p:
                print(f"[完成] {p}  ({p.stat().st_size / 1e6:.1f} MB)")
                ok += 1
        except subprocess.CalledProcessError as e:
            print(f"[失败] {u}: exit={e.returncode}", file=sys.stderr)
            fail += 1
        except Exception as e:
            print(f"[失败] {u}: {e}", file=sys.stderr)
            fail += 1
    print(f"\n汇总: 成功 {ok}, 失败 {fail}")
    sys.exit(1 if fail and not ok else 0)


if __name__ == "__main__":
    main()
