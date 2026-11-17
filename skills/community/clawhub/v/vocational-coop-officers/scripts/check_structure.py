#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VCO 技能包结构自检（无第三方依赖）。

用法：
    python scripts/check_structure.py            # 检查本技能包
    python scripts/check_structure.py <包目录>    # 检查指定目录

检查项对应 M3 接口校验中可自动化的部分：
  A1 三层结构存在 / A5 域间逻辑流 / A6 依赖拓扑摘要
  B1 单元 5 字段 / B2 依赖格式 / B3 元操作 / B4 无孤立 / B5 入口占比
  C1-C5 槽位齐全 / E1-E2 范本索引与子文件
  两级目录深度 / frontmatter 必填字段
"""
import re
import sys
from pathlib import Path

UUID = re.compile(r"^(X0|N[1-4]|B(?:[1-9]|10))-\d{2}$")
META = re.compile(r"^[SCAOIG]（")
DEP = re.compile(r"^(无（入口）|(X0|N[1-4]|B(?:[1-9]|10))-\d{2}(, ?(X0|N[1-4]|B(?:[1-9]|10))-\d{2})*)$")

ok, warn, bad = [], [], []


def p(msg):
    ok.append(msg)


def w(msg):
    warn.append(msg)


def f(msg):
    bad.append(msg)


def read(pth):
    return pth.read_text(encoding="utf-8", errors="replace")


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    d = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip()] = v.split("#")[0].strip()
    return d


def _report():
    print("=" * 56)
    print("VCO 结构自检：PASS %d / WARN %d / FAIL %d" % (len(ok), len(warn), len(bad)))
    print("=" * 56)
    for m in bad:
        print("[FAIL]", m)
    for m in warn:
        print("[WARN]", m)
    if not bad:
        print("结果：全部通过")
    return 1 if bad else 0


def main(root):
    skill = root / "SKILL.md"
    refs = root / "references"

    # ---- 基础结构 ----
    if not skill.is_file():
        f("SKILL.md 缺失")
        return _report()
    if not refs.is_dir():
        f("references/ 目录缺失")
        return _report()
    for need in ("VCO-catalog.md", "VCO-requirements.md", "VCO-exemplars.md"):
        if not (refs / need).is_file():
            f("核心索引缺失：%s" % need)
            return _report()
    p("SKILL.md 存在")

    fm = frontmatter(read(skill))
    for k in ("description", "description_zh", "description_en", "version", "author"):
        (p if fm.get(k) else f)("frontmatter %s" % k)
    if fm.get("name") and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", fm["name"]):
        f("name 非 kebab-case")
    if fm.get("version") and not re.fullmatch(r"\d+\.\d+\.\d+", fm["version"]):
        f("version 非 x.y.z")

    # ---- 两级目录 ----
    for x in root.rglob("*"):
        if x.is_file() and len(x.relative_to(root).parts) > 2:
            f("目录层级超限: %s" % x.relative_to(root).as_posix())
    p("目录深度检查完成")

    # ---- 索引文件 ----
    idx = ["VCO-catalog.md", "VCO-requirements.md", "VCO-exemplars.md"]
    for n in idx:
        (p if (refs / n).is_file() else f)("索引文件 %s" % n)

    # ---- 范本子文件 ----
    doms = ["X0", "N1", "N2", "N3", "N4", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"]
    exemplars = list(refs.glob("VCO-*-*范本.md"))
    if len(exemplars) >= 15:
        p("域范本文件 %d 个" % len(exemplars))
    else:
        f("域范本文件不足：%d/15" % len(exemplars))
    for d in doms:
        if not list(refs.glob("VCO-%s-*范本.md" % d)):
            f("缺少域范本：%s" % d)

    cat = read(refs / "VCO-catalog.md")
    if "域间逻辑流声明" in cat:
        p("catalog 域间逻辑流")
    else:
        f("catalog 缺域间逻辑流")
    if "依赖拓扑摘要" in cat:
        p("catalog 依赖拓扑摘要")
    else:
        f("catalog 缺依赖拓扑摘要")

    # ---- 解析 catalog 单元行 ----
    units = {}
    for line in cat.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) >= 6 and UUID.match(cells[0]):
            units[cells[0]] = cells
    if len(units) == 125:
        p("catalog 单元数 125")
    else:
        f("catalog 单元数 %d（应 125）" % len(units))

    entry = 0
    for uid, c in units.items():
        deps = c[3]
        if deps.startswith("无"):
            entry += 1
        if not DEP.match(deps):
            f("%s 依赖格式异常: %s" % (uid, deps))
        if not META.match(c[4]):
            f("%s 元操作异常: %s" % (uid, c[4]))
    for uid, c in units.items():
        if c[3].startswith("无"):
            continue
        for d in [t.strip() for t in c[3].split(",")]:
            if d not in units:
                f("%s 依赖指向未定义单元: %s" % (uid, d))
    if entry and entry <= len(units) * 0.3:
        p("入口单元 %d（≤30%%）" % entry)
    else:
        f("入口单元 %d 超限" % entry)

    # ---- 身份 ----
    names = []
    for uid, c in units.items():
        for n in re.split(r"[×]", c[5].replace("🎭", "")):
            n = n.strip()
            if n.startswith("协同"):
                n = n[2:].strip()
            if n:
                names.append(n)
    dup = {n for n in names if names.count(n) > 1}
    if len(names) >= 375 and not dup:
        p("身份 %d 个，唯一" % len(names))
    else:
        f("身份数 %d，重名 %d 个：%s" % (len(names), len(dup), ",".join(list(dup)[:5])))

    # ---- requirements ----
    rq = read(refs / "VCO-requirements.md")
    secs = re.findall(r"^#### ((?:X0|N[1-4]|B(?:[1-9]|10))-\d{2}) .+$", rq, re.M)
    if len(secs) == 125 and len(set(secs)) == 125:
        p("requirements 单元节 125")
    else:
        f("requirements 单元节 %d（应 125）" % len(secs))
    for need in ("必选组件", "可选组件", "组装顺序", "约束", "格式"):
        cnt = rq.count("- **%s**:" % need)
        if cnt >= 125:
            p("requirements %s %d 处" % (need, cnt))
        else:
            f("requirements %s 仅 %d 处" % (need, cnt))

    # ---- 范本覆盖 ----
    ex = read(refs / "VCO-exemplars.md")
    rows = len(re.findall(r"^\| (?:X0|N[1-4]|B(?:[1-9]|10))-\d{2} \|", ex, re.M))
    (p if rows >= 125 else f)("范本索引行 %d" % rows)

    return _report()


if __name__ == "__main__":
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    sys.exit(main(base))
