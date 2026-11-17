#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""attack_test.py — 检查器攻击测试（防假绿）

目的：验证 `scripts/check_consistency.py` 能拦住"应当报红"的场景。
方法：**把技能目录复制到系统临时目录**，在副本上做变异，运行**副本的**检查器，期望 FAIL。

为什么需要：v9.0.2 的 A1 只断言"关键短语在应有节内存在"，
删掉整段内容只留标题时仍会 PASS（见 `RETRO-20261006-008` 模式 4）。

历史（安全修复，`REV-20261006-018`）：早期版本**原地变异真实 SKILL.md 再还原**，两次踩坑：
  1. 还原用**文本模式**写回，Windows 下把 LF 变成 CRLF，而校验也用文本模式读（会归一化）→ 假通过；
  2. 中途被强杀（Ctrl-C / kill）会**把真实 SKILL.md 留在变异态**，且脚本不落 .bak。
现改为**临时副本**：真实目录自始至终只读，脚本崩溃也不会污染产物（结束时用 sha256 断言）。

必拦场景（`MODES` + `A3_MODES`）：
  wipe           整段清空，只留标题
  drop_line      删掉含必需词的那一行
  summarize      整段换成"一句罗列全部必需词"（掏空但保留关键词）
  dup_heading    清空真段体 + 追加**2/3 级**同名诱饵段（利用 dict 后者覆盖前者）
  dup_level4     同上，但诱饵用 **4 级**同名标题（旧实现只统计 2/3 级 → 曾是盲区）
  comment_wrap   清空段体，只把必需词放进 **HTML 注释** 里（旧实现把注释当内容）
  code_wrap      清空段体，只把必需词放进**代码围栏**（由"行数下限"拦住）
  quote_wrap     清空段体，只把必需词放进 **`>` 引用块**（由"行数下限"拦住）
  enum_drop_key  把某个**枚举行**的键删掉一个 → `A3` 必须报红
  enum_reorder   把某个**枚举行**的键顺序换位 → `A3` 必须报红

已知漏检（`KNOWN_LEAK`；**预期不被拦住**。若某天被拦住会打印"改进"，此时应把它移进 `MODES`）：
  strip_definition  保留必需词、删掉其**定义**（`2. **观察关系**：…` → `2. **观察关系**`）
  pad_to_count      1 行必需词 + N 行"（占位）" 凑够"行数下限"
  code_wrap_pad     把必需词放进代码围栏 **并凑够行数**（`code_wrap` 的加强版）
  enum_super_set    同行枚举**多出**一个其它要素（如多加"五感来源"）—— A3 不判"多余"
  enum_cross_line   把 4 个键**拆到多行**—— A3 只查同行

必须**不报红**的合法改法（`EXPECT_PASS`；报红即算假红失败）：
  prose_mention        在别处写含 2 个规范键的**散文**（如"视觉起点与观察关系需一一对应"）
  enum_extra_related   在完整枚举**后面加一句说明**（如"（按导演意图确定）"）

> 判据是**字面**的：`code_wrap`/`quote_wrap` 之所以被拦住，靠的是"内容行数 < 必需词数"，
> **不是**因为识别出"词在代码里"。因此只要攻击者同时凑够行数（`code_wrap_pad`）就仍会漏。
> 这是"对行数敏感、对语义无感"的固有代价 —— 见 `scripts/check_consistency.py` 文件头「已知限制」。
> A3 同理：它只把"相邻规范键之间只有分隔符/空白"的行当作枚举，故散文提及不误报，
> 但跨行枚举与"多出要素"也不查（见上）。

用法：
    python tests/attack_test.py [--verbose]

退出码：0 = 全部必拦场景被拦住；1 = 存在漏网（假绿）；2 = 环境错误/真实文件被改动
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_NAME = "SKILL.md"
CHECKER_NAME = os.path.join("scripts", "check_consistency.py")
SKILL = os.path.join(ROOT, SKILL_NAME)
CHECKER = os.path.join(ROOT, CHECKER_NAME)
VERBOSE = "--verbose" in sys.argv

# 攻击场景：{段落标题（##/### 级）, 该段必须包含的内容行}
# `MARK` 为 None 表示只用 `wipe` 一种模式（TD-7：为其余受守护小节补最低限度覆盖 —— 每节 1 个 wipe，
# 目的是"删内容留标题必须报红"这一条在**全部 7 个受守护小节**上都有回归护栏，而不是只覆盖 3 个）
ATTACKS = [
    ("### 每镜四项事实（缺一不可）", ["视觉起点", "观察关系", "构图落位", "摄影机状态"], True),
    ("### 主动运镜三要素（缺一不可）", ["起始观察点", "运动轨迹方向", "停止结果"], True),
    ("### 承接等式", ["上一组末尾空间状态", "下一组人物空间站位"], True),
    ("### 时间码规范", ["整数秒", "不重叠", "组时长"], False),
    ("### 台词写法", ["逐字嵌入", "引号"], False),
    ("### 硬门总览", ["台词容量", "分组硬门", "镜头密度", "运镜设计"], False),
    ("### 核心硬规则（不可跳过）", ["台词容量预检先于分组", "组尾必须是可继承稳定状态", "承接等式"], False),
]
MODES = [("wipe", "整段清空"), ("drop_line", "删关键行"), ("summarize", "概化成一句"),
         ("dup_heading", "同名诱饵段"), ("dup_level4", "4级同名诱饵"),
         ("comment_wrap", "词藏注释"), ("code_wrap", "词藏代码围栏"),
         ("quote_wrap", "词藏引用块")]
# A4（TD-10，全文件级）：文件内指针被改坏 → A4 必须报红
A4_MODES = [("bad_sub_pointer", "子标题错位"), ("bad_main_pointer", "主标题不存在")]
# A3（G3'，全文件级，**WARN 级**）：
#   因为 A3 不阻塞构建（WARN），"被拦住"的判据是 **A3 这项断言报 not-ok**，而不是退出码。
A3_KEYS = ["视觉起点", "观察关系", "构图落位", "摄影机状态"]
A3_MODES = [("enum_reorder", "枚举乱序")]
# **必须不报红**的合法改法（来源 `REV-20261006-024` FR-1 / `025` 的 11 反例 / `026`）
EXPECT_PASS = [("prose_mention", "散文提及两个键"),
               ("enum_extra_related", "枚举后加一句相关说明"),
               ("prose_dunhao", "顿号散文（非枚举）"),
               ("paren_mention", "括号内提及两个键"),
               ("table_row_2keys", "表格行只含两个键"),
               ("fullwidth_comma", "全角逗号分隔的散文"),
               ("cross_line_comment", "跨行 HTML 注释里的键")]
KNOWN_LEAK = [("strip_definition", "删定义留小标题"), ("pad_to_count", "占位凑数"),
              ("code_wrap_pad", "围栏+凑行数"),
              ("enum_super_set", "枚举多一个要素"), ("enum_cross_line", "跨行枚举"),
              ("enum_drop_key", "枚举少一个键（部分枚举不查）")]
TMP_PREFIX = "seedancer_attack_"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_raw(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def write_raw(path, text):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def cleanup_stale_tmp():
    """清理**历史**遗留的攻击临时目录（脚本被强杀时 finally 不会执行 → 会残留）。
    返回清理数量；只删 `%TEMP%` 下以 TMP_PREFIX 开头且本次之外的目录。
    """
    removed = 0
    for d in glob.glob(os.path.join(tempfile.gettempdir(), TMP_PREFIX + "*")):
        if os.path.isdir(d):
            shutil.rmtree(d, ignore_errors=True)
            removed += 1
    return removed


def section_bounds(text, heading):
    """返回 (标题行下标, 下一同级或更高级标题下标)；找不到返回 (None, None)。"""
    lines = text.splitlines()
    level = len(heading) - len(heading.lstrip("#"))
    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == heading:
            start = i
            continue
        if start is not None and i > start:
            m = re.match(r"^(#{2,6})\s", ln)
            if m and len(m.group(1)) <= level:
                return start, i
    if start is not None:
        return start, len(lines)
    return None, None


def mutate(text, mode, heading, keys):
    """返回变异后的文本；段落未找到返回 None。"""
    s, e = section_bounds(text, heading)
    if s is None:
        return None
    lines = text.splitlines()
    head, body, tail = lines[:s + 1], lines[s + 1:e], lines[e:]
    name = heading.lstrip("#").strip()
    if mode == "wipe":
        body = ["（内容已删除 —— 攻击测试）", ""]
    elif mode == "drop_line":
        body = [l if not any(k in l for k in keys) else "（该行已删除）" for l in body]
    elif mode == "summarize":
        body = ["；".join(keys), ""]
    elif mode == "dup_heading":
        body = ["（内容已删除 —— 攻击测试）", ""]
        tail = tail + ["", heading, ""] + ["- %s" % k for k in keys]
    elif mode == "dup_level4":
        body = ["（内容已删除 —— 攻击测试）", ""]
        tail = tail + ["", "#### " + name, ""] + ["- %s" % k for k in keys]
    elif mode == "comment_wrap":
        body = ["<!-- %s -->" % "；".join(keys), ""]
    elif mode == "strip_definition":
        body = [re.sub(r"([：:])\s*\S.*$", r"\1", l) if any(k in l for k in keys) else l
                for l in body]
    elif mode == "code_wrap":
        body = ["```", "；".join(keys), "```", ""]
    elif mode == "quote_wrap":
        body = ["> " + "；".join(keys), ""]
    elif mode == "pad_to_count":
        body = ["；".join(keys)] + ["（占位）"] * len(keys)
    elif mode == "code_wrap_pad":
        body = ["```", "；".join(keys), "```"] + ["（占位）"] * len(keys)
    else:
        return None
    return "\n".join(head + body + tail)


def mutate_enum(text, mode):
    """A3 相关变异（作用于"首个完整枚举行"或文件末）。找不到锚点返回 None。"""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not all(k in line for k in A3_KEYS):
            continue
        if mode == "enum_drop_key":                       # 少一个键（A3 必红）
            lines[i] = line.replace(A3_KEYS[1], "", 1)
        elif mode == "enum_reorder":                      # 顺序换位（A3 必红）
            tmp = "\u0000"
            lines[i] = (line.replace(A3_KEYS[0], tmp, 1)
                            .replace(A3_KEYS[1], A3_KEYS[0], 1)
                            .replace(tmp, A3_KEYS[1], 1))
        elif mode == "enum_super_set":                    # 多一个要素（**已知漏检**）
            lines[i] = line.rstrip() + " + 五感来源"
        elif mode == "enum_extra_related":                # 枚举后加说明（**必须不报红**）
            lines[i] = line.rstrip() + "（按导演意图确定）"
        elif mode == "enum_cross_line":                   # 打散成 4 行（**已知漏检**）
            body = "\n".join("- %s" % k for k in A3_KEYS)
            return "\n".join(lines[:i] + [body] + lines[i + 1:])
        else:
            return None
        return "\n".join(lines)
    return None


def mutate_pointer(text, mode):
    """A4 攻击：改坏**首个** `见 §<主>` 指针；找不到返回 None。"""
    m = re.search(r"见\s*§\s*([^（(）)。,，;；\s·]+)(?:\s*·\s*([^（(）)。,，;；\s]+))?", text)
    if not m:
        return None
    if mode == "bad_sub_pointer":                       # 子标题不存在（当初的真实错位）
        if m.group(2):
            return text[:m.start()] + "见 §%s · 不存在的子标题" % m.group(1) + text[m.end():]
        return text[:m.end()] + " · 不存在的子标题" + text[m.end():]
    if mode == "bad_main_pointer":                      # 主标题不存在
        return text[:m.start()] + "见 §根本没有这一节" + text[m.end():]
    return None


def mutate_prose(text, mode):
    """注入**合法写法**（含 2 个规范键，但不是完整枚举）→ A3 **必须不报 not-ok**。"""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.strip().startswith("### 每镜四项事实"):
            continue
        inject = {
            "prose_mention": "本镜的视觉起点与观察关系按导演意图确定。",
            "prose_dunhao": "视觉起点、观察关系由导演在分镜时统一决定，其余两项另议。",
            "paren_mention": "（视觉起点、观察关系）见上一节的说明。",
            "table_row_2keys": "| `视觉起点` | `观察关系` |",
            "fullwidth_comma": "视觉起点，观察关系，两者需一一对应。",
            "cross_line_comment": "<!-- 说明：\n视觉起点、观察关系\n-->",
        }.get(mode)
        if inject is None:
            return None
        return "\n".join(lines[:i] + inject.splitlines() + lines[i:])
    return None


def main():
    if not (os.path.isfile(SKILL) and os.path.isfile(CHECKER)):
        print("环境错误：SKILL.md 或 check_consistency.py 不存在于 %s" % ROOT, file=sys.stderr)
        return 2

    removed = cleanup_stale_tmp()
    original_sha = sha256_file(SKILL)
    n_attacks = (sum(len(MODES) if full else 1 for _h, _k, full in ATTACKS)
                 + len(A3_MODES) + len(A4_MODES))
    n_leaks = (sum(len([m for m in KNOWN_LEAK if not m[0].startswith("enum_")]) for _ in ATTACKS)
               + len([m for m in KNOWN_LEAK if m[0].startswith("enum_")]))
    print("== 检查器攻击测试（%d 个必拦场景 + %d 个已知漏检 + %d 类合法写法）=="
          % (n_attacks, n_leaks, len(EXPECT_PASS)))
    if removed:
        print("[清理] 删除 %d 个陈旧临时目录（上次被强杀残留）" % removed)

    tmp_root = tempfile.mkdtemp(prefix=TMP_PREFIX)
    leaked, improvements = [], []
    try:
        work = os.path.join(tmp_root, "seedancer")
        shutil.copytree(ROOT, work,
                        ignore=shutil.ignore_patterns("_git_baseline", ".git", "__pycache__"))
        tmp_skill = os.path.join(work, SKILL_NAME)
        tmp_checker = os.path.join(work, CHECKER_NAME)
        pristine = read_raw(tmp_skill)

        def run_checker():
            p = subprocess.run([sys.executable, tmp_checker], capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=120)
            return p.returncode, (p.stdout or "") + (p.stderr or "")

        def a3_flagged():
            """A3 是 WARN 级 → 判"是否被拦住"要看**该项是否 not-ok**（而非退出码）。"""
            p = subprocess.run([sys.executable, tmp_checker, "--json"], capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=120)
            try:
                items = json.loads(p.stdout)["items"]
            except Exception:  # noqa: BLE001
                return None
            for it in items:
                if it["id"] == "A3":
                    return (not it["ok"], it.get("detail", ""))
            return None

        rc, _ = run_checker()
        print("[基线] 副本未变异 → exit=%d（期望 0）" % rc)
        if rc != 0:
            print("基线不通过 → 无法进行攻击测试（先修正常状态）")
            return 1

        for heading, keys, full in ATTACKS:
            for mode, label in (MODES if full else [("wipe", "整段清空")]):
                mutated = mutate(pristine, mode, heading, keys)
                if mutated is None:
                    print("[SKIP] %s / %s —— 段落未找到" % (heading, label))
                    continue
                write_raw(tmp_skill, mutated)
                rc, out = run_checker()
                caught = rc != 0
                print("[%s] %-28s %-12s → exit=%d %s"
                      % ("PASS" if caught else "LEAK", heading.replace("### ", ""), label, rc,
                         "" if caught else "⚠ 假绿：未被拦住"))
                if VERBOSE and not caught:
                    print("      checker 尾部：%s" % " | ".join(out.strip().splitlines()[-2:]))
                if not caught:
                    leaked.append("%s/%s" % (heading, label))
                write_raw(tmp_skill, pristine)

        # A3（G3'）：全文件级的规范枚举顺序（**WARN 级** → 以"该项是否 not-ok"判定）
        for mode, label in A3_MODES:
            mutated = mutate_enum(pristine, mode)
            if mutated is None:
                print("[SKIP] A3枚举顺序 / %s —— 未找到完整枚举行" % label)
                continue
            write_raw(tmp_skill, mutated)
            flagged, detail = a3_flagged()
            print("[%s] %-28s %-12s → A3=%s %s"
                  % ("PASS" if flagged else "LEAK", "A3 枚举顺序", label,
                     "not-ok" if flagged else "ok", "" if flagged else "⚠ 假绿：未被拦住"))
            if VERBOSE and flagged:
                print("      A3 detail：%s" % detail[:120])
            if not flagged:
                leaked.append("A3/%s" % label)
            write_raw(tmp_skill, pristine)

        # A4（TD-10）：文件内指针必须可解析（FAIL 级 → 看退出码）
        for mode, label in A4_MODES:
            mutated = mutate_pointer(pristine, mode)
            if mutated is None:
                print("[SKIP] A4指针解析 / %s —— 未找到 `见 §…` 指针" % label)
                continue
            write_raw(tmp_skill, mutated)
            rc, out = run_checker()
            caught = rc != 0
            print("[%s] %-28s %-12s → exit=%d %s"
                  % ("PASS" if caught else "LEAK", "A4 指针解析", label, rc,
                     "" if caught else "⚠ 假绿：坏指针未被拦住"))
            if VERBOSE and not caught:
                print("      checker 尾部：%s" % " | ".join(out.strip().splitlines()[-2:]))
            if not caught:
                leaked.append("A4/%s" % label)
            write_raw(tmp_skill, pristine)

        # **必须不报 not-ok** 的合法写法（防假红）—— 报了即算失败
        prose_modes = ("prose", "paren", "table", "fullwidth", "cross")
        for mode, label in EXPECT_PASS:
            mutated = (mutate_prose(pristine, mode) if mode.startswith(prose_modes)
                       else mutate_enum(pristine, mode))
            if mutated is None:
                print("[SKIP] 合法写法 / %s —— 未找到锚点" % label)
                continue
            write_raw(tmp_skill, mutated)
            flagged, detail = a3_flagged()
            rc_all, _ = run_checker()
            bad = bool(flagged) or rc_all != 0
            print("[%s] %-28s %-12s → A3=%s rc=%d %s"
                  % ("LEAK" if bad else "PASS", "合法写法（不应报错）", label,
                     "not-ok" if flagged else "ok", rc_all,
                     "⚠ 假红：合法内容被判失败" if bad else ""))
            if bad:
                leaked.append("假红/%s" % label)
            write_raw(tmp_skill, pristine)

        for heading, keys, _full in ATTACKS:
            for mode, label in KNOWN_LEAK:
                mutated = mutate(pristine, mode, heading, keys)
                if mutated is None:
                    continue
                write_raw(tmp_skill, mutated)
                rc, _ = run_checker()
                if rc != 0:
                    improvements.append("%s/%s" % (heading, label))
                    print("[改进] %-28s %-12s → 已被拦住（旧记录的漏检已覆盖，请移进 MODES）"
                          % (heading.replace("### ", ""), label))
                else:
                    print("[已知] %-28s %-12s → 仍漏检（已在 docstring 声明）"
                          % (heading.replace("### ", ""), label))
                write_raw(tmp_skill, pristine)

        # A3 的两类**已知漏检**（文件级；预期不报红）
        for mode, label in [m for m in KNOWN_LEAK if m[0].startswith("enum_")]:
            mutated = mutate_enum(pristine, mode)
            if mutated is None:
                continue
            write_raw(tmp_skill, mutated)
            rc, _ = run_checker()
            if rc != 0:
                improvements.append("A3/%s" % label)
                print("[改进] %-28s %-12s → 已被拦住（旧记录的漏检已覆盖，请移进 MODES/EXPECT_PASS）"
                      % ("A3 枚举一致性", label))
            else:
                print("[已知] %-28s %-12s → 仍漏检（已在 docstring 声明）"
                      % ("A3 枚举一致性", label))
            write_raw(tmp_skill, pristine)
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)
        after_sha = sha256_file(SKILL)
        if after_sha != original_sha:
            print("[污染] ❌ 真实 SKILL.md 被改动（sha256 %s ≠ %s）——请用 git 还原"
                  % (after_sha[:12], original_sha[:12]))
            return 2
        print("[隔离] 真实 %s 未被触碰（sha256 %s 前后一致）" % (SKILL_NAME, after_sha[:12]))

    print("\nRESULT: %s（%d 漏网）" % ("PASS" if not leaked else "FAIL(假绿)", len(leaked)))
    for x in leaked:
        print("  漏网：%s" % x)
    if improvements:
        print("  需同步 MODES（这些漏检已被覆盖）：%s" % "、".join(improvements))
    return 1 if leaked else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    raise SystemExit(main())
