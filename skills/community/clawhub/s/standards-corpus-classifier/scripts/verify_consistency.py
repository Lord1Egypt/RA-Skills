#!/usr/bin/env python3
"""标准语料分类结果的事实一致性核验（防幻觉机制）。

核心思想：分类结果是"确定性脚本 + 文件名/注册表"产出的，必须可验证、可追溯，
不能依赖任何 LLM 生成。本脚本断言以下不变量，任意一项失败即说明产物有错（或幻觉）：
  1. CSV 行数 == pdfs/ 下实际 PDF 文件数（无丢行、无多行）
  2. CSV 每行「文件名」都能在 pdfs/<子文件夹>/<文件名> 真实找到（无虚构条目）
  3. 领域列无空值（无未归类）
  4. 标准号无重复（无编造/重复计数）
  5. 报告 HTML 中声称的总数 == CSV 行数

用法:
    python scripts/verify_consistency.py <CORPUS_DIR> [--report 报告.html]
退出码 0=全部通过, 1=存在不一致
"""
import sys
import csv
from pathlib import Path
from collections import Counter


def verify(corpus_root, report_html=None):
    root = Path(corpus_root)
    csvp = root / "standards_categorized.csv"
    if not csvp.exists():
        print(f"❌ 找不到 CSV: {csvp}")
        return False

    rows = list(csv.DictReader(open(csvp, encoding="utf-8-sig")))
    n = len(rows)
    pdfs_dir = root / "pdfs"
    actual = list(pdfs_dir.rglob("*.pdf")) if pdfs_dir.is_dir() else []
    actual_n = len(actual)

    problems = []

    # 1. 行数 == 实际文件数
    if n != actual_n:
        problems.append(f"CSV行数({n}) != pdfs实际PDF数({actual_n})")

    # 2. 文件名可追溯
    missing = []
    for r in rows:
        fn = (r.get("文件名") or "").strip()
        sub = (r.get("子文件夹") or "").strip()
        if fn and not (pdfs_dir / sub / fn).exists():
            missing.append(fn)
    if missing:
        problems.append(f"{len(missing)} 个文件名在 pdfs 下找不到（如 {missing[:3]}）")

    # 3. 领域空值
    empty = sum(1 for r in rows if not (r.get("领域") or "").strip())
    if empty:
        problems.append(f"{empty} 行领域为空（未归类）")

    # 4. 标准号重复
    stdnos = [r.get("标准号", "").strip() for r in rows]
    dup = [k for k, c in Counter(stdnos).items() if c > 1 and k]
    if dup:
        problems.append(f"{len(dup)} 个重复标准号（如 {dup[:3]}）")

    # 5. 报告数字一致
    if report_html:
        rp = Path(report_html)
        if rp.exists():
            t = rp.read_text(encoding="utf-8", errors="ignore")
            if str(n) not in t:
                problems.append(f"报告 {rp.name} 未包含总数 {n}（数字对不上）")

    print(f"\n=== {root.name} 事实一致性核验 ===")
    print(f"  CSV 行数 = {n}")
    print(f"  pdfs 实际 PDF 数 = {actual_n}")
    print(f"  文件名可追溯 = {len(missing) == 0}（缺失 {len(missing)}）")
    print(f"  领域空值 = {empty} | 重复标准号 = {len(dup)}")
    if problems:
        print("❌ 发现不一致:")
        for p in problems:
            print("   -", p)
        return False
    print("✅ 全部通过：CSV 与源文件完全自洽，无虚构/丢失/重复")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: verify_consistency.py <CORPUS_DIR> [--report 报告.html]")
        sys.exit(2)
    corpus = sys.argv[1]
    report = None
    if "--report" in sys.argv:
        report = sys.argv[sys.argv.index("--report") + 1]
    ok = verify(corpus, report)
    sys.exit(0 if ok else 1)
