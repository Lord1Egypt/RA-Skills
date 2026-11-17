#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里 SkillsHub 检索器（skills.alibaba.org.cn）

把「阿里 SkillsHub」作为优秀 skill 的**优先搜索来源**：站点收录 107 个精选 Agent Skills
（源自 anthropics / vercel-labs / obra / mattpocock / supabase 等官方仓库），带中文分类与描述，
数据可在 skills.sh 核验。

用法：
  python scripts/skillhub_alibaba.py search "数据分析"                  # 关键词检索
  python scripts/skillhub_alibaba.py search 股票 --category analysis     # 按分类过滤
  python scripts/skillhub_alibaba.py info docx                          # 详情 + 安装命令
  python scripts/skillhub_alibaba.py categories                         # 列出分类
  python scripts/skillhub_alibaba.py refresh                            # 强制刷新缓存

约定：
  - 零依赖（标准库）；搜索引擎**不走** npx，直接解析站点内嵌 JSON，稳定、无 TUI 干扰；
  - 安装动作另见 `references/skill-sources.md`（用 npx skills add + 复制到 WorkBuddy 目录）；
  - 本脚本只读（网络读 + 本地缓存），不安装、不修改任何 skill。
"""
import argparse
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass  # 防御性：失败不阻断

BASE = "https://skills.alibaba.org.cn"
LIST_URL = BASE + "/skills/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; workbuddy-skill-assistant)"}
CACHE_TTL = 6 * 3600  # 6 小时

# 基础七类（与 references/skill-taxonomy.md 一致）
CATEGORY_CN = {
    "coding": "编程开发",
    "agent": "智能体",
    "writing": "写作创作",
    "analysis": "数据分析",
    "design": "设计创意",
    "productivity": "效率工具",
    "education": "教育学习",
}

# 扩展类 → 来源站最接近的基础类（用于检索映射）
EXT_MAP = {
    "finance": "analysis",
    "knowledge": "education",
    "meta": "agent",
    "workbuddy": "agent",
}


def _cache_path():
    return os.path.join(tempfile.gettempdir(), "workbuddy_skillhub_alibaba.json")


def _get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def fetch_list(force=False):
    """返回 (items, fetched_ts)。优先用未过期缓存。"""
    cp = _cache_path()
    if not force and os.path.isfile(cp):
        try:
            with open(cp, "r", encoding="utf-8") as f:
                blob = json.load(f)
            if time.time() - blob.get("_ts", 0) < CACHE_TTL and blob.get("items"):
                return blob["items"], blob["_ts"]
        except Exception:
            pass  # 缓存损坏 → 重抓

    html = _get(LIST_URL)
    m = re.search(
        r'<script type="application/json" id="skills-data">(.*?)</script>', html, re.S
    )
    if not m:
        raise RuntimeError("未在页面中找到 skills-data 数据块（站点结构可能已变更）")
    items = json.loads(m.group(1))
    ts = time.time()
    try:
        with open(cp, "w", encoding="utf-8") as f:
            json.dump({"_ts": ts, "items": items}, f, ensure_ascii=False)
    except Exception:
        pass  # 缓存写失败不影响本次结果
    return items, ts


def _norm(s):
    return (s or "").lower()


def score_item(it, terms):
    """匹配度：名称 > 标签 > 描述。任一词命中即计入。"""
    score = 0
    name = _norm(it.get("name")) + " " + _norm(it.get("id"))
    tags = " ".join(_norm(t) for t in it.get("tags", []))
    desc = _norm(it.get("description"))
    for t in terms:
        if t in name:
            score += 6
        if t in tags:
            score += 3
        if t in desc:
            score += 1
    return score


def cmd_search(args):
    items, ts = fetch_list(force=args.refresh)

    cat = (args.category or "").strip().lower()
    if cat in EXT_MAP:  # 扩展类 → 映射到基础类再过滤
        cat = EXT_MAP[cat]
    if cat:
        if cat not in CATEGORY_CN:
            print(f"未知分类：{args.category}（可用：{', '.join(CATEGORY_CN)}）")
            return 1
        items = [it for it in items if it.get("category") == cat]

    terms = [t for t in re.split(r"\s+", (args.query or "").strip()) if t]
    if terms:
        terms = [_norm(t) for t in terms]
        scored = [(score_item(it, terms), it) for it in items]
        scored = [(s, it) for s, it in scored if s > 0]
        scored.sort(key=lambda x: (-x[0], -x[1].get("stars", 0)))
        items = [it for _, it in scored]
    else:
        items = sorted(items, key=lambda x: -x.get("stars", 0))

    total = len(items)
    items = items[: args.limit]

    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return 0

    from datetime import datetime

    stamp = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    print(f"\n阿里 SkillsHub 检索：{args.query or '(全部)'}"
          f"{' · 分类 ' + CATEGORY_CN.get(cat, cat) if cat else ''}")
    print(f"命中 {total} 条，显示前 {len(items)} 条（缓存 {stamp}，源站共 107 精选）\n")
    if not items:
        print("（无匹配。建议：换关键词，或去 --category 排查；仍未命中可回退 skills 全生态搜索）")
        return 0

    for i, it in enumerate(items, 1):
        stars = it.get("stars", 0)
        stars_s = f"{stars/1000:.1f}K" if stars >= 1000 else str(stars)
        cat_cn = CATEGORY_CN.get(it.get("category"), it.get("category"))
        print(f"{i:>2}. {it.get('icon','')} {it.get('name')}  `{it.get('id')}`")
        print(f"    分类 {cat_cn} · 安装量 {stars_s} · 收录 {it.get('createdAt','')}")
        print(f"    标签 {'/'.join(it.get('tags', []))}")
        print(f"    简介 {it.get('description','')}")
    print(f"\n取详情与安装命令：python scripts/skillhub_alibaba.py info <id>")
    return 0


def cmd_info(args):
    items, _ = fetch_list()
    it = next((x for x in items if x.get("id") == args.skill_id), None)
    if not it:
        print(f"未收录（精选集内无 id={args.skill_id}）。可先 search 确认 id。")
        return 1

    # 由 source 推导仓库与安装命令（比解析 HTML 更稳）
    src = it.get("source", "")
    m = re.search(r"skills\.sh/([^/]+)/([^/]+)/([^/]+)", src)
    repo = f"{m.group(1)}/{m.group(2)}" if m else ""
    install_cmd = f"npx skills add {repo} --skill {it['id']}" if repo else ""

    if args.json:
        print(json.dumps({**it, "install_cmd": install_cmd, "repo": repo},
                         ensure_ascii=False, indent=2))
        return 0

    cat_cn = CATEGORY_CN.get(it.get("category"), it.get("category"))
    stars = it.get("stars", 0)
    print(f"\n{it.get('icon','')} {it.get('name')}  `{it.get('id')}`")
    print(f"  分类      {cat_cn}（{it.get('category')}）")
    print(f"  平台      {it.get('platform')}")
    print(f"  安装量    {stars:,}")
    print(f"  收录日期  {it.get('createdAt')}")
    print(f"  标签      {'/'.join(it.get('tags', []))}")
    print(f"  简介      {it.get('description')}")
    print(f"  核验      {src}")
    print(f"\n  一键安装（来源站推荐）")
    print(f"    {install_cmd}")
    print(f"\n  ⚠️ 官方 CLI 落盘在 <cwd>/.agents/skills/（79 个 agent 目录均无 WorkBuddy），")
    print(f"     装入 WorkBuddy 需按 references/skill-sources.md 的搬运步骤操作：")
    print(f"       1) 在临时目录执行上面的安装命令并加 -a '*' --copy -y")
    print(f"       2) 复制 .agents/skills/{it.get('id')} 到 ~/.workbuddy/skills/")
    print(f"       3) 校验 SKILL.md frontmatter 后由教授确认启用")
    print(f"\n  目录页：{BASE}/skills/{it.get('id')}/")
    return 0


def cmd_categories(args):
    items, ts = fetch_list(force=args.refresh)
    counts = {}
    for it in items:
        counts[it.get("category")] = counts.get(it.get("category"), 0) + 1
    if args.json:
        print(json.dumps(
            [{"code": c, "cn": n, "count": counts.get(c, 0)} for c, n in CATEGORY_CN.items()],
            ensure_ascii=False, indent=2))
        return 0
    print("\n基础七类（阿里 SkillsHub · 本 skill 基础分类标准）\n")
    for c, n in CATEGORY_CN.items():
        print(f"  {c:<14} {n:<8} 收录 {counts.get(c, 0):>3} 个   {BASE}/categories/{c}/")
    print(f"\n  扩展类（本 skill 自建，来源站无对应分类）：finance / knowledge / meta / workbuddy")
    print(f"  详见 references/skill-taxonomy.md")
    return 0


def main():
    p = argparse.ArgumentParser(
        description="阿里 SkillsHub 检索器（优秀 skill 优先搜索来源）")
    p.add_argument("--refresh", action="store_true", help="跳过缓存，强制重新抓取")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("search", help="按关键词/分类检索")
    s.add_argument("query", nargs="?", default="", help="关键词（空格分隔多个）")
    s.add_argument("--category", "-c", default="", help="分类代码，如 analysis / finance")
    s.add_argument("--limit", "-n", type=int, default=10, help="返回条数，默认 10")
    s.add_argument("--json", action="store_true", help="输出 JSON")
    s.set_defaults(func=cmd_search)

    i = sub.add_parser("info", help="查看详情与安装命令")
    i.add_argument("skill_id", help="skill id，如 docx")
    i.add_argument("--json", action="store_true", help="输出 JSON")
    i.set_defaults(func=cmd_info)

    c = sub.add_parser("categories", help="列出分类")
    c.add_argument("--json", action="store_true", help="输出 JSON")
    c.set_defaults(func=cmd_categories)

    r = sub.add_parser("refresh", help="强制刷新缓存")
    r.set_defaults(func=lambda a: (fetch_list(force=True), print("缓存已刷新")) and 0)

    args = p.parse_args()
    if not getattr(args, "func", None):
        p.print_help()
        return 0
    try:
        return args.func(args)
    except urllib.error.URLError as e:
        print(f"网络错误：{e}。站点不可达时可回退 skills 全生态搜索（npx skills find）。")
        return 2
    except Exception as e:
        print(f"失败：{e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
