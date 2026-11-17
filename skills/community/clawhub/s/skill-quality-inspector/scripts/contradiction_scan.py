#!/usr/bin/env python3
"""
contradiction_scan.py — 技能仓库矛盾点扫描

检测仓库内部自相矛盾的地方：断链、重复标题、数字对账失败、术语漂移。
跨文件语义级"规则冲突"仍需人工，本脚本只标记可疑信号。

用法:
    python3 contradiction_scan.py --repo <path> [--json] [--strict]

退出码:
    0  无 fail（--strict 下也无 warn）
    1  存在 fail；或 --strict 且存在 warn
    2  参数/路径错误
"""
import argparse
import json
import os
import re
import sys

MD_RE = re.compile(r"\.md$")
# 只校验真正的 Markdown 链接 [文本](路径)；不再用裸路径正则匹配，
# 避免把方法论文档中的示例/说明性路径（如 `scripts/x.py`、references/...）误判为断链。
LINK_RE = re.compile(r"\]\(((?:references|scripts|assets)/[^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$", re.MULTILINE)
NUMERIC_RE = re.compile(r"(\d+)\s*(?:个)?\s*(子技能|references|篇\s*references|脚本|assets|个子技能)")
# 规范词 → 非规范写法（仅收录真正的拼写/写法错误，不收录同义正确术语）
# 注意：误报同属 bug。'路由表' 是 superpower 根 SKILL.md 路由表的标准叫法，
# 'playbook' 是方法论文档的英文标准词，二者均非笔误，不得作为漂移信号。
TERM_MAP = {
    "Level A": [r"\bA\s*级\b", r"\bA级\b", r"\bLv\s*A\b"],
    "Level B": [r"\bB\s*级\b", r"\bB级\b", r"\bLv\s*B\b"],
}


def iter_md(repo):
    repo_abs = os.path.abspath(repo)
    for root, dirs, files in os.walk(repo):
        if ".git" in root.split(os.sep):
            continue
        # 不进入被扫描根目录直属的 tests/（本工具的自检合成样本，非仓库内容）；
        # 从 dirs 裁剪以阻止 os.walk 继续下钻。若用户显式 --repo tests/sample_bad，
        # 该路径自身不含直属 tests/ 子目录，仍会被正常扫描。
        if root == repo_abs and "tests" in dirs:
            dirs.remove("tests")
        for f in files:
            if MD_RE.search(f):
                yield os.path.join(root, f)


def scan(repo):
    findings = []
    rel = lambda p: os.path.relpath(p, repo)

    # 1. 断链（仅校验 Markdown 链接 [文本](路径) 中的真实引用）
    for p in iter_md(repo):
        txt = open(p, encoding="utf-8", errors="ignore").read()
        for m in set(LINK_RE.findall(txt)):
            if not os.path.exists(os.path.join(repo, m)):
                findings.append({"type": "broken_link", "file": rel(p), "detail": f"引用不存在: {m}", "severity": "fail"})

    # 2. 重复标题（同文件内）
    for p in iter_md(repo):
        txt = open(p, encoding="utf-8", errors="ignore").read()
        seen = {}
        for m in HEADING_RE.finditer(txt):
            h = m.group(2).strip()
            if h in seen:
                findings.append({"type": "duplicate_heading", "file": rel(p), "detail": f"重复标题: '{h}'", "severity": "warn"})
            seen[h] = True

    # 3. 数字对账（仅校验仓库显式声明结构数的位置：README.md 与根 SKILL.md）
    #    不在 references/、skills/、decisions/ 等文档里逐项比对——那些是示例/历史数字，
    #    会被误判为"声称数"造成大量误报（误报同属 bug）。
    def count_dir(layer):
        d = os.path.join(repo, layer)
        if not os.path.isdir(d):
            return 0
        return len([x for x in os.listdir(d) if not x.startswith(".")])

    actual = {
        "子技能": count_dir("skills"),
        "references": count_dir("references"),
        "脚本": count_dir("scripts"),
        "assets": count_dir("assets"),
    }
    for name in ("README.md", "SKILL.md"):
        p = os.path.join(repo, name)
        if not os.path.isfile(p):
            continue
        txt = open(p, encoding="utf-8", errors="ignore").read()
        for m in NUMERIC_RE.finditer(txt):
            claimed = int(m.group(1))
            label = m.group(2).replace(" ", "")
            key = {"子技能": "子技能", "references": "references", "篇references": "references",
                   "脚本": "脚本", "assets": "assets", "个子技能": "子技能"}.get(label)
            if key and actual.get(key) is not None and claimed != actual[key]:
                findings.append({"type": "numeric_mismatch", "file": rel(p),
                                 "detail": f"声称 {claimed} 个{key}，实际目录 {actual[key]} 个", "severity": "fail"})

    # 4. 术语漂移
    for p in iter_md(repo):
        txt = open(p, encoding="utf-8", errors="ignore").read()
        for canon, pats in TERM_MAP.items():
            for pat in pats:
                if re.search(pat, txt):
                    findings.append({"type": "term_drift", "file": rel(p),
                                     "detail": f"非规范写法命中（建议统一为 '{canon}'）: /{pat}/", "severity": "warn"})
                    break

    return findings


def main():
    ap = argparse.ArgumentParser(description="技能仓库矛盾点扫描")
    ap.add_argument("--repo", default=".", help="仓库路径")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="有 warn 也退出 1")
    args = ap.parse_args()

    repo = os.path.abspath(os.path.expanduser(args.repo))
    if not os.path.isdir(repo):
        print(f"[ERROR] 仓库不存在: {repo}", file=sys.stderr)
        return 2

    findings = scan(repo)
    n_fail = sum(f["severity"] == "fail" for f in findings)
    n_warn = sum(f["severity"] == "warn" for f in findings)

    if args.json:
        print(json.dumps({"repo": repo, "summary": {"fail": n_fail, "warn": n_warn},
                          "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print(f"== contradiction_scan: {os.path.basename(repo)} ==")
        if not findings:
            print("  无 findings")
        for f in findings:
            mark = "FAIL" if f["severity"] == "fail" else "WARN"
            print(f"  [{mark}] {f['type']} @{f['file']} — {f['detail']}")
        print(f"-- 汇总: fail={n_fail} warn={n_warn}")

    if n_fail > 0:
        return 1
    if args.strict and n_warn > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
