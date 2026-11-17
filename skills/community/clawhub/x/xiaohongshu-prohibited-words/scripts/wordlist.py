#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
违禁词库的解析与匹配 —— **单一实现，两个消费方共用**。

词库（`references/prohibited-words.md`）是本 skill 的资产；
「怎么把它解析成可执行规则」也归本 skill，**不复制到使用方去**。

消费方：
  · `scripts/check_prohibited.py`                        —— 同目录，直接 import
  · `xiaohongshu-preflight-check/scripts/preflight.py`   —— 按同级 skill 目录 import

为什么要有这个文件：
  原先 check_prohibited.py 里内嵌了一份「精简词库」，靠人工与 md 保持同步。
  实测两边已经漂移 —— 文档里写着 P0 的「免费（全文≥2次）」与
  「答案+PDF+主页群」，脚本一个都没拦住。内嵌副本就是漂移的来源。

段落配置（哪一段归哪一组、默认什么级别）在 `references/sections.json`，
和词库同在 references/ 下，改级别只改那一个文件。

对外 API：
  find_wordlist()                 → 词库 md 路径（找不到返回 None）
  load_section_config()           → sections.json 内容
  load()                          → (rules, notices, stats, errors)
  match_rule(rule, text)          → [(命中文本, start, end)]
  collect(rules, text)            → 按 (级别, 命中词, 依据) 聚合后的清单
"""
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
DEFAULT_WORDLIST = SKILL_ROOT / "references" / "prohibited-words.md"
SECTIONS_JSON = SKILL_ROOT / "references" / "sections.json"

LEVEL_RANK = {"P0": 0, "P1": 1, "P2": 2, "hint": 3, "info": 4}

SECTION_RE = re.compile(r"^##\s*([一二三四五六七八九十]+)、")
PAREN_RE = re.compile(r"（([^）]*)）")
COUNT_RE = re.compile(r"[≥>=]+\s*(\d+)")

# 极限词清单里裸的「最」是词干不是词 —— 不展开会把每一处「最」都误杀
STEM_EXPAND = {
    "最": r"最(好|佳|优|大|小|便宜|火|安全|强|快|全|低|高|多|少|新|潮|划算|值|省时|实用|值得)",
}

TABLE_HEADERS = ("违禁词/组合", "违禁词", "词")


# ─────────────────────────── 定位与配置 ───────────────────────────

def find_wordlist(explicit=None):
    """词库是单一真相源 —— 本模块只负责找到它。

    优先级：显式参数 > 环境变量 `XHS_WORDLIST` > 本 skill 自带路径。
    **指定了却找不到 → 返回 None**，由消费方 fail-closed（退出码 3）；
    绝不静默回落到默认词库 —— 那会让「我换了词库」变成一句谎话。
    """
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.is_file() else None
    env = os.environ.get("XHS_WORDLIST")
    if env:
        p = Path(env).expanduser()
        return p if p.is_file() else None
    return DEFAULT_WORDLIST if DEFAULT_WORDLIST.is_file() else None


def load_section_config(path=None):
    p = Path(path) if path else SECTIONS_JSON
    if not p.is_file():
        raise RuntimeError(f"段落配置缺失：{p}（没有它就无法判定级别，拒绝继续）")
    return json.loads(p.read_text(encoding="utf-8"))


# ─────────────────────────── 词库解析 ───────────────────────────

def read_sections(path):
    """按 `## 一、` `## 二、` … 切段。其它任何 `## ` 都会清空当前段，避免串段。"""
    sections, cur = {}, None
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            m = SECTION_RE.match(ln)
            cur = m.group(1) if m else None
            if cur:
                sections[cur] = []
            continue
        if ln.startswith("# "):
            cur = None
            continue
        if cur is not None:
            sections[cur].append(ln)
    return sections


def clean_note(note):
    """把括号里的备注洗成人话（去掉「慎用，」这类引导词）。"""
    n = (note or "").strip()
    n = re.sub(r"^(慎用|建议)[，,、]?\s*", "", n)
    if len(n) > 1 and n[0] in "\"'" and n[-1] in "\"'":
        n = n[1:-1]
    return n.strip() or (note or "").strip()


def parse_cell(cell):
    """把一个「词」单元格解析成 (kind, payload)。

    覆盖词库里实际出现的四种写法：
      白嫖                        → literal
      0元 / ¥0                    → alternatives
      免费（全文≥2次）             → count(免费, 2)
      官方+免费+拿证（三词连用）     → cooccur([[官方], [免费], [拿证,证书,徽章]])
      答案/答案合集 + PDF + 主页群   → cooccur([[答案,答案合集], [PDF], [主页群]])
    """
    note = " ".join(PAREN_RE.findall(cell))
    core = PAREN_RE.sub("", cell).strip()

    mc = COUNT_RE.search(note)
    if mc and "次" in note:
        return "count", {"pattern": core, "threshold": int(mc.group(1)), "raw": cell}

    if "+" in core:
        groups = []
        for grp in core.split("+"):
            alts = [a.strip() for a in grp.split("/") if a.strip()]
            if alts == ["拿证"]:                 # 正文里常写「证书 / 徽章」
                alts = ["拿证", "证书", "徽章"]
            if alts:
                groups.append(alts)
        if len(groups) > 1:
            return "cooccur", {"groups": groups, "raw": cell}

    alts = [a.strip() for a in core.split("/") if a.strip()]
    if len(alts) > 1:
        return "alternatives", {"alts": alts, "raw": cell}
    return "literal", {"alts": alts or [core], "raw": cell}


def parse_prose_items(text):
    """解析「全禁：最、最佳、……」这类散文清单 → [(词, 备注), ...]"""
    items = []
    for raw in re.split(r"[、；]", text or ""):
        s = raw.strip().strip("。").strip()
        if not s:
            continue
        note = " ".join(PAREN_RE.findall(s))
        core = PAREN_RE.sub("", s).strip().strip("。").strip()
        if not core:
            continue
        if core.endswith("句式"):                 # 「我学了X」句式 → 我学了
            inner = re.search(r"[「“](.+?)[」”]", core)
            if inner:
                core = inner.group(1)
            core = re.sub(r"\s*[Xx]$", "", core).strip()
        if core:
            items.append((core, clean_note(note) if note else ""))
    return items


def build_rule(section, word, level, why, suggest, group, overrides):
    lvl = overrides.get(word, level)
    if lvl not in LEVEL_RANK:
        lvl = "P1"
    rule = {
        "id": "wl-{0}-{1}".format(section, word),
        "section": section, "group": group, "level": lvl,
        "why": why or "", "suggest": suggest or "", "src": "词库 {0}".format(section),
        "raw": word,
    }
    if word in STEM_EXPAND:
        rule.update(kind="regex", pattern=STEM_EXPAND[word])
        return rule
    kind, payload = parse_cell(word)
    rule.update(kind=kind)
    rule.update(payload)
    # 「微信 / 微信号 / vx / 卫星」这类一格多词，允许逐词定级
    if kind == "alternatives":
        rule["altLevels"] = {a: overrides.get(a, lvl) for a in rule["alts"]}
    return rule


def load(wordlist_path=None, sections_path=None):
    """→ (rules, notices, stats, errors)。notices 是不参与匹配的强制标注提醒。"""
    path = find_wordlist(wordlist_path)
    if path is None:
        return [], [], {}, ["词库未找到：{0}".format(wordlist_path or DEFAULT_WORDLIST)]

    cfg = load_section_config(sections_path)
    maps = cfg.get("sections", {})
    overrides = {k: v for k, v in (cfg.get("levelOverrides") or {}).items()
                 if not k.startswith("_")}

    sections = read_sections(path)
    rules, notices, stats, errors = [], [], {}, []

    for sec, sc in maps.items():
        lines = sections.get(sec)
        if lines is None:
            errors.append("词库缺少「{0}、」段（格式可能已变）".format(sec))
            continue
        group = sc.get("group", "words")
        count = 0
        for ln in lines:
            s = ln.strip()
            if not s:
                continue
            entries = []            # [(word, level, why, suggest)]
            if s.startswith("|"):
                cells = [c.strip() for c in s.strip().strip("|").split("|")]
                cells = [c for c in cells if c]
                if not cells or cells[0] in TABLE_HEADERS:
                    continue
                if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    continue
                if len(cells) >= 4:                       # 词|级别|场景|替代|日期
                    entries.append((cells[0], cells[1], cells[2], cells[3]))
                elif len(cells) == 2:                     # 词|替代
                    entries.append((cells[0], sc.get("level", "P1"), sc.get("why", ""), cells[1]))
                else:
                    entries.append((cells[0], sc.get("level", "P1"), sc.get("why", ""), ""))
            elif s.startswith("全禁：") or "、" in s or "；" in s:
                body = re.sub(r"^全禁：", "", s)
                for w, note in parse_prose_items(body):
                    entries.append((w, sc.get("level", "P1"), sc.get("why", ""),
                                    note or sc.get("suggestDefault", "")))
            elif s.startswith("- "):
                # 强制标注类：不参与文本匹配，只作为「请逐条核对」提醒
                notices.append({"group": group, "section": sec, "text": s[2:].strip()})
                count += 1
                continue

            for word, level, why, suggest in entries:
                rules.append(build_rule(
                    sec, word,
                    level or sc.get("level", "P1"),
                    why or sc.get("why", ""),
                    suggest or sc.get("suggestDefault", ""),
                    group, overrides))
                count += 1
        stats[sec] = count

    # 词库没写、但同属一个判定面的补充规则（手机号 / 邮箱）
    for name, ep in (cfg.get("extraPatterns") or {}).items():
        if name.startswith("_") or not ep.get("pattern"):
            continue
        rules.append({
            "id": "extra-{0}".format(name), "section": "extra",
            "group": ep.get("group", "diversion"), "level": ep.get("level", "P1"),
            "kind": "regex", "pattern": ep["pattern"],
            "why": ep.get("why", ""), "suggest": ep.get("suggest", ""),
            "src": "补充规则",
        })

    return rules, notices, stats, errors


# ─────────────────────────── 匹配 ───────────────────────────

def dedupe_span(items):
    """同一规则内做包含去重：命中「微信号」时不再单独报「微信」。"""
    items = sorted(items, key=lambda x: (x[1], -(x[2] - x[1])))
    kept = []
    for it in items:
        if any(it[1] >= k[1] and it[2] <= k[2] for k in kept):
            continue
        kept.append(it)
    return kept


def match_rule(rule, text):
    kind = rule.get("kind")
    if kind in ("literal", "alternatives"):
        out = []
        for a in rule.get("alts", []):
            for m in re.finditer(re.escape(a), text):
                out.append((a, m.start(), m.end()))
        return dedupe_span(out)
    if kind == "regex":
        return [(m.group(0), m.start(), m.end()) for m in re.finditer(rule["pattern"], text)]
    if kind == "count":
        ms = list(re.finditer(re.escape(rule["pattern"]), text))
        if len(ms) >= rule["threshold"]:
            # 只锚在第一次出现的位置，避免宽 span 吞掉其它命中
            return [("{0} × {1} 次".format(rule["pattern"], len(ms)), ms[0].start(), ms[0].end())]
        return []
    if kind == "cooccur":
        found = []
        for alts in rule["groups"]:
            hit = None
            for a in alts:
                m = re.search(re.escape(a), text)
                if m:
                    hit = (a, m.start(), m.end())
                    break
            if not hit:
                return []
            found.append(hit)
        return [(" + ".join(f[0] for f in found),
                 min(f[1] for f in found), max(f[2] for f in found))]
    return []


def collect(rules, text):
    """跑全部规则并收敛成可读清单。

    词库里同一个词可能被多条规则覆盖（如「最」展开的 regex 与清单里的「最好」
    命中同一位置），所以先按 span 去重（同级取先到的），再按
    (级别, 命中词, 依据) 聚合，把重复出现折叠成 ×N —— 自检结果要能一眼看完。
    """
    raw = []
    for r in rules:
        for matched, s, e in match_rule(r, text):
            lvl = r.get("altLevels", {}).get(matched, r["level"])
            raw.append((s, e, lvl, matched, r))

    seen, deduped = set(), []
    for s, e, lvl, matched, r in sorted(raw, key=lambda x: (x[0], x[1], LEVEL_RANK.get(x[2], 9))):
        if (s, e) in seen:
            continue
        seen.add((s, e))
        deduped.append((s, e, lvl, matched, r))

    agg = {}
    for s, e, lvl, matched, r in deduped:
        key = (lvl, matched, r["why"])
        if key not in agg:
            agg[key] = {"group": r["group"], "level": lvl, "matched": matched,
                        "why": r["why"], "suggest": r["suggest"], "src": r["src"],
                        "count": 0}
        agg[key]["count"] += 1
    return sorted(agg.values(), key=lambda h: (LEVEL_RANK.get(h["level"], 9), -h["count"]))
