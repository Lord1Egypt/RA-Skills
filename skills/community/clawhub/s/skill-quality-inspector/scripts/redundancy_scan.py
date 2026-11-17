#!/usr/bin/env python3
"""
redundancy_scan.py — 组织内技能冗余扫描

跨仓库检测重复/重叠的技能名、近重描述、路由关键词打架。
所有去重建议都只是"信号"，是否合并/下线由人工按"只增不减"铁律裁决。

用法:
    python3 redundancy_scan.py --org <org-root> [--json] [--strict]

退出码:
    0  无 fail（--strict 下也无 warn）
    1  存在 fail（如同名冲突）；或 --strict 且存在 warn
    2  参数/路径错误
"""
import argparse
import json
import os
import re
import sys

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
SEP_RE = re.compile(r"^[\s|:-]+$")
CJK = re.compile(r"[一-鿿]")


def read_frontmatter(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return {}
    m = FM_RE.match(text)
    if not m:
        return {}
    out = {}
    for raw in m.group(1).splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line or raw.startswith((" ", "\t")):
            continue
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip().strip("\"'")
    return out


def tokens(s):
    s = (s or "").lower()
    toks = set(re.findall(r"[a-z0-9]+", s))
    for w in re.findall(r"[一-鿿]+", s):
        for i in range(len(w) - 1):
            toks.add(w[i:i + 2])
    return toks


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def routing_keywords(repo):
    """从根 SKILL.md 路由表抽取 grep 关键词 token 集合。"""
    p = os.path.join(repo, "SKILL.md")
    if not os.path.isfile(p):
        return set()
    txt = open(p, encoding="utf-8", errors="ignore").read()
    kws = set()
    for line in txt.splitlines():
        if not ROW_RE.match(line) or SEP_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        last = cells[-1]
        if "关键词" in last or "grep" in last.lower():
            continue  # 表头行
        kws |= tokens(last)
    return kws


def collect(repos_root):
    repos = []
    for name in sorted(os.listdir(repos_root)):
        d = os.path.join(repos_root, name)
        if not os.path.isdir(d) or name.startswith("."):
            continue
        skills_dir = os.path.join(d, "skills")
        if not os.path.isdir(skills_dir):
            continue
        skills = []
        for sn in sorted(os.listdir(skills_dir)):
            sp = os.path.join(skills_dir, sn, "SKILL.md")
            if not os.path.isfile(sp):
                continue
            fm = read_frontmatter(sp)
            skills.append({"name": sn, "description": fm.get("description", "")})
        if skills:
            repos.append({"repo": name, "skills": skills, "keywords": routing_keywords(d)})
    return repos


def scan(repos_root):
    repos = collect(repos_root)
    findings = []

    # 1. 跨仓重名
    name_map = {}
    for r in repos:
        for s in r["skills"]:
            name_map.setdefault(s["name"], []).append(r["repo"])
    for nm, owners in name_map.items():
        if len(owners) > 1:
            findings.append({"type": "duplicate_name", "skill": nm,
                             "detail": f"同名技能出现在多个仓库: {owners}", "severity": "fail",
                             "repos": owners})

    # 2. 近重描述（不同仓）
    pairs = []
    for i in range(len(repos)):
        for j in range(i + 1, len(repos)):
            for a in repos[i]["skills"]:
                for b in repos[j]["skills"]:
                    jc = jaccard(tokens(a["description"]), tokens(b["description"]))
                    if jc >= 0.6:
                        pairs.append({"type": "near_dup_desc", "repos": [repos[i]["repo"], repos[j]["repo"]],
                                      "skills": [a["name"], b["name"]], "jaccard": round(jc, 2),
                                      "severity": "warn"})
    findings.extend(pairs)

    # 3. 关键词打架（仓间）
    for i in range(len(repos)):
        for j in range(i + 1, len(repos)):
            inter = repos[i]["keywords"] & repos[j]["keywords"]
            if len(inter) >= 3:
                findings.append({"type": "keyword_overlap", "repos": [repos[i]["repo"], repos[j]["repo"]],
                                 "shared": sorted(inter), "severity": "warn"})

    return findings, repos


def main():
    ap = argparse.ArgumentParser(description="组织内技能冗余扫描")
    ap.add_argument("--org", required=True, help="组织根目录（含各仓库子目录）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="有 warn 也退出 1")
    args = ap.parse_args()

    if not os.path.isdir(args.org):
        print(f"[ERROR] 组织根目录不存在: {args.org}", file=sys.stderr)
        return 2

    findings, repos = scan(args.org)
    n_fail = sum(f["severity"] == "fail" for f in findings)
    n_warn = sum(f["severity"] == "warn" for f in findings)

    if args.json:
        print(json.dumps({"org": args.org, "repos_scanned": len(repos),
                          "summary": {"fail": n_fail, "warn": n_warn},
                          "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print(f"== redundancy_scan: 扫描 {len(repos)} 个仓库 ==")
        if not findings:
            print("  无冗余信号")
        for f in findings:
            mark = "FAIL" if f["severity"] == "fail" else "WARN"
            extra = ""
            if f["type"] == "keyword_overlap":
                extra = f" 共享关键词: {f['shared']}"
            elif f["type"] == "near_dup_desc":
                extra = f" Jaccard={f['jaccard']} skills={f['skills']}"
            print(f"  [{mark}] {f['type']} {f.get('repos')}{extra}")
        print(f"-- 汇总: fail={n_fail} warn={n_warn}")

    if n_fail > 0:
        return 1
    if args.strict and n_warn > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
