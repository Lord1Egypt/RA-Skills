#!/usr/bin/env python3
"""
organize_attachments.py — 把微信附件按联系人/月份/类型整理到输出目录
用法：
    python organize_attachments.py --src "<msg目录>" --dst "<输出目录>" --contact <标签>
    python organize_attachments.py --src "<msg目录>" --dst "<输出目录>" --contact <标签> --decrypt

参数：
    --src       源目录（递归遍历，只读）
    --dst       输出目录
    --contact   联系人/来源标签（只写进日志与 README）
    --copy      复制（默认移动）
    --decrypt   解密 .dat 后再归档；不加则只列清单（原行为不变）
    --code      已知 code（8~10 位），配合 --decrypt 跳过暴力推导
    --wxid      wxid 候选，配合 --decrypt，可重复
    --key-file  含 code/wxid 的 JSON（例如 wechat_dat_decrypt.py 写出的 secret_hit.json）
    --account   账号根目录（缺省时自动向上探测）
    --decrypt-timeout  暴力推导超时秒数（默认 300）
"""
import argparse
import csv
import hashlib
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


TYPE_MAP = {
    "01-documents": {".docx", ".doc", ".pdf", ".xlsx", ".xls", ".pptx",
                     ".ppt", ".txt", ".md", ".csv", ".rtf", ".wps"},
    "02-images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".heic",
                  ".webp", ".tif", ".tiff"},
    "03-videos": {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"},
    "04-voice": {".silk", ".amr", ".mp3", ".wav", ".m4a"},
}

# 微信 4.x 的 .dat 是图片混淆格式：不加 --decrypt 时只列清单，加了才解密归档
SKIP_EXTS = {".dat"}


def classify(ext: str) -> str:
    ext = ext.lower()
    for folder, exts in TYPE_MAP.items():
        if ext in exts:
            return folder
    return "05-misc"


def sha256_of(path: Path, buf=65536) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            data = f.read(buf)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def find_account_root(src: Path) -> Path:
    """从 src 向上找账号根目录（含 msg/ 或 db_storage/ 的那一层），找不到就用 src。"""
    for p in [src, *src.parents]:
        if (p / "msg").is_dir() or (p / "db_storage").is_dir():
            return p
    return src


def load_decryptor(args, src: Path):
    """返回 (decrypt_fn, key, xor) 或 (None, None, None)；失败时已打印原因。"""
    here = Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    try:
        import wechat_dat_decrypt as wdd
    except ImportError as exc:
        print(f"[!] 找不到 wechat_dat_decrypt.py（{exc}），无法 --decrypt")
        return None, None, None

    code = wxid = None
    if args.key_file:
        try:
            hit = json.loads(Path(args.key_file).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"[!] 读取 --key-file 失败: {exc}")
            return None, None, None
        code, wxid = hit.get("code"), hit.get("wxid")
    if args.code:
        code = args.code

    account = Path(args.account).expanduser() if args.account else find_account_root(src)
    if not account.is_dir():
        print(f"[!] 账号目录不存在: {account}")
        return None, None, None

    files, blocks = wdd.collect_probe_blocks(account)
    if not blocks:
        print("[!] 找不到可用的 .dat 探针，无法 --decrypt")
        return None, None, None

    xor = wdd.infer_xor(files)[0]

    if code is not None:
        wxids = wdd.discover_wxids(account, list(args.wxid or []) + ([wxid] if wxid else []))
        for w in wxids:
            if wdd.verify_key(code, w, blocks):
                wxid = w
                break
        else:
            print("[!] code 对不上任何 wxid 候选，请补 --wxid 或检查 --key-file")
            return None, None, None
        print(f"[*] 使用已知 code（跳过暴力），wxid 候选 {len(wxids)} 个已校验")
        status = "provided"
        elapsed = 0.0
    else:
        wxids = wdd.discover_wxids(account, list(args.wxid or []))
        if not wxids:
            print("[!] 没有 wxid 候选，请用 --wxid 指定")
            return None, None, None
        if xor is None:
            print("[!] 尾字节反推 xor 失败，请提供 --code / --key-file")
            return None, None, None
        print(f"[*] 自动推导 code：探针 {len(files)}，wxid 候选 {len(wxids)}，"
              f"超时 {args.decrypt_timeout}s")
        import os as _os
        wdd._VERIFY_PATHS = files
        ncpu = args.procs or max(1, (_os.cpu_count() or 4) - 1)
        code, wxid, status, elapsed = wdd.brute_code(
            blocks, wxids, Path(args.dst), args.decrypt_timeout, ncpu, xor)
        if code is None:
            print(f"[!] 暴力推导未命中（{status}），可改用 --code / --key-file 直接给")
            return None, None, None
        print(f"[*] 推导命中，耗时 {elapsed}s")

    key = wdd.derive_key(code, wxid)
    if xor is None:
        xor = int(code) & 0xFF
    # 命中的 code 只落在 --dst（用户指定输出目录），不写进技能包目录
    try:
        hit_path = Path(args.dst) / "00-index" / "secret_hit.json"
        hit_path.parent.mkdir(parents=True, exist_ok=True)
        hit_path.write_text(json.dumps(
            {"code": int(code), "wxid": wxid, "xor": int(code) & 0xFF,
             "hit_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
            ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass
    return (lambda data: wdd.decrypt_blob(data, key, xor)), key, xor


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="源目录（递归遍历）")
    ap.add_argument("--dst", required=True, help="输出目录")
    ap.add_argument("--contact", required=True, help="联系人/来源标签（用于日志）")
    ap.add_argument("--copy", action="store_true", help="复制（默认移动）")
    ap.add_argument("--decrypt", action="store_true",
                    help="解密 .dat 后再归档（不加则只列清单）")
    ap.add_argument("--code", default=None, help="已知 code，配合 --decrypt")
    ap.add_argument("--wxid", action="append", default=[], help="wxid 候选，可重复")
    ap.add_argument("--key-file", default=None, help="含 code/wxid 的 JSON")
    ap.add_argument("--account", default=None, help="账号根目录（缺省自动向上探测）")
    ap.add_argument("--decrypt-timeout", type=int, default=300, help="暴力推导超时秒数")
    ap.add_argument("--procs", type=int, default=0, help="暴力并发进程数（0=CPU-1）")
    args = ap.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)
    if not src.is_dir():
        print(f"[!] 源目录不存在: {src}")
        return

    # 建输出目录
    for folder in ["00-index", *TYPE_MAP.keys(), "05-misc", "99-duplicates"]:
        (dst / folder).mkdir(parents=True, exist_ok=True)

    decrypt_fn = None
    if args.decrypt:
        decrypt_fn, _key, _xor = load_decryptor(args, src)
        if decrypt_fn is None:
            print("[!] 未启用解密，退回只列清单模式")

    seen_hashes = {}
    records = []
    dat_records = []
    dup_count = 0
    file_count = 0
    dat_ok = dat_fail = 0

    for fp in src.rglob("*"):
        if not fp.is_file():
            continue
        ext = fp.suffix.lower()
        data = None           # 解密后的字节（None = 走原文件复制/移动）
        out_name = fp.name
        out_suffix = fp.suffix

        if ext in SKIP_EXTS:
            if decrypt_fn is None:
                # 不加 --decrypt：只列清单（原行为）
                mtime = datetime.fromtimestamp(fp.stat().st_mtime)
                dat_records.append({
                    "原路径": str(fp),
                    "大小": human_size(fp.stat().st_size),
                    "修改时间": mtime.strftime("%Y-%m-%d %H:%M"),
                })
                continue
            try:
                raw = fp.read_bytes()
            except OSError:
                dat_fail += 1
                continue
            data, fmt, err = decrypt_fn(raw)
            if data is None:
                dat_fail += 1
                mtime = datetime.fromtimestamp(fp.stat().st_mtime)
                dat_records.append({
                    "原路径": str(fp),
                    "大小": human_size(fp.stat().st_size),
                    "修改时间": mtime.strftime("%Y-%m-%d %H:%M"),
                    "解密": err or "失败",
                })
                continue
            dat_ok += 1
            out_suffix = "." + fmt
            out_name = fp.stem + out_suffix

        if not ext:
            ext = ""
        folder = classify(out_suffix)
        mtime = datetime.fromtimestamp(fp.stat().st_mtime)
        month = mtime.strftime("%Y-%m")
        prefix = mtime.strftime("%Y%m%d")
        stem = Path(out_name).stem

        # 计算哈希（去重）
        h = sha256_bytes(data) if data is not None else sha256_of(fp)
        if h in seen_hashes:
            target_dir = dst / "99-duplicates" / month
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / out_name
            dup_count += 1
        else:
            seen_hashes[h] = str(fp)
            target_dir = dst / folder / month
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / f"{prefix}-{stem}{out_suffix}"
            # 避免重名
            i = 1
            while target.exists():
                target = target_dir / f"{prefix}-{stem}-v{i}{out_suffix}"
                i += 1
            file_count += 1

        # 落盘：解密件直接写字节，原文件按 --copy 复制/默认移动
        if data is not None:
            try:
                target.write_bytes(data)
            except OSError as exc:
                print(f"[!] 写入失败 {target}: {exc}")
                continue
        elif args.copy:
            shutil.copy2(fp, target)
        else:
            shutil.move(str(fp), str(target))

        records.append({
            "原路径": str(fp),
            "归档路径": str(target),
            "类型": folder,
            "月份": month,
            "大小": human_size(target.stat().st_size),
            "哈希": h,
            "重复": h in seen_hashes and seen_hashes[h] != str(fp),
        })

    # 写 index.csv
    csv_path = dst / "00-index" / "index.csv"
    fields = ["原路径", "归档路径", "类型", "月份", "大小", "哈希", "重复"]
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

    # 写 .dat 清单（没解密的、或解密失败的才留在这张表里）
    dat_csv_path = dst / "00-index" / "dat_files.csv"
    if dat_records:
        with open(dat_csv_path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=["原路径", "大小", "修改时间", "解密"])
            w.writeheader()
            w.writerows(dat_records)

    # 写 README.md
    readme = dst / "00-index" / "README.md"
    with open(readme, "w", encoding="utf-8") as f:
        f.write(f"# 微信归档 — {args.contact}\n\n")
        f.write(f"- 源目录: `{src}`\n")
        f.write(f"- 归档时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"- 总文件数: {file_count}\n")
        f.write(f"- 去重重复文件: {dup_count}\n")
        if decrypt_fn is not None:
            f.write(f"- .dat 已解密并归档: {dat_ok}\n")
            f.write(f"- .dat 解密失败（清单见 dat_files.csv）: {dat_fail}\n")
        else:
            f.write(f"- .dat 图片缓存（未解密，加 --decrypt 可解，清单见 dat_files.csv）"
                    f": {len(dat_records)}\n")
        f.write("\n## 目录结构\n\n")
        f.write("- `01-documents/` Word/PDF/Excel\n")
        f.write("- `02-images/` 图片（含 .dat 解出来的）\n")
        f.write("- `03-videos/` 视频\n")
        f.write("- `04-voice/` 语音\n")
        f.write("- `05-misc/` 其他\n")
        f.write("- `99-duplicates/` 哈希重复文件\n")

    print(f"[✓] 整理完成")
    print(f"    归档文件: {file_count}")
    print(f"    重复文件: {dup_count}")
    if decrypt_fn is not None:
        print(f"    .dat 解密成功: {dat_ok}，失败: {dat_fail}")
    else:
        print(f"    .dat 图片（未解密，仅记录）: {len(dat_records)}")
    print(f"    输出: {dst}")
    print(f"    索引: {csv_path}")


if __name__ == "__main__":
    main()
