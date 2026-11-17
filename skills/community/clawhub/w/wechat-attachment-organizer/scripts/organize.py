#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat 附件整理器（合规版）。

按分类方法把附件【复制】到目标目录。默认 dry-run 预览，绝不移动/删除源文件。
  - type    ：按真实类型（文档/表格/图片/视频/压缩包/音频/其他）+ 年-月归档
  - customer：按目标目录下已有的「客户文件夹名」匹配
              L1 文件名包含客户名 -> 命中
              L2 文档正文（docx/xlsx/txt/pdf）包含客户名 -> 命中
              都未命中 -> 进入 __未归类__/ 待人工处理
  - custom  ：按 --custom-rules 的 JSON（[{pattern, folder}]）匹配

增量：目标目录下的 .wxa_state.json 记录已处理 sha256，重跑只处理新增。
安全：只写目标目录；任何删除必须由操作者另行显式执行（走回收站）。
"""
import os
import sys
import re
import json
import shutil
import argparse
import zipfile
import subprocess
import datetime
from collections import Counter

TYPE_MAP = {
    "pdf": "文档", "doc": "文档", "docx": "文档", "txt": "文档", "rtf": "文档",
    "md": "文档", "ppt": "文档", "pptx": "文档", "pages": "文档",
    "xls": "表格", "xlsx": "表格", "csv": "表格", "numbers": "表格",
    "jpg": "图片", "jpeg": "图片", "png": "图片", "gif": "图片", "bmp": "图片",
    "webp": "图片", "heic": "图片",
    "mp4": "视频", "mov": "视频", "avi": "视频", "mkv": "视频", "webm": "视频",
    "zip": "压缩包", "rar": "压缩包", "7z": "压缩包", "tar": "压缩包", "gz": "压缩包",
    "mp3": "音频", "wav": "音频", "m4a": "音频", "aac": "音频",
}
DEFAULT_TYPE = "其他"


def type_category(ext):
    return TYPE_MAP.get((ext or "").lower(), DEFAULT_TYPE)


def decode_dat(src, key, dst):
    with open(src, "rb") as f:
        data = f.read()
    dec = bytes(b ^ key for b in data)
    with open(dst, "wb") as f:
        f.write(dec)


def extract_text(src, ext):
    """尽力抽取文本用于客户名匹配；失败返回空串。"""
    ext = (ext or "").lower()
    try:
        if ext == "txt":
            return open(src, encoding="utf-8", errors="ignore").read()
        if ext == "docx":
            with zipfile.ZipFile(src) as z:
                xml = z.read("word/document.xml")
            return re.sub(r"<[^>]+>", " ", xml.decode("utf-8", "ignore"))
        if ext == "xlsx":
            with zipfile.ZipFile(src) as z:
                if "xl/sharedStrings.xml" in z.namelist():
                    return re.sub(r"<[^>]+>", " ",
                                 z.read("xl/sharedStrings.xml").decode("utf-8", "ignore"))
            return ""
        if ext == "pdf":
            try:
                r = subprocess.run(["pdftotext", src, "-"], capture_output=True,
                                   text=True, timeout=30)
                if r.returncode == 0:
                    return r.stdout
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
            return ""
    except Exception:
        return ""
    return ""


def customer_match(name, text, customers):
    low = (name or "").lower()
    for c in customers:
        if c and c.lower() in low:
            return c
    for c in customers:
        if c and c.lower() in (text or "").lower():
            return c
    return None


def custom_match(entry, real_ext, rules):
    name = entry["name"].lower()
    for rule in rules:
        pat = (rule.get("pattern") or "").lower()
        if pat in name or pat == (real_ext or "").lower() or pat in entry["src"].lower():
            return rule.get("folder")
    return None


def pick_canonical(group):
    """同内容（sha256 相同）多份时选一份保留。

    判定重复只看 sha256（调用方已按哈希分组）。本函数只决定【保留哪一份】，
    且仅依据技术属性、不比较文件名：
      1) 优先已解码的真实文件（非 .dat），因为 .dat 是微信容器、需解码还原；
      2) 其次修改时间最早（通常是最早收到的那份原件）。
    """
    def key(e):
        is_dat = 1 if e.get("dat_key") is not None else 0
        return (is_dat, e["mtime"])
    return sorted(group, key=key)[0]


def main():
    ap = argparse.ArgumentParser(description="Organize WeChat attachments (copy-only, dry-run default).")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--mode", choices=["type", "customer", "custom"], required=True)
    ap.add_argument("--custom-rules", help="自定义规则 JSON 文件路径")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不复制（默认行为）")
    ap.add_argument("--apply", action="store_true", help="真正执行复制")
    ap.add_argument("--suggest-new", action="store_true",
                    help="customer 模式下，列出未归类文件名中的候选新客户名")
    ap.add_argument("--dedup", action="store_true",
                    help="按 sha256 去重：仅哈希值相同才视为重复，同内容只保留一份（保留非 .dat 解码态/修改时间最早者），其余写入去重报告")
    args = ap.parse_args()

    if not args.dry_run and not args.apply:
        args.dry_run = True  # 安全默认：不显式 --apply 就只预览

    manifest = json.load(open(args.manifest, encoding="utf-8"))
    entries = manifest["entries"]
    os.makedirs(args.dest, exist_ok=True)
    state_path = os.path.join(args.dest, ".wxa_state.json")
    state = json.load(open(state_path, encoding="utf-8")) if os.path.exists(state_path) else {"hashes": []}
    done = set(state["hashes"])

    customers = []
    if args.mode == "customer":
        customers = [d for d in sorted(os.listdir(args.dest))
                     if os.path.isdir(os.path.join(args.dest, d)) and not d.startswith(".")]
        if not customers and not args.suggest_new:
            print("目标目录下没有客户文件夹。请先建至少一个，或改用 type 模式。", file=sys.stderr)
            sys.exit(2)

    rules = []
    if args.mode == "custom":
        if not args.custom_rules or not os.path.exists(args.custom_rules):
            print("custom 模式需要 --custom-rules JSON 文件。", file=sys.stderr)
            sys.exit(2)
        rules = json.load(open(args.custom_rules, encoding="utf-8"))

    # 1) 分类（排除已处理），产出待办 todo = [(entry, rel_dir, out_name), ...]
    todo = []
    new_candidates = Counter()
    for e in entries:
        if e.get("sha256") and e["sha256"] in done:
            continue
        real_ext = e.get("real_ext") or e["ext"]
        if args.mode == "type":
            cat = type_category(real_ext)
            ym = datetime.datetime.fromtimestamp(e["mtime"]).strftime("%Y-%m")
            rel_dir = os.path.join(cat, ym)
        elif args.mode == "customer":
            cust = customer_match(e["name"], extract_text(e["src"], real_ext), customers)
            rel_dir = os.path.join(cust, type_category(real_ext)) if cust \
                else os.path.join("__未归类__", type_category(real_ext))
            if not cust and args.suggest_new:
                for tok in re.split(r"[\s_\-+（）()【】\[\].]+", os.path.splitext(e["name"])[0]):
                    if len(tok) >= 2 and not re.fullmatch(r"\d{4,}", tok):
                        new_candidates[tok] += 1
        else:
            folder = custom_match(e, real_ext, rules)
            rel_dir = folder if folder else os.path.join("__未归类__", type_category(real_ext))
        base, _ = os.path.splitext(e["name"])
        out_name = (base + "." + (real_ext or "bin")) if e.get("dat_key") is not None else e["name"]
        todo.append((e, rel_dir, out_name))

    # 2) 去重：同 sha256 只保留一份
    plan = []
    dup_report = []
    space_saved = 0
    if args.dedup:
        by_hash = {}
        unhashed = []
        for tri in todo:
            h = tri[0].get("sha256")
            if not h:
                unhashed.append(tri)  # 无哈希（--no-hash 扫描）无法去重，保留原样
                continue
            by_hash.setdefault(h, []).append(tri)
        for h, group in by_hash.items():
            if len(group) == 1:
                plan.append(group[0])
                continue
            canon = pick_canonical([t[0] for t in group])
            canon_tri = next(t for t in group if t[0] is canon)
            dups = [t[0]["src"] for t in group if t[0] is not canon]
            space_saved += sum(t[0]["size"] for t in group if t[0] is not canon)
            dup_report.append({
                "sha256": h, "count": len(group),
                "canonical": canon_tri[0]["src"],
                "canonical_target": os.path.join(args.dest, canon_tri[1], canon_tri[2]),
                "duplicates": dups,
            })
            plan.append(canon_tri)
        plan.extend(unhashed)
    else:
        plan = todo

    # 3) 预览
    print(f"[{'DRY-RUN 预览' if args.dry_run else 'APPLY 执行'}] 模式={args.mode}"
          f"  去重={'开' if args.dedup else '关'}  待复制={len(plan)} 个")
    by_dir = Counter(t[1] for t in plan)
    for d in sorted(by_dir):
        print(f"  {by_dir[d]:>4}  {d}")
    if args.dedup and dup_report:
        print(f"\n去重：{len(dup_report)} 组重复（涉及 {sum(g['count'] for g in dup_report)} 个文件），"
              f"仅保留 {len(plan)} 份，预计节省 {space_saved/1024/1024:.1f} MB")
        print("     重复文件原路径已记入 dedup_report.json（源文件不动）。")
    if args.suggest_new and new_candidates:
        print("\n候选新客户名（来自未归类文件名，请人工甄别）：")
        for tok, n in new_candidates.most_common(30):
            print(f"  {n:>4}  {tok}")

    if args.dry_run:
        print("\n（dry-run 未改动任何文件。加 --apply 才真正复制。）")
        return

    # 4) 执行复制
    copied = 0
    upload_list = []
    for e, rel_dir, out_name in plan:
        target = os.path.join(args.dest, rel_dir, out_name)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        if e.get("dat_key") is not None:
            decode_dat(e["src"], e["dat_key"], target)
        else:
            shutil.copy2(e["src"], target)
        if e.get("sha256"):
            done.add(e["sha256"])
        copied += 1
        upload_list.append({
            "abs_path": target,
            "rel_path": os.path.relpath(target, args.dest),
            "sha256": e["sha256"],
            "size": e["size"],
            "type": type_category(e.get("real_ext") or e["ext"]),
            "real_ext": e.get("real_ext") or e["ext"],
            "name": e["name"],
        })
    state["hashes"] = sorted(done)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    if args.dedup and dup_report:
        dr_path = os.path.join(args.dest, "dedup_report.json")
        with open(dr_path, "w", encoding="utf-8") as f:
            json.dump({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
                       "groups": dup_report, "space_saved_bytes": space_saved},
                      f, ensure_ascii=False, indent=2)
    up_path = os.path.join(args.dest, "wxa_upload_manifest.json")
    with open(up_path, "w", encoding="utf-8") as f:
        json.dump(upload_list, f, ensure_ascii=False, indent=2)

    print(f"\n已复制 {copied} 个文件。状态已记入 {state_path}")
    print(f"上传清单已生成：{up_path}（供导入资料库全文检索）")
    if args.dedup and dup_report:
        print(f"去重报告：{dr_path}（{len(dup_report)} 组重复，节省 {space_saved/1024/1024:.1f} MB）")
    print("注意：源文件未被移动或删除。需要清理请在确认备份后手动处理。")


if __name__ == "__main__":
    main()
