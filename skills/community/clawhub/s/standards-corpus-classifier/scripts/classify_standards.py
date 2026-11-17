# -*- coding: utf-8 -*-
"""
标准语料库分类脚本（通用版，skill: standards-corpus-classifier）

将一批标准 PDF 按「级别(国家/行业/地方) × 领域」归置：
  - 解析文件名中的标准代号 → 查 sources.json 得 级别/归属
  - 按标准名称关键词 → 查 domains.json 得 领域，移入 01_领域 编号子文件夹
  - 产出 standards_categorized.csv（领域/级别/归属/标准类型/年份/标准号/名称/子文件夹）

支持国家(GB/GB-T/GB-Z)、行业(QX/JB/YY/…)、地方(DB11/DB31/…，含 DB11_ 空格坑)。
采集层(WebSearch/WebFetch 拉取)属 Phase2，本脚本仅做编目与本地归类。

用法:
    python classify_standards.py <CORPUS_DIR> [--dry] [--sources PATH] [--domains PATH] [--out SUBDIR]
    <CORPUS_DIR>  含 PDF 的目录（脚本递归扫描，故 PDF 在根或 pdfs/ 子目录均可）
    --dry          仅统计与预览，不移动文件、不写 CSV
    --sources      sources.json 路径（默认脚本同级的 ../references/sources.json）
    --domains      domains.json 路径（默认脚本同级的 ../references/domains.json）
    --out          PDF 输出子目录名（默认 pdfs；分类结果写入 <CORPUS_DIR>/<out>/01_领域/…）
"""
import os, re, csv, sys, json, shutil, argparse
from collections import Counter, OrderedDict
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = SKILL_ROOT / "references" / "sources.json"
DEFAULT_DOMAINS = SKILL_ROOT / "references" / "domains.json"
FALLBACK = "其他(未明确归类)"


def load_sources(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_domains(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    domains = OrderedDict(d.get("domains", d))
    if FALLBACK not in domains:
        domains[FALLBACK] = []
    return domains


def parse_code(fname):
    """从文件名提取 (base, is_recommended, number, year, title)。

    文件名形如:
        DB11_ 2567-2026_生活垃圾焚烧大气污染物排放标准.pdf   (地方, 强制, 注意下划线+空格)
        DB11_T 1031-2025_低层蒸压加气混凝土承重建筑技术规程.pdf (地方, 推荐)
        GB/T 1.1-2020_标准化工作导则.pdf                      (国家, 推荐)
        QX 45-2020_xxx.pdf / QX/T 45-2020_xxx.pdf             (行业)
    返回 None 表示无法解析。
    """
    if not fname.lower().endswith(".pdf"):
        return None
    stem = fname[:-4]
    parts = stem.split(None, 1)          # 按首个空白切分
    if len(parts) < 2:
        return None
    prefix_token, rest = parts
    m = re.match(r"^([\d.]+)-(\d{4})_(.+)$", rest)
    if not m:
        return None
    number, year, title = m.group(1), m.group(2), m.group(3)
    raw = prefix_token.replace("_", "")
    is_rec = raw.endswith("T") and len(raw) > 1
    base = raw[:-1] if is_rec else raw
    return base, is_rec, number, year, title


def lookup_source(sources, base):
    for bucket in ("national", "industry", "local"):
        entry = sources.get(bucket, {}).get(base)
        if entry:
            return entry
    # DB 子级市代码(如 DB4403 深圳)回退到省级(DB44)
    if base.startswith("DB") and len(base) > 4:
        prov = base[:4]
        for bucket in ("national", "industry", "local"):
            entry = sources.get(bucket, {}).get(prov)
            if entry:
                return dict(entry, subcity=base)
    return None


def domain_of(title, domains):
    for dom, kws in domains.items():
        if any(k in title for k in kws):
            return dom
    return FALLBACK


def std_type(is_recommended):
    return "推荐性" if is_recommended else "强制性"


def main():
    ap = argparse.ArgumentParser(description="标准语料库分类（级别×领域）")
    ap.add_argument("corpus_dir", help="含 PDF 的目录（递归扫描）")
    ap.add_argument("--sources", default=str(DEFAULT_SOURCES))
    ap.add_argument("--domains", default=str(DEFAULT_DOMAINS))
    ap.add_argument("--out", default="pdfs", help="PDF 输出子目录名（默认 pdfs）")
    ap.add_argument("--year-folders", action="store_true",
                    help="额外按年份建 <CORPUS>/by_year/YYYY/ 文件夹（硬链接，不占额外磁盘）")
    ap.add_argument("--dry", action="store_true", help="仅统计，不移动/不写CSV")
    args = ap.parse_args()

    sources = load_sources(args.sources)
    domains = load_domains(args.domains)
    corpus = Path(args.corpus_dir).resolve()
    if not corpus.exists():
        sys.exit(f"目录不存在: {corpus}")

    out_dir = corpus / args.out
    dom_index = OrderedDict(
        (dom, f"{i+1:02d}_{dom}") for i, dom in enumerate(domains.keys())
    )

    counted = Counter()
    rows = []
    unparsed = []
    if not args.dry:
        for sub in dom_index.values():
            (out_dir / sub).mkdir(parents=True, exist_ok=True)

    for fpath in sorted(corpus.rglob("*.pdf")):
        p = parse_code(fpath.name)
        if not p:
            unparsed.append(fpath.name)
            continue
        base, is_rec, number, year, title = p
        entry = lookup_source(sources, base)
        level = entry.get("level", "未配置") if entry else "未配置"
        belong = entry.get("name", "未配置") if entry else "未配置"
        if entry and entry.get("subcity"):
            belong = f"{belong}({entry['subcity']})"
        dom = domain_of(title, domains)
        sub = dom_index[dom]
        target_dir = out_dir / sub
        final_path = target_dir / fpath.name
        if fpath.parent == target_dir:
            counted[dom] += 1
        else:
            if not args.dry:
                shutil.move(str(fpath), str(final_path))
            counted[dom] += 1
        rows.append((dom, level, belong, std_type(is_rec), year,
                     f"{base}{'/T' if is_rec else ''} {number}-{year}", title, sub, fpath.name))
        if args.year_folders and not args.dry:
            ydir = corpus / "by_year" / year
            ydir.mkdir(parents=True, exist_ok=True)
            ydst = ydir / fpath.name
            if not ydst.exists():
                try:
                    os.link(str(final_path), str(ydst))
                except OSError:
                    shutil.copy2(str(final_path), str(ydst))

    if args.dry:
        print("=== 干跑: 各领域 PDF 数量（未移动） ===")
        for dom, sub in dom_index.items():
            n = counted.get(dom, 0)
            if n:
                print(f"  {sub}: {n}")
        print(f"\n总计匹配: {sum(counted.values())} | 无法解析: {len(unparsed)}")
        if unparsed:
            print("--- 无法解析（前20） ---")
            for f in unparsed[:20]:
                print("  ", f)
        others = [r for r in rows if r[0] == FALLBACK]
        if others:
            print(f"--- {FALLBACK} {len(others)} 项（前30） ---")
            for r in others[:30]:
                print("  -", r[6])
        print("\n（加 --dry 去掉后即实际执行；或省略 --dry 直接运行）")
        return

    csv_path = corpus / "standards_categorized.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["领域", "级别", "归属", "标准类型", "年份", "标准号", "名称", "子文件夹", "文件名"])
        for r in sorted(rows, key=lambda x: (x[7], x[5])):
            w.writerow(r)

    print("=== 各子文件夹 PDF 数量 ===")
    for dom, sub in dom_index.items():
        n = counted.get(dom, 0)
        if n:
            print(f"  {sub}: {n}")
    print(f"\n总计: {sum(counted.values())} 个 PDF | 无法解析: {len(unparsed)}")
    if unparsed:
        print("--- 无法解析（留在原处） ---")
        for f in unparsed:
            print("  ", f)
    print(f"分类名录: {csv_path}")


if __name__ == "__main__":
    main()
