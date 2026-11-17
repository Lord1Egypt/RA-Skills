#!/usr/bin/env python3
"""
quality_audit.py — 技能仓库质量审计（结构 + 跨文件一致性 + 路由完整性）

对单个 superpower 技能仓库做确定性检查，输出逐检查项 pass/warn/fail。
不依赖组织内其他脚本，可作为独立技能安装后直接运行。

用法:
    python3 quality_audit.py --repo <path>          # 文本报告
    python3 quality_audit.py --repo <path> --json    # JSON 报告
    python3 quality_audit.py --repo <path> --strict  # 有 warn 也退出 1（CI 用）

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

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
PATH_RE = re.compile(r"(?:references|scripts|assets)/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*")
# 代码块 / 行内代码：TODO 出现在其中属于「文档里引用字面量」，不是遗留待办标记。
FENCE_RE = re.compile(r"```.*?```", re.S)
CODESPAN_RE = re.compile(r"`[^`\n]*`")
EXAMPLE_SIBLING_SUFFIX = ".example"


def looks_like_file(ref):
    """悬空路由只校验**看得出是文件**的引用：末段必须带点（扩展名）。

    反例：散文里的 `references/scripts/assets`（枚举三层目录名）末段无点，不是路径引用；
    早期实现会把它判成悬空路由。注意不要按扩展名长度截断——
    `assets/Dockerfile.node.multistage` 这类长扩展名必须整段保留。
    """
    last = ref.rstrip("/").rsplit("/", 1)[-1]
    return "." in last and not last.endswith(".")
LINK_RE = re.compile(r"\]\(((?:references|scripts|assets)/[^)]+)\)")
# Q4/Q9：规范只要求 `npx skills add skills-repo/<repo>[@<name>]`，尾部 flags（如 `-g -y`）是**可选**的，
# 组织内两种风格并存。因此不要把命令锚定到行尾（`\s*$`）——那会把所有带 flags 的 README 判成缺命令。
# 整库命令用负向断言排除 `@`，避免单技能命令被误算成整库命令。
INSTALL_WHOLE_RE = re.compile(r"npx\s+skills\s+add\s+skills-repo/[a-z0-9-]+(?![\w@-])")
INSTALL_SINGLE_RE = re.compile(r"npx\s+skills\s+add\s+skills-repo/[a-z0-9-]+@[a-z0-9-]+(?![\w-])")
TODO_RE = re.compile(r"\bTODO\b")


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


def load_text(path):
    try:
        return open(path, encoding="utf-8").read()
    except OSError:
        return ""


def fm_raw(path):
    """返回 frontmatter 原始块文本（含嵌套字段），用于 source 等嵌套检测。"""
    try:
        t = open(path, encoding="utf-8").read()
    except OSError:
        return ""
    m = FM_RE.match(t)
    return m.group(1) if m else ""


def list_dir(d):
    if not os.path.isdir(d):
        return []
    return [f for f in os.listdir(d) if not f.startswith(".")]


def guess_level(repo):
    has_s = os.path.isdir(os.path.join(repo, "scripts"))
    has_a = os.path.isdir(os.path.join(repo, "assets"))
    return "A" if (has_s and has_a) else "B"


def audit(repo):
    checks = []

    def add(cid, name, status, detail):
        checks.append({"id": cid, "name": name, "status": status, "detail": detail})

    root_skill = os.path.join(repo, "SKILL.md")
    if not os.path.isfile(root_skill):
        add("root", "根 SKILL.md 存在", "fail", f"未找到 {root_skill}")
        return checks, None

    text = load_text(root_skill)
    fm = read_frontmatter(root_skill)
    # Q1/Q7 frontmatter
    missing = [k for k in ("name", "description") if not fm.get(k)]
    if missing:
        add("Q1", "Frontmatter 完整(name/description)", "fail", f"缺失: {missing}")
    else:
        add("Q1", "Frontmatter 完整(name/description)", "pass", "name/description 均存在")

    if fm.get("metadata.architecture") != "superpower" and "superpower" not in (fm.get("metadata") or ""):
        # metadata 可能在嵌套；简易判断
        if "architecture" not in text or "superpower" not in text:
            add("Q7", "声明 architecture: superpower", "fail", "根 SKILL.md 未声明 superpower")
        else:
            add("Q7", "声明 architecture: superpower", "pass", "已声明")
    else:
        add("Q7", "声明 architecture: superpower", "pass", "已声明")

    # 行数 / TODO
    lines = text.splitlines()
    if len(lines) > 150:
        add("Q7", "根 SKILL.md ≤150 行", "fail", f"当前 {len(lines)} 行")
    else:
        add("Q7", "根 SKILL.md ≤150 行", "pass", f"{len(lines)} 行")
    prose = CODESPAN_RE.sub(" ", FENCE_RE.sub(" ", text))
    if TODO_RE.search(prose):
        add("Q7", "根 SKILL.md 无 TODO", "fail", "发现遗留 TODO 标记")
    else:
        add("Q7", "根 SKILL.md 无 TODO", "pass", "无 TODO（代码块/行内代码内的字面量不计）")

    # 子技能 frontmatter (Q2/Q3/Q5)
    skills_dir = os.path.join(repo, "skills")
    sk_names = list_dir(skills_dir)
    seen = set()
    for name in sk_names:
        sp = os.path.join(skills_dir, name, "SKILL.md")
        if not os.path.isfile(sp):
            add("Q3", f"子技能 {name} 有 SKILL.md", "fail", f"缺失 {sp}")
            continue
        sfm = read_frontmatter(sp)
        sname = sfm.get("name", "")
        if sname != name:
            add("Q3", f"子技能名==目录名 ({name})", "fail", f"name='{sname}' != 目录 '{name}'")
        if sname in seen:
            add("Q2", f"技能名唯一 ({name})", "fail", "同名重复")
        seen.add(sname)
        if not sfm.get("description"):
            add("Q1", f"子技能描述 ({name})", "fail", "description 缺失")
        raw = fm_raw(sp)
        if "source:" in raw and "type:" in raw and ("repo:" in raw or "url:" in raw):
            add("Q5", f"子技能来源 ({name})", "pass", "source.type/repo(或url) 完整")
        else:
            add("Q5", f"子技能来源 ({name})", "fail", "source 字段缺失或类型不明")

    # 路由完整性：孤儿 + 悬空
    for layer in ("references", "scripts", "assets"):
        d = os.path.join(repo, layer)
        for f in list_dir(d):
            fp = os.path.join(layer, f)
            if fp not in text and f not in text:
                add("route", f"路由索引 ({fp})", "warn", "文件存在但根 SKILL.md 未索引（孤儿）")
    for m in sorted(set(PATH_RE.findall(text) + LINK_RE.findall(text))):
        if not looks_like_file(m):
            continue
        full = os.path.join(repo, m)
        if os.path.exists(full):
            continue
        # 组织约定：`X.example.<ext>` 是随库发布的模板，`X.<ext>` 由用户复制后自建（运行时产物）。
        # 存在 .example 兄弟文件时不算悬空，降级为 warn 以免把"待用户创建"误报成断链。
        stem, ext = os.path.splitext(full)
        if os.path.exists(stem + EXAMPLE_SIBLING_SUFFIX + ext) or os.path.exists(full + EXAMPLE_SIBLING_SUFFIX):
            add("route", f"运行时产物路由 ({m})", "warn", "磁盘不存在，但有 .example 模板兄弟文件（由用户复制生成）")
            continue
        add("route", f"悬空路由 ({m})", "fail", f"根 SKILL.md 引用但磁盘不存在: {m}")

    # README 双安装 + 清单一致性 (Q4/Q9/W1)
    rd = os.path.join(repo, "README.md")
    rtext = load_text(rd)
    if not rtext:
        add("Q9", "README 存在", "fail", "未找到 README.md")
    else:
        if not INSTALL_WHOLE_RE.search(rtext):
            add("Q9", "整库安装命令", "fail", "缺少 `npx skills add skills-repo/<repo>`")
        else:
            add("Q9", "整库安装命令", "pass", "存在")
        if not INSTALL_SINGLE_RE.search(rtext):
            add("Q9", "单技能安装命令", "fail", "缺少 `npx skills add skills-repo/<repo>@<name>`")
        else:
            add("Q9", "单技能安装命令", "pass", "存在")
        missing_tab = [n for n in sk_names if n and n not in rtext]
        if missing_tab:
            add("W1", "README 清单含全部子技能", "warn", f"未列出的子技能: {missing_tab}")
        else:
            add("W1", "README 清单含全部子技能", "pass", f"全部 {len(sk_names)} 个已列出")

    return checks, guess_level(repo)


def main():
    ap = argparse.ArgumentParser(description="技能仓库质量审计")
    ap.add_argument("--repo", default=".", help="仓库路径（默认当前目录）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="有 warn 也退出 1")
    args = ap.parse_args()

    repo = os.path.abspath(os.path.expanduser(args.repo))
    if not os.path.isdir(repo):
        print(f"[ERROR] 仓库不存在: {repo}", file=sys.stderr)
        return 2

    checks, level = audit(repo)
    n_pass = sum(c["status"] == "pass" for c in checks)
    n_warn = sum(c["status"] == "warn" for c in checks)
    n_fail = sum(c["status"] == "fail" for c in checks)

    if args.json:
        out = {
            "repo": repo,
            "level_guess": level,
            "summary": {"pass": n_pass, "warn": n_warn, "fail": n_fail},
            "checks": checks,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"== quality_audit: {os.path.basename(repo)} (Level 猜测 {level}) ==")
        for c in checks:
            mark = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}[c["status"]]
            print(f"  [{mark}] {c['id']:6} {c['name']} — {c['detail']}")
        print(f"-- 汇总: pass={n_pass} warn={n_warn} fail={n_fail}")

    if n_fail > 0:
        return 1
    if args.strict and n_warn > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
