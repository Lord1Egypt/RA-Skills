#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""动效静态检查：找出会掉帧、不可访问、不一致的写法。

用法：
    python3 lint_motion.py src/components/Card.tsx
    python3 lint_motion.py src/styles/ --format json
    python3 lint_motion.py . --quiet          # 只看 error

规则：
    layout-prop       error  动画了会触发重排的属性（width/height/top/left/margin…）
    transition-all    error  transition: all
    will-change-all   error  will-change: all
    long-duration     warn   单次过渡 > 800ms 且非无限循环
    no-reduced-motion warn   文件里有动画但没有 prefers-reduced-motion 降级
    hover-ungated     warn   :hover 未包在 @media (hover: hover) 里
    shadow-transition info   过渡 box-shadow（重绘成本高）
    infinite-loop     info   无限循环动画，确认可暂停/可降级

退出码：有 error 返回 1，否则 0。
"""
import argparse
import bisect
import json
import os
import re
import sys

EXTS = {".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx",
        ".vue", ".svelte", ".html", ".htm", ".astro"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", "coverage", "vendor", ".cache"}

LAYOUT_PROPS = {
    "width", "height", "min-width", "min-height", "max-width", "max-height",
    "top", "right", "bottom", "left", "inset", "inset-block", "inset-inline",
    "margin", "margin-top", "margin-right", "margin-bottom", "margin-left",
    "margin-block", "margin-inline",
    "padding", "padding-top", "padding-right", "padding-bottom", "padding-left",
    "padding-block", "padding-inline",
    "border-width", "font-size", "line-height", "flex-basis",
}

RULE_DESC = {
    "layout-prop": "动画了布局属性，每帧触发重排；改用 transform / opacity，或用 grid-template-rows、clip-path 表达展开",
    "transition-all": "transition: all 会把不相干属性一起过渡，包括布局属性；显式列出要过渡的属性",
    "will-change-all": "will-change: all 会让浏览器提升大量图层；只给即将动画的元素加，结束后移除",
    "long-duration": "单次过渡超过 800ms，交互反馈会显得拖沓；超过 1s 需有明确叙事理由",
    "no-reduced-motion": "文件含动画但没有 prefers-reduced-motion 降级，前庭敏感用户无法关闭",
    "hover-ungated": ":hover 未包在 @media (hover: hover) and (pointer: fine) 里，触屏点按后样式会粘住",
    "shadow-transition": "过渡 box-shadow 会逐帧重绘；改为预置伪元素只改透明度",
    "infinite-loop": "无限循环动画，确认提供暂停方式或在 reduced-motion 下关闭",
}

SEVERITY_ORDER = {"info": 0, "warn": 1, "error": 2}


def strip_comments(text):
    """把注释替换成等长空白，保持偏移不变。"""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"/\*.*?\*/", blank, text, flags=re.S)
    text = re.sub(r"(?m)(^|[^:])//[^\n]*", lambda m: m.group(1) + " " * (len(m.group(0)) - len(m.group(1))), text)
    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    return text


def collect(paths):
    files = []
    for p in paths:
        if os.path.isfile(p):
            if os.path.splitext(p)[1].lower() in EXTS:
                files.append(p)
            continue
        for root, dirs, names in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for n in names:
                if os.path.splitext(n)[1].lower() in EXTS:
                    files.append(os.path.join(root, n))
    return sorted(files)


def iter_keyframe_bodies(text):
    """产出 (@keyframes 名称, body 起始位置, body 文本) 供逐条检查声明。"""
    for m in re.finditer(r"@(?:-webkit-)?keyframes\s+([\w-]+)\s*\{", text):
        start = m.end() - 1
        depth = 0
        for i in range(start, len(text)):
            ch = text[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    yield m.group(1), start + 1, text[start + 1:i]
                    break


def parse_props(value):
    props = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        token = re.split(r"[\s(]", part, maxsplit=1)[0].strip().lower()
        if token:
            props.append(token)
    return props


def durations_ms(value):
    out = []
    for num, unit in re.findall(r"(\d*\.?\d+)\s*(ms|s)\b", value):
        try:
            v = float(num)
        except ValueError:
            continue
        out.append(v if unit == "ms" else v * 1000)
    return out


def lint_file(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    text = strip_comments(raw)
    starts = [0] + [m.end() for m in re.finditer(r"\n", text)]

    def line_of(pos):
        return bisect.bisect_right(starts, pos)

    issues = []

    def add(rule, pos, snippet, severity=None):
        issues.append({
            "rule": rule,
            "severity": severity or ("error" if rule in
                                     ("layout-prop", "transition-all", "will-change-all") else
                                     "warn" if rule in ("long-duration", "no-reduced-motion", "hover-ungated") else
                                     "info"),
            "line": line_of(pos),
            "message": RULE_DESC[rule],
            "snippet": snippet.strip()[:120],
        })

    has_anim = bool(re.search(r"\b(animation|transition)\s*:", text))
    has_reduced = "prefers-reduced-motion" in text

    # 1) transition / transition-property 声明
    for m in re.finditer(r"(?<![\w-])(transition|transition-property)\s*:\s*([^;}{\n]+)", text):
        value = m.group(2)
        props = parse_props(value)
        if "all" in props:
            add("transition-all", m.start(), m.group(0))
        layout_hit = [p for p in props if p in LAYOUT_PROPS]
        if layout_hit:
            add("layout-prop", m.start(), f"{m.group(0)}  ← {','.join(layout_hit)}")
        if "box-shadow" in props:
            add("shadow-transition", m.start(), m.group(0))
        if "infinite" not in value:
            worst = max(durations_ms(value), default=0)
            if worst > 800:
                add("long-duration", m.start(), f"{m.group(0)}  ← {worst:.0f}ms")

    # 2) @keyframes 里的声明
    for name, bstart, body in iter_keyframe_bodies(text):
        for m in re.finditer(r"([\w-]+)\s*:\s*([^;}{\n]+)", body):
            prop = m.group(1).lower()
            if prop in LAYOUT_PROPS:
                add("layout-prop", bstart + m.start(), f"@keyframes {name} ← {prop}: {m.group(2).strip()}")

    # 3) animation 简写里的超长时长
    for m in re.finditer(r"(?<![\w-])animation\s*:\s*([^;}{\n]+)", text):
        value = m.group(1)
        if "infinite" in value:
            add("infinite-loop", m.start(), m.group(0))
            continue
        worst = max(durations_ms(value), default=0)
        if worst > 800:
            add("long-duration", m.start(), f"{m.group(0)}  ← {worst:.0f}ms")

    # 4) JS 内联样式对象（transition: 'width .3s' / animate={{ width: 0 }}）
    for m in re.finditer(r"transition\s*:\s*['\"`]([^'\"`]+)['\"`]", text):
        value = m.group(1)
        if re.search(r"\ball\b", value):
            add("transition-all", m.start(), m.group(0))
        hit = [p for p in re.findall(r"[a-zA-Z-]+", value) if p in LAYOUT_PROPS]
        if hit:
            add("layout-prop", m.start(), f"{m.group(0)}  ← {','.join(set(hit))}")

    for m in re.finditer(r"(?:animate|variants|from|to)\s*[=:]\s*\{([^{}]{0,400})\}", text):
        body = m.group(1)
        hit = [p for p in re.findall(r"(?:^|[,{\s])([a-zA-Z-]+)\s*:", body)
               if p.lower() in LAYOUT_PROPS]
        if hit:
            add("layout-prop", m.start(), f"{m.group(0)[:80]}  ← {','.join(set(hit))}")

    # 5) 全局可访问性
    if has_anim and not has_reduced:
        add("no-reduced-motion", 0, "缺 @media (prefers-reduced-motion: reduce)")

    gated = re.search(r"@media[^{]*(hover\s*:\s*hover|hover\s*:\s*none)", text)
    if ":hover" in text and not gated:
        pos = text.find(":hover")
        add("hover-ungated", pos, text[pos:pos + 60].split("\n")[0])

    # 6) will-change
    if re.search(r"will-change\s*:\s*all", text):
        pos = re.search(r"will-change\s*:\s*all", text).start()
        add("will-change-all", pos, "will-change: all")
    wc = len(re.findall(r"will-change\s*:", text))
    if wc > 3:
        add("will-change-all", text.find("will-change"),
            f"文件中出现 {wc} 处 will-change，图层可能过多")

    # 去重（同规则同行）
    seen, uniq = set(), []
    for it in issues:
        k = (it["rule"], it["line"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(it)
    uniq.sort(key=lambda x: (-SEVERITY_ORDER[x["severity"]], x["line"]))
    return uniq


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--quiet", action="store_true", help="只显示 error")
    args = ap.parse_args()

    files = collect(args.paths)
    if not files:
        print("没有找到可检查的文件（支持 css/scss/less/js/jsx/ts/tsx/vue/svelte/html/astro）")
        sys.exit(2)

    report, counts = [], {"error": 0, "warn": 0, "info": 0}
    for f in files:
        issues = lint_file(f)
        for it in issues:
            counts[it["severity"]] += 1
        if issues:
            report.append({"file": f, "issues": issues})

    if args.format == "json":
        print(json.dumps({"files": report, "summary": counts, "scanned": len(files)},
                         ensure_ascii=False, indent=1))
    else:
        for item in report:
            print(item["file"])
            for it in item["issues"]:
                if args.quiet and it["severity"] != "error":
                    continue
                print(f"  {it['severity']:<5} L{it['line']:<5} {it['rule']:<17} {it['snippet']}")
                if it["severity"] == "error":
                    print(f"        → {it['message']}")
            print()
        print(f"扫描 {len(files)} 个文件：{counts['error']} error / {counts['warn']} warn / {counts['info']} info")
        if counts["error"]:
            print("有 error，改完再交付。")

    sys.exit(1 if counts["error"] else 0)


if __name__ == "__main__":
    main()
