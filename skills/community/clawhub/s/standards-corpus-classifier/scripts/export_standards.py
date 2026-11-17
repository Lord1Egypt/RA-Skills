# -*- coding: utf-8 -*-
"""
从已分类语料导出（下载）某一分类或某一年度的标准 PDF 为 zip 包。

读取 classify_standards.py 产出的 standards_categorized.csv，按 --domain / --year /
--stdno(标准号) / --name(标准名称) 过滤，将匹配到的 PDF 打包成 zip（即"下载"该子集）。
各过滤条件之间为 AND 组合；均不指定时需加 --all 才导出全部（防误下载整个语料）。--stdno / --name 为子串模糊匹配（忽略大小写）。

用法:
    python export_standards.py <CSV> --domain 安全生产 --out 安全生产.zip
    python export_standards.py <CSV> --year 2024 --out 2024年度.zip
    python export_standards.py <CSV> --stdno 1031 --out 含1031.zip
    python export_standards.py <CSV> --name 大气污染物 --out 大气污染物.zip
    python export_standards.py <CSV> --domain 安全生产 --year 2024 --name 加油站 --list   # 仅预览
依赖: 仅标准库 (csv / argparse / pathlib / zipfile / collections)
"""
import csv, sys, argparse, zipfile, re
from pathlib import Path
from collections import Counter


def contains(haystack, needle):
    """子串模糊匹配（忽略大小写）。needle 为空时恒真。"""
    if not needle:
        return True
    return needle.lower() in (haystack or "").lower()


def _confine(corpus, path):
    """若 path 解析后不在 corpus 内则返回 None，防路径遍历读出语料外文件。"""
    try:
        corpus_r = Path(corpus).resolve()
        p_r = Path(path).resolve()
    except OSError:
        return None
    if p_r == corpus_r or corpus_r in p_r.parents:
        return p_r
    return None


def sanitize_token(tok):
    """去除路径分隔符与 . / ..，避免拼接出的 label 含危险片段。"""
    out = []
    for seg in str(tok).replace("\\", "/").split("/"):
        if seg in ("", ".", ".."):
            continue
        out.append(seg)
    return "_".join(out) if out else "x"


def locate(corpus, r):
    """按 文件名 + 子文件夹 定位 PDF；找不到时回退到 by_year/年份/ 或按标准号模糊匹配。"""
    fname = r.get("文件名", "").strip()
    sub = r.get("子文件夹", "").strip()
    year = r.get("年份", "").strip()
    if fname:
        for cand in (corpus / "pdfs" / sub / fname,
                     corpus / sub / fname,
                     corpus / "by_year" / year / fname):
            if cand.exists():
                safe = _confine(corpus, cand)
                if safe:
                    return safe
    # 回退：用标准号中的 number-year 在子文件夹里模糊匹配
    std = r.get("标准号", "")
    m = re.search(r"(\d+-\d{4})", std)
    if m and sub:
        token = m.group(1)
        d = corpus / "pdfs" / sub
        if d.is_dir():
            for p in d.glob(f"*{token}*.pdf"):
                safe = _confine(corpus, p)
                if safe:
                    return safe
    return None


def main():
    ap = argparse.ArgumentParser(description="按分类/年份导出标准 PDF 为 zip（下载子集）")
    ap.add_argument("csv", help="standards_categorized.csv 路径")
    ap.add_argument("--domain", help="按领域过滤（精确匹配，如 安全生产）")
    ap.add_argument("--year", help="按年份过滤（如 2024）")
    ap.add_argument("--stdno", help="按标准号模糊匹配（子串，忽略大小写，如 1031 或 DB11/T 1031）")
    ap.add_argument("--name", help="按标准名称模糊匹配（子串，忽略大小写，如 大气污染物）")
    ap.add_argument("--out", default=None, help="输出 zip 路径（默认按过滤条件命名）")
    ap.add_argument("--list", action="store_true", help="仅列出匹配项，不打包")
    ap.add_argument("--all", action="store_true", help="未指定任何过滤条件时，显式导出整个语料")
    args = ap.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        sys.exit(f"找不到 CSV 文件：{csv_path}")
    corpus = csv_path.parent  # standards_categorized.csv 位于语料根目录
    rows = []
    try:
        with open(csv_path, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                rows.append(r)
    except OSError as e:
        sys.exit(f"无法读取 CSV：{e}")

    has_filter = any([args.domain, args.year, args.stdno, args.name])
    if not has_filter and not args.list and not args.all:
        sys.exit("未指定任何过滤条件，不会导出整个语料（防误下载）。"
                 "如需导出全部请加 --all；或加 --list 仅预览。")

    matched = [r for r in rows
               if (not args.domain or r.get("领域", "") == args.domain)
               and (not args.year or r.get("年份", "") == args.year)
               and contains(r.get("标准号", ""), args.stdno)
               and contains(r.get("名称", ""), args.name)]
    if not matched:
        sys.exit(f"无匹配项（domain={args.domain} year={args.year} stdno={args.stdno} name={args.name}）")

    if args.list:
        c = Counter(r["领域"] for r in matched)
        print(f"匹配 {len(matched)} 份：")
        for dom, n in c.most_common():
            print(f"  {dom}: {n}")
        for r in matched[:50]:
            print(f"  - [{r['年份']}] {r['标准号']} {r['名称']}")
        if len(matched) > 50:
            print(f"  ... 共 {len(matched)} 份")
        return

    parts = [p for p in (
        sanitize_token(args.domain) if args.domain else None,
        f"年度{args.year}" if args.year else None,
        f"号{args.stdno}" if args.stdno else None,
        f"名{args.name}" if args.name else None,
    ) if p]
    label = "_".join(parts) if parts else "全部"
    out_name = args.out or f"{label}.zip"
    out_path = Path(out_name)
    if not out_path.is_absolute():
        out_path = corpus / out_name

    n_added, missing = 0, []
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        for r in matched:
            src = locate(corpus, r)
            if not src:
                missing.append(r.get("文件名") or r.get("标准号", ""))
                continue
            arcname = f"{label}/{src.name}"
            # 二次保险：arcname 不得含 .. 或以 / 开头，防 zip 内部路径逃逸
            if ".." in arcname or arcname.startswith("/"):
                missing.append(r.get("文件名") or r.get("标准号", ""))
                continue
            z.write(str(src), arcname)
            n_added += 1

    msg = f"已打包: {out_path} （{n_added} 份"
    if missing:
        msg += f"，{len(missing)} 份源文件未找到"
    msg += "）"
    print(msg)
    for m in missing[:10]:
        print("  缺失:", m)


if __name__ == "__main__":
    main()
