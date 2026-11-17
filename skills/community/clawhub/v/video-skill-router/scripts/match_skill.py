#!/usr/bin/env python3
"""match_skill.py - need-to-skill matcher for video-skill-router.

Usage:
    python match_skill.py --query "做数学公式讲解动画"
    python match_skill.py --query "..." --category education
    python match_skill.py --query "..." --local-only
    python match_skill.py --query "..." --candidates candidates.json

Pools merged for scoring:
  1. local installed skills (~/.workbuddy/skills/*/SKILL.md frontmatter)
  2. built-in curated catalog (../data/curated-catalog.json, verified skill packs)
  3. optional --candidates file from search_anim.py

Exit codes:
    0 = LOCAL HIT: an installed skill scores >= 25 (use it directly, no download)
    1 = EXTERNAL READY: catalog/candidate top hit >= 35, or weak match (search/install)
    2 = NO MATCH: nothing scored above 0
Standard library only.
"""

import argparse
import json
import os
import re
import sys

SKILLS_DIR = os.path.join(os.path.expanduser("~"), ".workbuddy", "skills")
CATALOG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "curated-catalog.json"
)
THRESHOLD = 35
LOCAL_THRESHOLD = 25
SELF_NAMES = {"video-skill-router", "anim-skill-router"}

CATEGORY_KEYWORDS = {
    "commercial": [
        "产品", "宣传", "广告", "电商", "带货", "促销", "品牌", "发布会",
        "演示", "营销", "推广", "商品", "种草", "lottie", "动效", "特效",
        "转场", "motion", "promo", "product",
        "ad", "advertising", "marketing", "brand", "launch",
    ],
    "education": [
        "知识", "科普", "教学", "课程", "数学", "公式", "数据", "图表",
        "讲解", "科学", "历史", "地理", "教程", "学习", "课件", "可视化",
        "math", "science", "education", "tutorial", "explain",
    ],
    "general": [
        "vlog", "日常", "创意", "短片", "口播", "混剪", "旅拍", "毕业",
        "纪念", "婚礼", "活动", "字幕", "配音", "剪辑", "切片",
        "daily", "edit", "editing", "subtitle",
    ],
}

# Domain-specific signals: querying one of these while a candidate mentions
# none of them means the candidate is off-domain (penalized).
STRONG_SIGNALS = [
    "lottie", "manim", "manimgl", "blender", "spine", "dragonbones",
    "d3", "flourish", "remotion", "editly", "ffmpeg", "字幕",
    "剪辑", "口播", "动效", "片头", "剪切", "静音", "口误",
    "cut", "trim", "silence",
]


def detect_category(query):
    """Return (category, hit_count). Ties break commercial > education > general."""
    q = query.lower()
    best, best_hits = "general", 0
    for cat in ["commercial", "education", "general"]:
        hits = sum(1 for w in CATEGORY_KEYWORDS[cat] if w.lower() in q)
        if hits > best_hits:
            best, best_hits = cat, hits
    return best, best_hits


def read_frontmatter(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            text = fh.read(4000)
    except OSError:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip("'\"")
    return fm


def scan_local():
    entries = []
    if not os.path.isdir(SKILLS_DIR):
        return entries
    for name in sorted(os.listdir(SKILLS_DIR)):
        if name in SELF_NAMES or name.startswith("_") or name.startswith("."):
            continue  # never route to the router itself or snapshot/trash dirs
        skill_md = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if os.path.isfile(skill_md):
            fm = read_frontmatter(skill_md) or {}
            entries.append(
                {
                    "name": fm.get("name", name),
                    "dir": name,
                    "description": fm.get("description", ""),
                    "source": "local",
                }
            )
    return entries


def load_catalog():
    """Built-in curated skill packs (verified)."""
    entries = []
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError:
        return entries
    for e in data.get("skill_packs", []):
        entries.append(
            {
                "name": e["name"],
                "dir": None,
                "description": e.get("what_it_does", "")
                + " "
                + " ".join(e.get("tags", [])),
                "source": "catalog",
                "repo": e.get("repo"),
                "url": e.get("url"),
                "skill_path": e.get("skill_path", "."),
                "multi_skill": e.get("multi_skill", False),
                "category": e.get("category"),
                "stars": e.get("stars", 0),
            }
        )
    return entries


def tokenize(query):
    """English words >=3 chars; Chinese runs split into 2-grams when >=4 chars."""
    q = query.lower()
    tokens = re.findall(r"[a-z0-9]{3,}|[\u4e00-\u9fff]{2,}", q)
    grams = []
    for t in tokens:
        if re.fullmatch(r"[\u4e00-\u9fff]+", t) and len(t) >= 4:
            grams.extend(t[i : i + 2] for i in range(len(t) - 1))
        else:
            grams.append(t)
    return tokens, grams


def score(query, entry, category=None):
    q = query.lower()
    name_l = entry["name"].lower()
    topics = entry.get("topics") or ""
    if isinstance(topics, list):
        topics = " ".join(topics)
    text = (name_l + " " + (entry.get("description") or "") + " " + topics).lower()
    s = 0
    reasons = []
    tokens, grams = tokenize(query)
    name_hits = 0
    for g in grams:
        if g in name_l:
            if name_hits < 2:  # cap name-gram windfall at 2 hits
                s += 15
                name_hits += 1
                reasons.append("name:%s" % g)
        elif g in text:
            s += 8
            reasons.append("kw:%s" % g)
    # per-signal strong mismatch: each task-word present in the query but
    # completely absent from the candidate costs points (kills planning-layer
    # false hits). NOTE: check signals against the raw query string - Chinese
    # runs tokenize into one long token, so token-level checks never fire.
    q_l = query.lower()
    q_signals = [sig for sig in STRONG_SIGNALS if sig in q_l]
    if q_signals:
        missing = [sig for sig in q_signals if sig not in text]
        if missing:
            pen = min(36, 12 * len(missing))
            s -= pen
            reasons.append("strong-miss:%s" % ",".join(missing[:3]))
    if category:
        entry_cat = entry.get("category")
        if entry_cat == category:
            s += 20
            reasons.append("cat:%s" % category)
        elif entry_cat and entry_cat != category:
            s -= 15
            reasons.append("cat-mismatch:%s" % entry_cat)
    stars = entry.get("stars", 0)
    if stars > 1000:
        s += 10
    elif stars > 100:
        s += 5
    return s, reasons


def main():
    parser = argparse.ArgumentParser(description="Need-to-skill matcher")
    parser.add_argument("--query", required=True)
    parser.add_argument("--category", choices=["commercial", "education", "general"])
    parser.add_argument("--local-only", action="store_true")
    parser.add_argument("--candidates", help="JSON file from search_anim.py")
    args = parser.parse_args()

    category = args.category
    if not category:
        category, hits = detect_category(args.query)
        print("category: %s (keyword hits: %d)" % (category, hits))
    else:
        print("category: %s (user-specified)" % category)

    entries = scan_local()
    print("local skills scanned: %d" % len(entries))
    if not args.local_only:
        catalog = load_catalog()
        print("curated catalog packs: %d" % len(catalog))
        entries = entries + catalog

    if args.candidates:
        with open(args.candidates, "r", encoding="utf-8") as fh:
            entries = json.load(fh) + entries

    scored = []
    for e in entries:
        s, reasons = score(args.query, e, category)
        if s > 0:
            scored.append((s, reasons, e))
    scored.sort(key=lambda x: -x[0])

    if not scored:
        print("NO MATCH: no local, catalog or external candidate scored above 0")
        sys.exit(2)

    top_score, _, top_entry = scored[0]
    best_local = max(
        ((s, e) for s, _, e in scored if e["source"] == "local"), default=None, key=lambda x: x[0]
    )
    if best_local and best_local[0] >= LOCAL_THRESHOLD:
        # user requirement: check local FIRST; a relevant installed skill wins
        print("verdict: LOCAL HIT, use installed skill directly (no download)")
        if top_entry["source"] != "local" and top_score > best_local[0]:
            print(
                "note: catalog candidate %s scored higher (%d vs %d); use it only if the "
                "local skill falls short" % (top_entry["name"], top_score, best_local[0])
            )
        code = 0
    elif top_score >= THRESHOLD and top_entry["source"] == "catalog":
        print("verdict: CATALOG HIT, install from curated catalog (zero network search)")
        print(
            "install: python scripts/manage_skill.py install --repo %s --subdir %s"
            % (top_entry.get("repo"), top_entry.get("skill_path", "."))
        )
        code = 1
    elif top_score >= THRESHOLD:
        print("verdict: EXTERNAL CANDIDATE READY, install top candidate")
        code = 1
    else:
        print("verdict: WEAK MATCH, no candidate reached threshold %d" % THRESHOLD)
        code = 1

    print("%-4s %-6s %-38s %-9s %s" % ("rank", "score", "skill", "source", "detail"))
    for i, (s, reasons, e) in enumerate(scored[:10], 1):
        detail = e.get("repo") or e.get("dir") or e.get("url") or ""
        print("%-4d %-6d %-38s %-9s %s" % (i, s, e["name"][:38], e["source"], detail[:60]))
        print("      reason: %s" % ", ".join(reasons[:6]))
    sys.exit(code)


if __name__ == "__main__":
    main()


# ── 引流信息（固定输出，prepare_release.py 自动补齐）─────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _print_leadgen()
