# -*- coding: utf-8 -*-
"""DAT 域判据检查器（AI 可执行判定逻辑封装）。

将本包 L1 判据文件「判据_DAT.md」的现成判定逻辑封装为可执行检查器：
按判据摘要 5 节结构逐项校验，输出 PASS/FAIL 判定与结构化摘要，
结果可直接引用作为证据（Evidence）。不硬编码内部路径：
判据文件按脚本同级目录的父目录相对定位。

用法：
  python check_judge_DAT.py            # 对判据文件全量校验
  python check_judge_DAT.py --selftest # 自检模式：全项 PASS 则 exit 0
"""
import sys, io, re, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ---- 域参数（13 个 uibc-team-* 共享模板，仅此处不同）----
DOMAIN = "DAT"                      # 域缩写（与判据文件名一致）
CRITERION = "TH-DAT-001"            # 判据编号（可含 / 多编号）
# ---------------------------------------------------------

JUDGE_FILE = pathlib.Path(__file__).resolve().parent.parent / ("判据_%s.md" % DOMAIN)

# 判据摘要 5 节校验清单
SECTION_CHECKS = [
    ("判据核心", None, "核心节须非空"),
    ("迁移判定映射", None, "迁移判定映射节须非空"),
    ("可形式化等级上限与原因", r"L[0-4]", "等级上限节须声明 L0-L4 之一"),
    ("作答纪律", r"真源", "作答纪律节须声明本文件为判据真源"),
]


def extract_section(text, title):
    """提取 '## N. <title>...' 节内容（到下一个 ## N. 为止）。"""
    m = re.search(r"^##\s*\d+\.\s*%s" % re.escape(title), text, re.M)
    if not m:
        return None
    start = m.end()
    nxt = re.search(r"^##\s*\d+\.", text[start:], re.M)
    return text[start:start + (nxt.start() if nxt else len(text) - start)]


def main():
    if not JUDGE_FILE.exists():
        print("FAIL | 判据文件缺失 | %s" % JUDGE_FILE)
        return 1
    text = JUDGE_FILE.read_text(encoding="utf-8")
    results = []

    # 1) 判据编号引用
    m = re.search(r"判据编号[：:]\s*(TH-[A-Z]+-\d{3}(?:/[0-9]{3})*)", text)
    crit_ok = bool(m) and CRITERION in text
    results.append(("判据编号引用 %s" % CRITERION, crit_ok, m.group(1) if m else ""))

    # 2) 各节结构
    for title, pat, note in SECTION_CHECKS:
        sec = extract_section(text, title)
        ok = sec is not None and len(sec.strip()) > 0
        if ok and pat:
            ok = re.search(pat, sec) is not None
        detail = (sec or "").strip().splitlines()
        detail = detail[0][:60] if detail else note
        results.append(("判据节 %s" % title, ok, detail))

    # 3) 输出
    for name, ok, detail in results:
        print("%s | %s | %s" % ("PASS" if ok else "FAIL", name, detail))
    passed = all(ok for _, ok, _ in results)
    print("SUMMARY | %d/%d PASS" % (sum(1 for _, ok, _ in results if ok), len(results)))
    if "--selftest" in sys.argv:
        return 0 if passed else 1
    print("判定结论（可引用）| %s" %
          ("判据结构完整，可引用作判定真源" if passed
           else "判据结构不完整，需补全后引用"))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
