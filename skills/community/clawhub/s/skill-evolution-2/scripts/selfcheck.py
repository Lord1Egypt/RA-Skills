#!/usr/bin/env python3
"""技能进化（知行环）· 包体自检

只读审计，不修改任何文件。用于改动 skill 之后快速回归，
也可在分发前确认包体干净、文档自洽。

检查项：
  1. 身份契约（name 必须是 skill-evolution，不可改）
  2. 必备文件齐全
  3. 圈码编号一致性（七步闭环语义，禁止旧的 Step N 编号残留）
  4. Markdown 代码围栏奇偶（防止文档结构被截断）
  5. README 内部锚点有效
  6. README 目录树与实际文件一致
  7. 换行符统一（包内约定 LF）
  8. 无 __pycache__ / .pyc 等打包垃圾
  9. 无本机绝对路径泄漏（个人目录 / 用户名）
 10. 跨副本哈希一致（需 --copy 指定副本目录）

用法：
  python selfcheck.py
  python selfcheck.py --copy <另一份副本目录>          # 可重复
  python selfcheck.py --copy <仓库副本> --copy <项目 .wiki>
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path

SKILL_NAME = "skill-evolution"

REQUIRED = [
    "SKILL.md",
    "README.md",
    "scripts/install.py",
    "scripts/wiki_init.py",
    "scripts/wiki_init.sh",
    "scripts/wiki_init.ps1",
    "scripts/wiki_remind.py",
    "scripts/wiki_remind.sh",
    "scripts/selfcheck.py",
    "references/rsi-framework.md",
    "references/design-playbook.md",
    "references/workflow.md",
    "references/anti-patterns.md",
    "references/platforms.md",
    "references/automation.md",
    "references/templates.md",
    "references/CLAUDE.template.md",
    "references/AGENTS.template.md",
    "assets/hooks/claude-code-settings.json",
    "assets/hooks/claude-code-settings.windows.json",
]

TEXT_SUFFIX = {".md", ".py", ".sh", ".ps1", ".json", ".txt", ".yml", ".yaml"}

# 本机路径泄漏：绝对个人目录（占位符写法不算）
USER_DIR_RE = re.compile(
    r"(?:[A-Za-z]:[\\/]Users[\\/](?P<win>[^\\/\s\"'`)]+)"
    r"|/(?:Users|home)/(?P<unix>[^/\s\"'`)]+))"
)
PLACEHOLDER_OK = {
    "xxx", "xx", "x", "user", "username", "yourname", "name", "demo",
    "example", "exampleuser", "someone", "test", "<user>", "administrator.example",
}

ok_count = 0
problems = []


def ok(msg):
    global ok_count
    ok_count += 1
    print(f"  [OK]   {msg}")


def bad(msg, detail=""):
    problems.append(msg if not detail else f"{msg} | {detail}")
    print(f"  [FAIL] {msg}" + (f"  → {detail}" if detail else ""))


def read(p: Path) -> str:
    return p.read_bytes().decode("utf-8", errors="replace")


def check_identity(root: Path):
    print("\n[1] 身份契约")
    p = root / "SKILL.md"
    if not p.exists():
        bad("SKILL.md 不存在")
        return
    head = read(p)[:800]
    m = re.search(r"^name:\s*(\S+)", head, re.M)
    if not m:
        bad("SKILL.md frontmatter 缺少 name")
    elif m.group(1) != SKILL_NAME:
        bad(f"name 契约被改：{m.group(1)}（必须是 {SKILL_NAME}）")
    else:
        ok(f"name: {SKILL_NAME}（目录 / .wiki / hook 依赖此契约）")
    if re.search(r"^display_name:", head, re.M):
        ok("中文显示名 display_name 存在")
    else:
        bad("缺少 display_name（中文显示名）")


def check_required(root: Path):
    print("\n[2] 必备文件")
    missing = [f for f in REQUIRED if not (root / f).exists()]
    if missing:
        for f in missing:
            bad(f"缺失 {f}")
    else:
        ok(f"{len(REQUIRED)} 个必备文件齐全")


def doc_files(root: Path):
    return sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in TEXT_SUFFIX - {".json"}
        and p.suffix.lower() == ".md"
    )


def check_numbering(root: Path):
    print("\n[3] 圈码编号一致性")
    stepn = []
    gate_bad = []
    # 人工门控在闭环中固定为 ⑤，不得被写成 ④（或裸 4）。
    # 负向后顾同时排除两类误伤：小数点（"1.4 门控"）与 RSI 自主权等级（"L4 门控验证"）。
    gate_re = re.compile(r"(?<![\d.L])[④4]\s*(?:[【\[]?人工[】\]]?)?\s*门控")
    for p in doc_files(root):
        for i, line in enumerate(read(p).splitlines(), 1):
            if re.search(r"Step\s+\d", line):
                stepn.append(f"{p.relative_to(root)}:{i}")
            if gate_re.search(line):
                gate_bad.append(f"{p.relative_to(root)}:{i}")
    if stepn:
        for s in stepn:
            bad("残留旧编号 Step N", s)
    else:
        ok("无旧『Step N』编号残留")
    if gate_bad:
        for s in gate_bad:
            bad("门控编号误标为 ④（应为 ⑤）", s)
    else:
        ok("门控编号统一为 ⑤")
    # 至少存在一处完整闭环链，确保编号语义被定义
    chain = re.compile(r"①.{0,12}②.{0,12}③.{0,12}④.{0,12}⑤.{0,12}⑥.{0,12}⑦")
    has = any(chain.search(read(p)) for p in doc_files(root))
    if has:
        ok("存在完整七步闭环链定义（①→⑦）")
    else:
        bad("未找到完整的 ①→⑦ 闭环链定义")


def check_fences(root: Path):
    print("\n[4] 代码围栏奇偶")
    badf = []
    for p in doc_files(root):
        n = sum(1 for line in read(p).splitlines() if line.startswith("```"))
        if n % 2:
            badf.append(f"{p.relative_to(root)}({n})")
    if badf:
        for f in badf:
            bad("围栏数为奇数，文档结构可能被截断", f)
    else:
        ok(f"{len(doc_files(root))} 个文档围栏全部闭合")


def slug(h: str) -> str:
    s = h.strip().lower()
    s = re.sub(r"[^\w\u4e00-\u9fff\s-]", "", s)
    return s.replace(" ", "-")


def check_anchors(root: Path):
    print("\n[5] README 内部锚点")
    p = root / "README.md"
    if not p.exists():
        bad("README.md 不存在")
        return
    t = read(p)
    anchors = {slug(l.lstrip("#")) for l in t.splitlines() if l.startswith("#")}
    links = re.findall(r"\]\(#([^)]+)\)", t)
    dead = [l for l in links if l not in anchors]
    if dead:
        for d in dead:
            bad("锚点失效", "#" + d)
    else:
        ok(f"{len(links)} 个内部链接全部有效")


def check_tree(root: Path):
    print("\n[6] README 目录树 vs 实际文件")
    p = root / "README.md"
    if not p.exists():
        return
    t = read(p).splitlines()
    start = next((i for i, l in enumerate(t) if l.strip().rstrip("/") == SKILL_NAME and l.strip().endswith("/")), None)
    if start is None:
        bad("README 未找到目录树区块")
        return
    end = next((i for i in range(start + 1, len(t)) if t[i].startswith("```")), len(t))
    block = "\n".join(t[start:end])
    documented = set(re.findall(r"[A-Za-z0-9_.\-]+\.(?:md|py|sh|ps1|json)", block))
    actual = {q.name for q in root.rglob("*") if q.is_file()}
    miss = sorted(actual - documented)
    extra = sorted(documented - actual)
    if miss or extra:
        for f in miss:
            bad("目录树漏记", f)
        for f in extra:
            bad("目录树多记（实际不存在）", f)
    else:
        ok(f"目录树与磁盘一致（{len(actual)} 个文件）")


def check_eol(root: Path):
    print("\n[7] 换行符统一")
    crlf = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_SUFFIX:
            if b"\r\n" in p.read_bytes():
                crlf.append(p.relative_to(root).as_posix())
    if crlf:
        for f in crlf:
            bad("含 CRLF（包内约定 LF）", f)
    else:
        ok("全部文本文件为 LF")


def check_junk(root: Path):
    print("\n[8] 打包垃圾")
    junk = [
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if "__pycache__" in p.parts or p.suffix in {".pyc", ".pyo"} or p.name in {".DS_Store", "Thumbs.db"}
    ]
    if junk:
        for j in junk[:10]:
            bad("混入打包垃圾", j)
    else:
        ok("无 __pycache__ / .pyc / 系统垃圾文件")


def check_leaks(root: Path):
    print("\n[9] 本机路径泄漏")
    leaks = []
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIX:
            continue
        for i, line in enumerate(read(p).splitlines(), 1):
            for m in USER_DIR_RE.finditer(line):
                name = (m.group("win") or m.group("unix") or "").lower()
                if name in PLACEHOLDER_OK or name.startswith("<"):
                    continue
                leaks.append(f"{p.relative_to(root)}:{i} → {m.group(0)}")
    if leaks:
        for l in leaks[:15]:
            bad("疑似本机个人目录", l)
    else:
        ok("未发现本机用户名 / 个人目录绝对路径")


def check_copies(root: Path, copies):
    print("\n[10] 跨副本哈希一致")
    if not copies:
        print("  [skip] 未指定 --copy，跳过")
        return
    mine = {p.relative_to(root).as_posix(): hashlib.md5(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file()}
    for c in copies:
        c = Path(c)
        if not c.exists():
            bad("副本目录不存在", str(c))
            continue
        theirs = {p.relative_to(c).as_posix(): hashlib.md5(p.read_bytes()).hexdigest()
                  for p in c.rglob("*") if p.is_file()}
        common = set(mine) & set(theirs)
        diff = sorted(f for f in common if mine[f] != theirs[f])
        only_mine = sorted(set(mine) - set(theirs))
        if diff:
            for f in diff:
                bad(f"副本内容不一致：{c}", f)
        else:
            note = f"（副本缺 {len(only_mine)} 个文件，属正常子集）" if only_mine else ""
            ok(f"{c} → 共有 {len(common)} 个文件内容一致{note}")


def main() -> int:
    ap = argparse.ArgumentParser(description="技能进化（知行环）包体自检（只读）")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent),
                    help="skill 根目录，默认取本脚本的上级目录")
    ap.add_argument("--copy", action="append", default=[],
                    help="要比对哈希的副本目录，可重复指定")
    a = ap.parse_args()
    root = Path(a.root)
    if not root.is_dir():
        print(f"目录不存在：{root}")
        return 2

    print(f"自检目标：{root}")
    check_identity(root)
    check_required(root)
    check_numbering(root)
    check_fences(root)
    check_anchors(root)
    check_tree(root)
    check_eol(root)
    check_junk(root)
    check_leaks(root)
    check_copies(root, a.copy)

    print("\n" + "=" * 52)
    if problems:
        print(f"结果：{len(problems)} 项异常（通过 {ok_count} 项）")
        return 1
    print(f"结果：全部通过（{ok_count} 项）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
