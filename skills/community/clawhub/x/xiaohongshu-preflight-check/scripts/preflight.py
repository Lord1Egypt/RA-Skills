#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书发布前检测 —— 文本合规自查（4 组）

  组 1  违禁词·敏感词·限流词   ← 词库单一真相源：xiaohongshu-prohibited-words
  组 2  标题与篇幅规范
  组 3  AI 声明与强制标注
  组 4  导流风险

设计原则 —— fail-closed：
  依赖缺失 / 解析失败 / 载入 0 条规则，一律退出码 3，绝不等价于「通过」。
  对一条发布前的自检命令来说，「没查出来」和「查不了」必须是两件事。

词库与其解析逻辑都在 `xiaohongshu-prohibited-words`（`scripts/wordlist.py`），
本 skill **不复制**，运行时按同级 skill 目录载入。

用法：
  python3 preflight.py --file 笔记终稿.md
  python3 preflight.py --title "标题" --body "正文" --tags "#标签1 #标签2"
  python3 preflight.py "标题" "正文" "标签"
  python3 preflight.py --file note.md --json          # 机器可读
  python3 preflight.py --file note.md --wordlist PATH # 指定词库

退出码：
  0  通过（无 P0、无 P1）
  1  有 P0 必改项 —— 禁止发布
  2  只有 P1 建议项 —— 可发，建议改
  3  输入缺失 / 词库找不到 / 解析失败（fail-closed）
"""
import argparse
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
PLATFORM_DIR = SKILL_ROOT / "references" / "platforms"

EXIT_PASS, EXIT_P0, EXIT_P1, EXIT_ERROR = 0, 1, 2, 3
LEVEL_RANK = {"P0": 0, "P1": 1, "P2": 2, "hint": 3, "info": 4}
CN_WHERE = {"title": "标题", "body": "正文", "tags": "标签"}

# 共享模块里的组名 → 本 skill 的 4 组（notice = 平台强制标注 → 并入第 3 组）
GROUP_MAP = {"words": "words", "diversion": "diversion", "notice": "ai"}

WORDLIST_SKILL = "xiaohongshu-prohibited-words"


# ─────────────────────────── 共享词库模块 ───────────────────────────

def skill_roots():
    """词库 skill 的候选安装位置 —— 默认词库与共享解析器都从这里找。"""
    home = Path.home()
    return [
        SKILL_ROOT.parent / WORDLIST_SKILL,
        home / ".workbuddy" / "skills" / WORDLIST_SKILL,
        home / ".workbuddy" / "skills" / "@bonniegeng-max" / WORDLIST_SKILL,
        home / ".agents" / "skills" / WORDLIST_SKILL,
    ]


def find_wordlist(explicit=None):
    """词库是单一真相源，本 skill 不复制它 —— 只按候选路径去找。

    优先级：`--wordlist` > 环境变量 `XHS_WORDLIST` > 词库 skill 的安装位置。
    **指定了却找不到 → 返回 None**（调用方据此 fail-closed，退出码 3），
    不静默回落到候选路径 —— 否则「指定了一个不存在的词库」会变成一次假通过。
    """
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.is_file() else None
    env = os.environ.get("XHS_WORDLIST")
    if env:
        p = Path(env).expanduser()
        return p if p.is_file() else None
    for root in skill_roots():
        c = root / "references" / "prohibited-words.md"
        if c.is_file():
            return c
    return None


def load_shared_module(wl_path):
    """载入共享解析模块（词库的解析逻辑归词库 skill，不归这里）。

    解析器**按词库文件位置反推**是错的：那样 `--wordlist` / `XHS_WORDLIST`
    指向一个纯数据文件（比如家目录里的 `my-words.md`）就会报「解析模块缺失」。
    解析器是代码、词库是数据，两者不该绑死。所以：

      1. 先看词库旁边有没有 `scripts/wordlist.py`（fork 换了格式也能跟得上）
      2. 没有就回落到词库 skill 的安装位置

    两条都找不到才报错 —— 仍然是 fail-closed，不会变成假通过。
    """
    cands = [Path(wl_path).resolve().parent.parent / "scripts" / "wordlist.py"]
    cands += [r / "scripts" / "wordlist.py" for r in skill_roots()]
    mod_path = next((c for c in cands if c.is_file()), None)
    if mod_path is None:
        raise RuntimeError(
            "共享解析模块缺失：找不到 scripts/wordlist.py（应在 skill "
            f"`{WORDLIST_SKILL}` 下）—— 词库 skill 可能没装或版本过旧")
    spec = importlib.util.spec_from_file_location("xhs_wordlist", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ─────────────────────────── 输入 ───────────────────────────

def extract_section(content, name):
    out, inside = [], False
    for ln in content.split("\n"):
        st = ln.strip()
        if st.startswith("## "):
            inside = st[3:].strip().startswith(name)
            continue
        if st.startswith("# ") and inside:
            break
        if inside:
            out.append(ln)
    return "\n".join(out).strip()


def read_input(args):
    warn = []
    if args.file:
        try:
            content = Path(args.file).read_text(encoding="utf-8")
        except Exception as e:
            raise RuntimeError(f"读取失败 {args.file}：{e}")
        title = extract_section(content, "标题")
        body = extract_section(content, "正文")
        tags = extract_section(content, "标签")
        if not title and not body:
            body = content
            warn.append("未识别到「## 标题」段 —— 标题规范检查已跳过。若文件里有标题，加一段 `## 标题`")
        elif not title:
            warn.append("未识别到「## 标题」段 —— 标题规范检查已跳过")
    else:
        title = args.title or ""
        body = args.body or ""
        tags = args.tags or ""
        if not (title or body or tags) and args.positional:
            ps = args.positional
            title = ps[0] if len(ps) > 0 else ""
            body = ps[1] if len(ps) > 1 else ""
            tags = ps[2] if len(ps) > 2 else ""
    return title, body, tags, warn


def char_len(s):
    """平台按「1 个字符」计 Emoji / 数字 / 字母 / 汉字 —— 直接用 len()。"""
    return len(s or "")


def is_emoji(ch):
    o = ord(ch)
    return (0x1F300 <= o <= 0x1F5FF or 0x1F600 <= o <= 0x1F64F or
            0x1F680 <= o <= 0x1F6FF or 0x1F900 <= o <= 0x1F9FF or
            0x1FA70 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF or
            0x2B00 <= o <= 0x2BFF or 0x1F1E6 <= o <= 0x1F1FF)


# ─────────────────────────── 内置检查（组 2）───────────────────────────

def run_builtin(platform, title, body, tags):
    lim = platform.get("limits", {})
    hits = []

    def add(group, level, where, matched, why, suggest):
        hits.append({"group": group, "level": level, "where": where,
                     "matched": matched, "why": why, "suggest": suggest, "count": 1})

    for r in platform.get("rules", []):
        chk = r["check"]
        if chk == "titleMaxChars" and title:
            n, mx = char_len(title), lim.get("titleMaxChars", 20)
            if n > mx:
                add(r["group"], r["level"], "标题", f"{n} 字符（上限 {mx}）", r["why"], r["suggest"])
        elif chk == "titleMinChars" and title:
            n, mn = char_len(title), lim.get("titleMinChars", 6)
            if n < mn:
                add(r["group"], r["level"], "标题", f"{n} 字符（建议 ≥{mn}）", r["why"], r["suggest"])
        elif chk == "hook" and title:
            if not any(re.search(p, title) for p in r.get("patterns", [])):
                add(r["group"], r["level"], "标题", "未见结果感钩子", r["why"], r["suggest"])
        elif chk == "titleCount" and title:
            n = len(re.findall(r.get("pattern", ""), title))
            if n >= r.get("min", 2):
                add(r["group"], r["level"], "标题", f"「{r.get('pattern')}」× {n} 处", r["why"], r["suggest"])
        elif chk == "titleEmojiCount" and title:
            n = sum(1 for c in title if is_emoji(c))
            if n >= r.get("min", 4):
                add(r["group"], r["level"], "标题", f"emoji × {n} 个", r["why"], r["suggest"])
        elif chk == "bodyMaxChars" and body:
            n, mx = char_len(body), lim.get("bodyMaxChars", 1000)
            if n > mx:
                add(r["group"], r["level"], "正文", f"{n} 字符（上限 {mx}）", r["why"], r["suggest"])
        elif chk == "bodyMinChars" and body:
            n, mn = char_len(body), lim.get("bodyMinChars", 40)
            if n < mn:
                add(r["group"], r["level"], "正文", f"{n} 字符（建议 ≥{mn}）", r["why"], r["suggest"])
    return hits


def run_ai(platform, title, body, tags):
    cfg = platform.get("aiSignals", {})
    all_text = "\n".join([title or "", body or "", tags or ""])
    sigs = sorted({m.group(0) for p in cfg.get("patterns", []) for m in re.finditer(p, all_text)})
    if sigs:
        return [{"group": "ai", "level": cfg.get("level", "P1"), "where": "全文",
                 "matched": " / ".join(sigs), "count": 1,
                 "why": cfg.get("why", ""), "suggest": cfg.get("suggest", "")}]
    fb = cfg.get("fallbackHint", {})
    if not fb:
        return []
    return [{"group": "ai", "level": "hint", "where": "全文", "count": 1,
             "matched": "未发现 AI 生成 / 辅助信号",
             "why": fb.get("why", ""), "suggest": fb.get("suggest", "")}]


# ─────────────────────────── 输出 ───────────────────────────

BAR = "═" * 58
THIN = "─" * 58
ICON = {"P0": "✗", "P1": "!", "P2": "·", "hint": "·", "info": "·"}
LEVEL_LABEL = {"P0": "P0", "P1": "P1", "P2": "P2", "hint": "提示", "info": "提示"}


def print_report(platform, args, title, body, tags, wl_path, wl_stats,
                 notices, hits, warnings, errors, code):
    groups = platform.get("groups", [])
    by_group = {g[0]: [] for g in groups}
    for h in hits:
        by_group.setdefault(h["group"], []).append(h)

    print(BAR)
    print(f" {platform.get('displayName', platform['platform'])}发布前检测 · 合规自查")
    print(BAR)
    print(f"平台  {platform.get('displayName')}")
    print(f"输入  标题 {char_len(title)} 字 / 正文 {char_len(body)} 字 / 标签 {len((tags or '').split())} 个")
    if wl_path:
        stat = " / ".join(f"{k} {v}" for k, v in wl_stats.items())
        print(f"词库  {wl_path}")
        print(f"      载入 {sum(wl_stats.values())} 条（{stat}）")
    else:
        print("词库  ✗ 未找到 —— 第 1 组无法执行")
    print("")

    for gid, glabel in groups:
        print(f"【{glabel}】")
        rows = sorted(by_group.get(gid, []), key=lambda h: LEVEL_RANK.get(h["level"], 9))
        if not rows:
            print("  ✓ 无命中")
        for h in rows:
            n = h.get("count", 1)
            times = f"  ×{n}" if n > 1 else ""
            print(f"  {ICON.get(h['level'], '·')} {LEVEL_LABEL.get(h['level'], h['level'])}  "
                  f"[{h['where']}]「{h['matched']}」{times}")
            if h.get("why"):
                print(f"        依据：{h['why']}")
            if h.get("suggest"):
                print(f"        建议：{h['suggest']}")
        for nt in [x for x in notices if x["group"] == gid]:
            print(f"  · 请逐条核对：{nt['text']}")
        print("")

    p0 = [h for h in hits if h["level"] == "P0"]
    p1 = [h for h in hits if h["level"] == "P1"]
    n0 = sum(h.get("count", 1) for h in p0)
    n1 = sum(h.get("count", 1) for h in p1)
    print(THIN)
    if code == EXIT_ERROR:
        print("结论：⚠ 检测未完成 —— fail-closed，按「不允许发布」处理")
        for e in errors:
            print(f"  ✗ {e}")
    elif p0:
        print(f"结论：✗ 需改 —— P0 共 {n0} 处（{len(p0)} 项），P0 未清空 = 禁止发布")
    elif p1:
        print(f"结论：! 可发 —— P1 建议项 {n1} 处（{len(p1)} 项），不阻塞发布但建议改")
    else:
        print("结论：✓ 通过 —— 未发现 P0 / P1")

    if p0 or p1:
        print("\n最小补法")
        i = 1
        if p0:
            print(f"  {i}. 先清 P0（{n0} 处）—— 这一档清空之前不要发")
            i += 1
        if p1:
            print(f"  {i}. 再处理 P1（{n1} 处）—— 顺手改，不阻塞")
            i += 1
        rerun = f"--file {args.file}" if args.file else "--title ... --body ... --tags ..."
        print(f"  {i}. 重跑自检：python3 scripts/preflight.py {rerun}")

    if warnings:
        print("\n提示")
        for w in warnings:
            print(f"  · {w}")
    print("\n未覆盖：图片 / 封面 / 视频 —— v1 只查文本。封面配字与 OCR 请人工过一眼")
    print(f"退出码 {code}")
    print(BAR)


def to_json(platform, title, body, tags, wl_path, wl_stats, notices,
            hits, warnings, errors, code):
    p0 = [h for h in hits if h["level"] == "P0"]
    p1 = [h for h in hits if h["level"] == "P1"]
    verdict = {EXIT_PASS: "pass", EXIT_P0: "must_fix", EXIT_P1: "advisory", EXIT_ERROR: "error"}[code]
    return json.dumps({
        "platform": platform["platform"],
        "verdict": verdict,
        "exitCode": code,
        "input": {"titleChars": char_len(title), "bodyChars": char_len(body),
                  "tagCount": len((tags or "").split())},
        "wordlist": {"path": str(wl_path) if wl_path else None,
                     "loaded": sum(wl_stats.values()), "bySection": wl_stats},
        "counts": {"P0": sum(h.get("count", 1) for h in p0),
                   "P1": sum(h.get("count", 1) for h in p1)},
        "findings": hits,
        "mandatoryNotices": notices,
        "warnings": warnings,
        "errors": errors,
    }, ensure_ascii=False, indent=2)


# ─────────────────────────── main ───────────────────────────

def main():
    ap = argparse.ArgumentParser(description="小红书发布前检测（文本合规自查）")
    ap.add_argument("positional", nargs="*", help="标题 正文 标签")
    ap.add_argument("--file", help="笔记 md/txt（读「## 标题」「## 正文」「## 标签」段）")
    ap.add_argument("--title")
    ap.add_argument("--body")
    ap.add_argument("--tags")
    ap.add_argument("--platform", default="xiaohongshu")
    ap.add_argument("--wordlist", help="词库路径（默认自动查找 xiaohongshu-prohibited-words）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    args = ap.parse_args()

    errors, warnings = [], []

    pf = PLATFORM_DIR / f"{args.platform}.json"
    if not pf.is_file():
        print(f"✗ 平台规则文件缺失：{pf}（fail-closed，不判定通过）", file=sys.stderr)
        return EXIT_ERROR
    try:
        platform = json.loads(pf.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"✗ 平台规则解析失败：{e}（fail-closed）", file=sys.stderr)
        return EXIT_ERROR

    try:
        title, body, tags, w = read_input(args)
        warnings.extend(w)
    except RuntimeError as e:
        print(f"✗ {e}", file=sys.stderr)
        return EXIT_ERROR

    if not (title or body or tags):
        print("✗ 没有输入 —— 用 --file 或 --title/--body/--tags（fail-closed，不判定通过）",
              file=sys.stderr)
        return EXIT_ERROR

    wl_path = find_wordlist(args.wordlist)
    wl_hits, notices, wl_stats = [], [], {}
    if wl_path is None:
        errors.append("词库未找到 —— 第 1 组（违禁词/敏感词/限流词）无法执行。"
                      "请先装 xiaohongshu-prohibited-words，或用 --wordlist 指定路径")
    else:
        try:
            wl = load_shared_module(wl_path)
            rules, raw_notices, wl_stats, perr = wl.load(wordlist_path=str(wl_path))
            errors.extend(perr)
            if not rules:
                errors.append(f"词库解析出 0 条可匹配规则（{wl_path}）—— 格式可能已变，拒绝放行")
            else:
                all_text = "\n".join([title or "", body or "", tags or ""])
                for h in wl.collect(rules, all_text):
                    h = dict(h)
                    h["group"] = GROUP_MAP.get(h["group"], h["group"])
                    h["where"] = "全文"
                    wl_hits.append(h)
                notices = [{"group": GROUP_MAP.get(n["group"], n["group"]), "text": n["text"]}
                           for n in raw_notices]
        except Exception as e:
            errors.append(f"词库加载失败：{e}")

    hits = list(wl_hits)
    try:
        hits.extend(run_builtin(platform, title, body, tags))    # 组 2
        hits.extend(run_ai(platform, title, body, tags))         # 组 3
    except re.error as e:
        errors.append(f"规则执行失败：{e}")

    if errors:
        code = EXIT_ERROR
    elif any(h["level"] == "P0" for h in hits):
        code = EXIT_P0
    elif any(h["level"] == "P1" for h in hits):
        code = EXIT_P1
    else:
        code = EXIT_PASS

    if args.json:
        print(to_json(platform, title, body, tags, wl_path, wl_stats, notices,
                      hits, warnings, errors, code))
    else:
        print_report(platform, args, title, body, tags, wl_path, wl_stats,
                     notices, hits, warnings, errors, code)
    return code


if __name__ == "__main__":
    sys.exit(main())
