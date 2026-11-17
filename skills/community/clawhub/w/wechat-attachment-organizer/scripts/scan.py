#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat 附件扫描器（合规版，绝不访问/解密聊天数据库）。

功能：
  - 自动探测 macOS 微信数据目录（兼容 3.x / 4.x）
  - 遍历文档 / 图片 / 视频附件，生成只读清单 manifest.json
  - 对微信的 .dat 容器做单字节 XOR 解码，还原真实文件类型
  - 计算 sha256，供后续去重与增量整理使用

仅做文件系统读取，不修改任何源文件，不触碰 MSGx.db。
"""
import os
import sys
import json
import hashlib
import argparse
import datetime

HOME = os.path.expanduser("~")
CONTAINER = os.path.join(HOME, "Library", "Containers", "com.tencent.xinWeChat", "Data")

# .dat 是原始文件与单字节密钥的 XOR。靠文件头 magic 反推密钥与真实类型。
DAT_MAGICS = [
    (b"\xff\xd8\xff", "jpg"),   # JPEG
    (b"\x89PNG", "png"),        # PNG
    (b"GIF8", "gif"),           # GIF
    (b"BM", "bmp"),             # BMP
    (b"%PDF", "pdf"),           # PDF
    (b"PK\x03\x04", "zip"),     # docx/xlsx 本质是 zip
]


def dat_key_and_ext(head):
    """head: 文件前若干字节。返回 (key, real_ext) 或 (None, None)。"""
    if not head:
        return None, None
    b0 = head[0]
    for magic, ext in DAT_MAGICS:
        key = b0 ^ magic[0]
        n = len(magic)
        if len(head) >= n and bytes(c ^ key for c in head[:n]) == magic:
            return key, ext
    # mp4: 前 4 字节常为 0x00 0x00 0x00 xx，随后是 'ftyp'（需先解码比对）
    key = b0 ^ 0x00
    dec = bytes(c ^ key for c in head[:12])
    if len(dec) >= 12 and dec[4:8] == b"ftyp":
        return key, "mp4"
    return None, None


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


def candidate_roots():
    """按当前平台返回待探测的根目录列表 [(root, 备注), ...]"""
    roots = []
    plat = sys.platform
    if plat == "darwin":
        c = os.path.expanduser("~/Library/Containers/com.tencent.xinWeChat/Data")
        roots.append((os.path.join(c, "Documents", "xwechat_files"), "macOS 4.x"))
        roots.append((os.path.join(c, "Application Support", "com.tencent.xinWeChat"), "macOS 3.x"))
    elif plat == "win32":
        prof = os.path.expandvars("%USERPROFILE%")
        docs = os.path.join(prof, "Documents")
        roots.append((os.path.join(docs, "xwechat_files"), "Windows 4.x"))
        roots.append((os.path.join(prof, "xwechat_files"), "Windows 4.x(少数安装)"))
        roots.append((os.path.join(docs, "WeChat Files"), "Windows 3.x"))
        roots.append((os.path.join(prof, "AppData", "Local", "Packages",
                     "TencentWeChatLimited.forWindows10_sdtnhv12zgd7a",
                     "LocalCache", "Roaming", "Tencent", "WeChatAppStore",
                     "WeChatAppStore Files"), "Windows UWP 3.x"))
    elif plat.startswith("linux"):
        home = os.path.expanduser("~")
        user = os.getenv("USER") or os.getenv("USERNAME") or "user"
        # 原生 4.x
        roots.append((os.path.join(home, "Documents", "xwechat_files"), "Linux 原生 4.x"))
        roots.append((os.path.join(home, ".xwechat", "xwechat_files"), "Linux 原生 4.x(~/.xwechat)"))
        roots.append((os.path.join(home, ".local", "share", "WeChat_Data", "Documents"), "Linux 原生 4.x(flatpak)"))
        roots.append((os.path.join(home, ".local", "share", "xwechat"), "Linux 原生 4.x"))
        # Wine / 深度 Wine（3.x 或 4.x）
        wine_base = os.path.join(home, ".wine", "drive_c", "users", user, "Documents")
        deepin_base = os.path.join(home, ".deepinwine", "Deepin-WeChat", "drive_c", "users", user, "Documents")
        roots.append((os.path.join(wine_base, "xwechat_files"), "Linux Wine 4.x"))
        roots.append((os.path.join(wine_base, "WeChat Files"), "Linux Wine 3.x"))
        roots.append((os.path.join(deepin_base, "xwechat_files"), "Linux 深度Wine 4.x"))
        roots.append((os.path.join(deepin_base, "WeChat Files"), "Linux 深度Wine 3.x"))
    return roots


def find_accounts_in(root):
    """在 root 下找账号目录。靠 msg/FileStorage 自动判 4.x/3.x，
    兼容 mac 3.x 的 'root/版本/账号' 嵌套结构。"""
    results = []
    if not os.path.isdir(root):
        return results
    try:
        names = sorted(os.listdir(root))
    except OSError:
        return results
    for name in names:
        p = os.path.join(root, name)
        if not os.path.isdir(p):
            continue
        if os.path.isdir(os.path.join(p, "msg")):
            results.append((name, "4.x", p))
        elif os.path.isdir(os.path.join(p, "FileStorage")):
            results.append((name, "3.x", p))
        else:
            # 可能是版本目录（mac 3.x 等）：再深一层找账号
            try:
                for sub in sorted(os.listdir(p)):
                    sp = os.path.join(p, sub)
                    if not os.path.isdir(sp):
                        continue
                    if os.path.isdir(os.path.join(sp, "msg")):
                        results.append((sub, "4.x", sp))
                    elif os.path.isdir(os.path.join(sp, "FileStorage")):
                        results.append((sub, "3.x", sp))
            except OSError:
                continue
    return results


def detect_accounts():
    """返回 [(account_name, version, account_path), ...]，跨平台去重。"""
    accounts = []
    seen = set()
    for root, _note in candidate_roots():
        for acc in find_accounts_in(root):
            if acc[2] not in seen:
                seen.add(acc[2])
                accounts.append(acc)
    return accounts


def source_dirs(account_path, version):
    """返回 [(abs_dir, raw_category), ...]，raw_category ∈ doc|image|video"""
    dirs = []
    if version == "4.x":
        msg = os.path.join(account_path, "msg")
        for sub, cat in (("file", "doc"), ("attach", "image"), ("video", "video")):
            p = os.path.join(msg, sub)
            if os.path.isdir(p):
                dirs.append((p, cat))
    else:
        fs = os.path.join(account_path, "FileStorage")
        for sub, cat in (("File", "doc"), ("Image", "image"), ("Video", "video")):
            p = os.path.join(fs, sub)
            if os.path.isdir(p):
                dirs.append((p, cat))
    return dirs


def human(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}" if unit != "B" else f"{n}B"
        n /= 1024
    return f"{n:.1f}PB"


def main():
    ap = argparse.ArgumentParser(description="Scan WeChat attachments into a manifest (no DB access).")
    ap.add_argument("--root", help="直接指定某个账号目录（跳过自动探测）")
    ap.add_argument("--out", default=os.path.join(os.getcwd(), "wxa_manifest.json"))
    ap.add_argument("--account-filter", default=None, help="只处理账号名包含该子串的账号")
    ap.add_argument("--no-hash", action="store_true",
                    help="跳过 sha256 计算（仅做分类/解码/体积统计，速度快；此模式下无法做内容去重）")
    ap.add_argument("--exclude", default=None,
                    help="跳过某些原始分类，逗号分隔：doc,image,video。例：--exclude image")
    ap.add_argument("--progress-every", type=int, default=1000, help="进度日志间隔（文件数）")
    args = ap.parse_args()
    exclude = set(x.strip().lower() for x in (args.exclude or "").split(",") if x.strip())

    if args.root:
        accounts = [("custom", "auto", os.path.abspath(args.root))]
    else:
        accounts = detect_accounts()
    if not accounts:
        print("ERROR: 未在当前平台自动探测到微信数据目录。", file=sys.stderr)
        print("已探测以下位置：", file=sys.stderr)
        for r, note in candidate_roots():
            print(f"  [{note}] {r}", file=sys.stderr)
        print("若微信装在非默认位置，请用 --root <账号目录> 直接指定。", file=sys.stderr)
        sys.exit(2)

    entries = []
    t0 = datetime.datetime.now()
    n_done = 0
    n_bytes = 0
    for acc, ver, apath in accounts:
        if args.account_filter and args.account_filter not in acc:
            continue
        if ver == "auto":
            ver = "4.x" if os.path.isdir(os.path.join(apath, "msg")) else "3.x"
        for d, cat in source_dirs(apath, ver):
            if cat in exclude:
                continue
            for root, _, files in os.walk(d):
                for fn in files:
                    fp = os.path.join(root, fn)
                    try:
                        st = os.stat(fp)
                    except OSError:
                        continue
                    if st.st_size == 0:
                        continue
                    head = open(fp, "rb").read(16)
                    ext = os.path.splitext(fn)[1].lower().lstrip(".")
                    dat_key = None
                    real_ext = ext
                    if ext == "dat":
                        key, rext = dat_key_and_ext(head)
                        if key is not None:
                            dat_key = key
                            real_ext = rext
                            cat = ("image" if rext in ("jpg", "png", "gif", "bmp")
                                   else "video" if rext == "mp4" else "doc")
                    sha = "" if args.no_hash else sha256_of(fp)
                    entries.append({
                        "src": fp,
                        "account": acc,
                        "wechat_version": ver,
                        "raw_category": cat,
                        "name": fn,
                        "ext": ext,
                        "real_ext": real_ext,
                        "dat_key": dat_key,
                        "size": st.st_size,
                        "mtime": st.st_mtime,
                        "sha256": sha,
                    })
                    n_done += 1
                    n_bytes += st.st_size
                    if args.progress_every and n_done % args.progress_every == 0:
                        dt = (datetime.datetime.now() - t0).total_seconds() or 1e-6
                        rate = n_bytes / dt
                        print(f"[progress] {n_done} 文件, {human(n_bytes)}, "
                              f"{rate/1024/1024:.1f} MB/s", file=sys.stderr)
    if args.progress_every:
        print(f"[progress] 完成扫描 {n_done} 文件, 共 {human(n_bytes)}", file=sys.stderr)

    manifest = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "platform": sys.platform,
        "hashed": not args.no_hash,
        "scan_roots": [r for r, _ in candidate_roots()],
        "count": len(entries),
        "entries": entries,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    from collections import Counter
    c = Counter(e["raw_category"] for e in entries)
    print(f"已扫描 {len(entries)} 个文件 -> {args.out}")
    print("分类统计：", dict(c))
    if any(e["dat_key"] is not None for e in entries):
        print("提示：部分 .dat 已解码还原真实类型（图片/视频/文档）。")


if __name__ == "__main__":
    main()
