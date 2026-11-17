#!/usr/bin/env python3
"""PDF 文本层探测：判断原理图 PDF 是 L2（矢量+文本层）还是 L3（扫描版）。

探测逻辑：
1. 逐页提文本（pymupdf），统计 refdes 命中（R/C/U/D/Q/J/L/SW/MK 前缀+数字）
   与 net-label 风格标记（全大写下划线词：VCC/GND/3V3/SDA/SCL/...）
2. 命中密度高 → L2；文本极少/为零 → L3
3. --dump 输出逐页 Markdown 摘要（refdes 聚合），供预读定位页码

仅用文本层，不做 OCR —— 扫描版直接判 L3，不硬猜。
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

# Windows GBK 控制台保护：中文输出强制 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REFDES_RE = re.compile(r"^(?P<prefix>[A-Z]{1,2})\??(?P<num>\d+)$")
# 常见 refdes 前缀（IEC 60617 / Altium 惯例）
KNOWN_PREFIXES = {
    "R", "C", "L", "D", "Q", "U", "J", "P", "K", "F", "T", "X",
    "SW", "MK", "Y", "FB", "RV", "Z", "TP", "CN", "LED", "BT", "SP",
}
NET_LABEL_RE = re.compile(
    r"^(?![0-9])[A-Z0-9][A-Z0-9_+/.\-]{1,30}$"
)
NET_BLOCKLIST = {"REF", "DES", "TITLE", "SIZE", "DATE", "REV", "SHEET", "FILE", "SCALE", "DRAWN", "CHECKED", "APPROVED"}


def classify_pages(doc):
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text") or ""
        words = [w.strip() for w in text.split() if w.strip()]
        refdes_hits = set()
        net_hits = set()
        for w in words:
            m = REFDES_RE.match(w)
            if m and m.group("prefix") in KNOWN_PREFIXES:
                refdes_hits.add(w)
            elif w.isupper() and NET_LABEL_RE.match(w):
                base = w.split("_")[0].split("+")[0].split("-")[0]
                if base not in NET_BLOCKLIST and len(w) >= 2:
                    net_hits.add(w)
        pages.append({
            "page": i + 1,
            "word_count": len(words),
            "refdes_count": len(refdes_hits),
            "net_label_count": len(net_hits),
            "refdes_sample": sorted(refdes_hits)[:20],
            "net_sample": sorted(net_hits)[:20],
        })
    return pages


def verdict(pages):
    total_refdes = sum(p["refdes_count"] for p in pages)
    total_words = sum(p["word_count"] for p in pages)
    if total_words < 20:
        level, reason = "L3", "几乎无文本层（扫描版/图片型 PDF）"
    elif total_refdes < 5:
        level, reason = "L3", "文本层存在但无 refdes 结构（非原理图 PDF 或文字已转曲线）"
    else:
        level, reason = "L2", f"矢量文本层有效：{total_refdes} 个 refdes 命中"
    return level, reason, total_refdes


def dump_markdown(doc, pages, out_path):
    lines = ["# PDF 预读摘要", ""]
    for p in pages:
        page = doc[p["page"] - 1]
        text = page.get_text("text") or ""
        tokens = [w.strip() for w in text.split() if w.strip()]
        by_prefix = defaultdict(list)
        for w in tokens:
            m = REFDES_RE.match(w)
            if m and m.group("prefix") in KNOWN_PREFIXES:
                by_prefix[m.group("prefix")].append(w)
        lines.append(f"## 第 {p['page']} 页（{p['word_count']} 词，{p['refdes_count']} refdes）")
        if by_prefix:
            parts = [f"{pf}×{len(lst)}" for pf, lst in sorted(by_prefix.items())]
            lines.append("- 器件分布：" + "、".join(parts))
        if p["net_sample"]:
            lines.append("- 网络标签样例：" + "、".join(p["net_sample"][:15]))
        lines.append("")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description="原理图 PDF 文本层探测")
    ap.add_argument("pdf")
    ap.add_argument("--dump", help="导出逐页 Markdown 摘要到指定路径")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--install-pymupdf", action="store_true",
                    help="缺 pymupdf 时允许脚本 pip --user 安装（默认只提示，不联网）")
    args = ap.parse_args()

    try:
        import fitz  # pymupdf
    except ImportError:
        # 可选解释器：环境变量 SCHEMATIC_PDF_PYTHON 指向已装 pymupdf 的 Python
        alt = os.environ.get("SCHEMATIC_PDF_PYTHON", "")
        if alt and os.path.exists(alt) and os.path.abspath(sys.executable) != os.path.abspath(alt):
            import subprocess
            r = subprocess.run([alt, os.path.abspath(__file__)] + sys.argv[1:])
            sys.exit(r.returncode)
        if args.install_pymupdf:
            import subprocess
            print("提示: 按 --install-pymupdf 安装 pymupdf（国内镜像）……", file=sys.stderr)
            r = subprocess.run([sys.executable, "-m", "pip", "install", "--user", "pymupdf",
                                "--index-url", "https://mirrors.aliyun.com/pypi/simple"],
                               capture_output=True, text=True)
            if r.returncode == 0:
                import importlib
                importlib.invalidate_caches()
                try:
                    import fitz  # noqa
                except ImportError:
                    pass
                else:
                    print("pymupdf 安装成功，重新运行探测……", file=sys.stderr)
                    r2 = subprocess.run([sys.executable, os.path.abspath(__file__)] + sys.argv[1:])
                    sys.exit(r2.returncode)
        print("ERROR: 缺少 pymupdf（PDF 文本层探测需要）。安装：pip install pymupdf\n"
              "  国内镜像: pip install pymupdf --index-url https://mirrors.aliyun.com/pypi/simple\n"
              "  或加 --install-pymupdf 让本脚本安装；也可用 SCHEMATIC_PDF_PYTHON 指定解释器",
              file=sys.stderr)
        sys.exit(2)

    if not os.path.exists(args.pdf):
        print(f"ERROR: 文件不存在 {args.pdf}", file=sys.stderr)
        sys.exit(2)

    try:
        doc = fitz.open(args.pdf)
    except Exception as e:
        print(f"ERROR: 打不开（{type(e).__name__}: {e}）——文件损坏、不是 PDF、"
              f"或后缀名与内容不符", file=sys.stderr)
        sys.exit(2)
    if doc.needs_pass:
        print("ERROR: PDF 加密（有打开密码）——请先解密：阅读器里另存为不受密码保护的 PDF",
              file=sys.stderr)
        sys.exit(2)
    if not doc.is_pdf:
        print("ERROR: pymupdf 认不出这是 PDF", file=sys.stderr)
        sys.exit(2)

    pages = classify_pages(doc)
    level, reason, total_refdes = verdict(pages)

    result = {
        "file": args.pdf,
        "page_count": len(doc),
        "level": level,
        "reason": reason,
        "total_refdes": total_refdes,
        "pages": pages,
    }

    if args.dump:
        dump_markdown(doc, pages, args.dump)
        result["dump"] = args.dump

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"档位: {level}")
        print(f"理由: {reason}")
        print(f"页数: {len(doc)}  refdes 命中: {total_refdes}")
        if level == "L2":
            print("能力: refdes/net label/页结构可提取；连通性不可恢复（须声明）")
            for p in pages:
                if p["refdes_count"]:
                    print(f"  第{p['page']}页: {p['refdes_count']} 器件, net 样例 {p['net_sample'][:5]}")
        else:
            print("处置: 走 L3 话术 —— 请用户补原格式工程或 EDA 导出的矢量 PDF")
    # 退出语义：探针本身的成败 ≠ 探测结论。
    #   0  = 探针正常给出档位结论（L2 或 L3 都是"成功探测"）
    #   2  = 探针故障（缺依赖/文件问题）——才是失败
    # L3 的"拒识结论"用 JSON level 字段或文本"档位: L3"判断，不用 exit code。
    sys.exit(0)


if __name__ == "__main__":
    main()
