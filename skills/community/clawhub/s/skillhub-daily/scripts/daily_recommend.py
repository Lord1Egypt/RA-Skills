#!/usr/bin/env python3
"""
SkillHub.cn 每日推荐生成器 v3.0
7 维度推荐 + 3 级权重记忆碰撞 + 7 天去重 + evaluation/reports 深度评估
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

SKILLHUB_BIN = shutil.which("skillhub") or os.environ.get("SKILLHUB_BIN", "skillhub")

# ── 7 大痛点场景库 ──
PAIN_POINTS = {
    "自动化办公": {
        "categories": ["office-efficiency"],
        "sub_categories": ["office-doc", "office-pdf", "office-spreadsheet", "office-presentation"],
        "keywords": ["办公", "文档", "表格", "PPT", "Word", "Excel", "自动化", "流程", "审批"],
    },
    "开发工具": {
        "categories": ["dev-programming", "it-ops-security"],
        "sub_categories": ["dev-code-gen", "dev-script", "dev-debug", "dev-deploy", "dev-testing"],
        "keywords": ["开发", "编程", "代码", "部署", "调试", "CLI", "API", "git", "测试"],
    },
    "内容创作": {
        "categories": ["content-creation", "design-media"],
        "sub_categories": ["content-article", "content-rewrite", "content-video", "design-image-gen", "design-poster"],
        "keywords": ["写作", "文章", "公众号", "文案", "视频", "设计", "封面", "排版", "配图"],
    },
    "数据采集": {
        "categories": ["data-analysis"],
        "sub_categories": ["data-web-scraping", "data-search", "data-report", "data-insight"],
        "keywords": ["搜索", "抓取", "爬虫", "数据", "分析", "查询", "研究", "可视化"],
    },
    "AI 增强": {
        "categories": ["ai-agent"],
        "sub_categories": ["agent-task-automation", "agent-tool-use", "agent-memory", "agent-workflow", "agent-multi-agent", "agent-context"],
        "keywords": ["AI", "智能", "提示词", "Agent", "生成", "大模型", "记忆", "工作流"],
    },
    "中文支持": {
        "categories": [],
        "sub_categories": [],
        "keywords": ["中文", "国内", "腾讯", "微信", "飞书", "企业微信", "小红书", "抖音", "公众号"],
    },
    "金融分析": {
        "categories": ["professional"],
        "sub_categories": ["pro-finance", "pro-research"],
        "keywords": ["股票", "投资", "金融", "财报", "估值", "选股", "行情", "审计", "税务"],
    },
}

# ── 中国/国内适配关键词 ──
CHINA_SIGNALS = [
    "中文", "国内", "腾讯", "微信", "飞书", "企业微信", "小红书", "抖音", "公众号",
    "淘宝", "京东", "拼多多", "钉钉", "支付宝", "百度", "华为", "国产", "汉化",
    "lark", "feishu", "wechat", "weixin", "dingtalk", "chinese",
]

# ── 技术关键词提取库 ──
TECH_KEYWORDS = [
    "Python", "JavaScript", "TypeScript", "React", "Vue", "Node",
    "飞书", "ClawHub", "GitHub", "Agent", "Skill", "openclaw",
    "定时任务", "自动化", "审计", "财务", "税务", "税务筹划",
    "数据分析", "报告", "推送", "IMA", "知识库", "记忆",
    "skillhub", "clawhub", "feishu", "lark",
    "OCR", "PDF", "Excel", "PPT", "Word",
    "MCP", "plugin", "skill", "cron",
    "Git", "CI/CD", "Docker", "deploy",
]


def extract_tech_keywords(text):
    """从文本中提取技术关键词"""
    found = []
    text_lower = text.lower()
    for kw in TECH_KEYWORDS:
        if kw.lower() in text_lower:
            found.append(kw)
    return found


def load_user_memory_keywords():
    """3 级权重关键词提取：project_memory ×3, topics ×2, user_profile ×1
    路径通过 TRAE_MEMORY_PATH 环境变量配置，不硬编码。
    """
    keywords = {}
    memory_root = Path(os.environ.get("TRAE_MEMORY_PATH", ""))
    if not memory_root.exists():
        return keywords

    project_memory_dir = memory_root / "projects" / "-d-TRAE-SOLO-CN-project"

    # Level 3: project_memory.md (weight=3)
    pm = project_memory_dir / "project_memory.md"
    if pm.exists():
        for kw in extract_tech_keywords(pm.read_text(encoding="utf-8", errors="ignore")):
            keywords[kw] = max(keywords.get(kw, 0), 3)

    # Level 2: topics.md (weight=2) — 取最近一天的
    if project_memory_dir.exists():
        for date_dir in sorted(project_memory_dir.iterdir(), reverse=True):
            if date_dir.is_dir() and not date_dir.name.startswith(".") and date_dir.name[0].isdigit():
                topics = date_dir / "topics.md"
                if topics.exists():
                    for kw in extract_tech_keywords(topics.read_text(encoding="utf-8", errors="ignore")):
                        keywords[kw] = max(keywords.get(kw, 0), 2)
                    break

    # Level 1: user_profile.md (weight=1)
    up = memory_root / "user_profile.md"
    if up.exists():
        for kw in extract_tech_keywords(up.read_text(encoding="utf-8", errors="ignore")):
            keywords[kw] = max(keywords.get(kw, 0), 1)

    return keywords


def collision_score(skill, user_keywords):
    """计算记忆碰撞分数（3 级权重）"""
    if not user_keywords:
        return 0
    search_text = " ".join([
        skill.get("description_zh", ""),
        skill.get("description", ""),
        skill.get("name", ""),
        skill.get("category", ""),
        skill.get("category_zh", ""),
        " ".join(sc.get("name", "") if isinstance(sc, dict) else str(sc) for sc in skill.get("subCategories", [])),
        " ".join(sc.get("key", "") if isinstance(sc, dict) else str(sc) for sc in skill.get("subCategories", [])),
    ]).lower()

    score = 0
    hit_keywords = []
    for keyword, weight in user_keywords.items():
        if keyword.lower() in search_text:
            score += weight
            hit_keywords.append(keyword)
    return score, hit_keywords


def pain_point_score(skill):
    """计算痛点场景匹配分数，返回 {场景: 分数}"""
    scores = {}
    cat = skill.get("category", "")
    sub_cats = []
    for sc in skill.get("subCategories", []):
        if isinstance(sc, dict):
            sub_cats.append(sc.get("key", ""))
        else:
            sub_cats.append(str(sc))
    desc_zh = skill.get("description_zh", "") + " " + skill.get("description", "")

    for scene, config in PAIN_POINTS.items():
        score = 0
        if cat in config["categories"]:
            score += 3
        for sc in sub_cats:
            if sc in config["sub_categories"]:
                score += 2
        for kw in config["keywords"]:
            if kw.lower() in desc_zh.lower():
                score += 1
        if score > 0:
            scores[scene] = score
    return scores


def is_china_relevant(skill):
    """判断技能是否与中国/国内适配强相关"""
    search_text = " ".join([
        skill.get("description_zh", ""),
        skill.get("description", ""),
        skill.get("name", ""),
        " ".join(sc.get("name", "") if isinstance(sc, dict) else str(sc) for sc in skill.get("subCategories", [])),
    ]).lower()
    hits = [sig for sig in CHINA_SIGNALS if sig.lower() in search_text]
    return len(hits), hits


def find_active_developers(skills):
    """发现活跃开发者：按 ownerName 聚合，计算活跃度分数"""
    dev_stats = {}
    for s in skills:
        owner = s.get("ownerName", "").strip()
        if not owner:
            continue
        if owner not in dev_stats:
            dev_stats[owner] = {
                "name": owner,
                "skills": [],
                "total_installs": 0,
                "total_downloads": 0,
                "total_stars": 0,
                "ranking_count": 0,
            }
        dev_stats[owner]["skills"].append(s.get("slug", ""))
        dev_stats[owner]["total_installs"] += s.get("installs", 0)
        dev_stats[owner]["total_downloads"] += s.get("downloads", 0)
        dev_stats[owner]["total_stars"] += s.get("stars", 0)
        if s.get("_rankings"):
            dev_stats[owner]["ranking_count"] += len(s["_rankings"])

    # 活跃度 = 技能数 × 1 + 总安装/1000 + 上榜次数 × 5
    for dev in dev_stats.values():
        dev["activity_score"] = (
            len(dev["skills"]) * 1
            + dev["total_installs"] / 1000
            + dev["ranking_count"] * 5
        )

    # 排序，取 top 开发者
    sorted_devs = sorted(dev_stats.values(), key=lambda x: x["activity_score"], reverse=True)
    return sorted_devs


def load_dedup_set(data_dir, window_days=7):
    """加载 7 天去重集合"""
    dedup = set()
    rec_dir = Path(data_dir) / "recommended"
    if not rec_dir.exists():
        return dedup
    today = datetime.now().date()
    for i in range(1, window_days + 1):
        date_str = (today - timedelta(days=i)).isoformat()
        rec_file = rec_dir / f"{date_str}.json"
        if rec_file.exists():
            with open(rec_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for rec in data.get("recommendations", []):
                    dedup.add(rec.get("slug", ""))
    return dedup


def fetch_evaluation(slug):
    """调用 skillhub skill evaluation 获取 AI 质量评估"""
    try:
        result = subprocess.run(
            [SKILLHUB_BIN, "skill", "evaluation", slug, "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            # 解析 JSON
            output = result.stdout.strip()
            for marker in ['{"', '{"evaluation"', '{"slug"']:
                idx = output.find(marker)
                if idx >= 0:
                    try:
                        return json.loads(output[idx:])
                    except:
                        pass
            try:
                return json.loads(output)
            except:
                pass
    except:
        pass
    return None


def fetch_reports(slug):
    """调用 skillhub skill reports 获取双实验室安全审计"""
    try:
        result = subprocess.run(
            [SKILLHUB_BIN, "skill", "reports", slug, "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            output = result.stdout.strip()
            for marker in ['{"', '{"reports"', '{"slug"']:
                idx = output.find(marker)
                if idx >= 0:
                    try:
                        return json.loads(output[idx:])
                    except:
                        pass
            try:
                return json.loads(output)
            except:
                pass
    except:
        pass
    return None


def recommend(skills, user_keywords, dedup_set):
    """7 维度推荐 v3.0"""
    recommendations = []
    added_slugs = set()

    # 过滤已推荐的
    candidates = [s for s in skills if s.get("slug") not in dedup_set]

    # ── D1: trending_surge × 2 — 同时在 hot + trending ──
    rankings_map = {}
    for s in candidates:
        slug = s.get("slug", "")
        rks = s.get("_rankings", [])
        if rks:
            rankings_map[slug] = rks

    hot_slugs = {s["slug"] for s in candidates if "hot" in s.get("_rankings", [])}
    trending_slugs = {s["slug"] for s in candidates if "trending" in s.get("_rankings", [])}
    surge_candidates = [s for s in candidates if s["slug"] in hot_slugs & trending_slugs]
    surge_candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
    for s in surge_candidates[:2]:
        if s["slug"] not in added_slugs:
            rec = {**s, "dimension": "trending_surge",
                   "reason": f"热门+趋势双榜，综合评分 {s.get('score', 0):.0f}"}
            recommendations.append(rec)
            added_slugs.add(s["slug"])

    # ── D2: newcomers × 1 — newest 榜 + 30 天内 + installs > 100 ──
    now_ms = int(datetime.now().timestamp() * 1000)
    thirty_days_ms = 30 * 24 * 3600 * 1000
    newcomers = [s for s in candidates
                 if "newest" in s.get("_rankings", [])
                 and (now_ms - s.get("created_at", 0)) < thirty_days_ms
                 and s.get("installs", 0) > 100]
    newcomers.sort(key=lambda x: x.get("installs", 0), reverse=True)
    for s in newcomers[:1]:
        if s["slug"] not in added_slugs:
            days_old = max(1, (now_ms - s.get("created_at", 0)) / (24 * 3600 * 1000))
            rec = {**s, "dimension": "newcomers",
                   "reason": f"新星上线 {int(days_old)} 天，安装量 {s.get('installs', 0):,}"}
            recommendations.append(rec)
            added_slugs.add(s["slug"])

    # ── D3: scene_match × 2 — 痛点场景匹配 ──
    scored = [(s, pain_point_score(s)) for s in candidates]
    scored = [(s, pp) for s, pp in scored if pp]
    scored.sort(key=lambda x: max(x[1].values()) * (1 + x[0].get("downloads", 0) / 100000), reverse=True)
    scenes_covered = set()
    for s, pp in scored:
        if s["slug"] not in added_slugs and len(scenes_covered) < 2:
            top_scene = max(pp, key=pp.get)
            if top_scene not in scenes_covered:
                rec = {**s, "dimension": "scene_match",
                       "reason": f"痛点匹配【{top_scene}】，{s.get('category_zh', '')}"}
                recommendations.append(rec)
                added_slugs.add(s["slug"])
                scenes_covered.add(top_scene)

    # ── D4: memory_collision × 1 — 记忆碰撞 ──
    mem_scored = [(s, *collision_score(s, user_keywords)) for s in candidates]
    mem_scored = [(s, sc, hits) for s, sc, hits in mem_scored if sc > 0]
    mem_scored.sort(key=lambda x: x[1], reverse=True)
    for s, sc, hits in mem_scored[:1]:
        if s["slug"] not in added_slugs:
            rec = {**s, "dimension": "memory_collision",
                   "reason": f"记忆碰撞匹配（权重 {sc}）"}
            recommendations.append(rec)
            added_slugs.add(s["slug"])

    # ── D5: china_first × 1 — 中国/国内优先（最低门槛：50 安装或 10 星）──
    china_candidates = []
    for s in candidates:
        cn_score, cn_hits = is_china_relevant(s)
        if cn_score > 0 and (s.get("installs", 0) >= 50 or s.get("stars", 0) >= 10):
            china_candidates.append((s, cn_score, cn_hits))
    # 门槛不够时降级：去掉最低门槛
    if not china_candidates:
        for s in candidates:
            cn_score, cn_hits = is_china_relevant(s)
            if cn_score > 0:
                china_candidates.append((s, cn_score, cn_hits))
    china_candidates.sort(key=lambda x: x[1] * (1 + x[0].get("installs", 0) / 5000), reverse=True)
    for s, cn_score, cn_hits in china_candidates[:1]:
        if s["slug"] not in added_slugs:
            rec = {**s, "dimension": "china_first",
                   "reason": f"国内适配（{', '.join(cn_hits[:3])}），安装 {s.get('installs', 0):,}"}
            recommendations.append(rec)
            added_slugs.add(s["slug"])

    # ── D6: active_developer × 1 — 活跃开发者 ──
    dev_stats = find_active_developers(candidates)
    # 选活跃度最高的开发者，推荐他评分最高的技能
    for dev in dev_stats:
        if len(dev["skills"]) < 2:
            continue
        # 找该开发者评分最高的、未被推荐的技能
        dev_slugs = set(dev["skills"])
        dev_skills = [s for s in candidates if s["slug"] in dev_slugs and s["slug"] not in added_slugs]
        if dev_skills:
            dev_skills.sort(key=lambda x: x.get("score", 0), reverse=True)
            best = dev_skills[0]
            rec = {**best, "dimension": "active_developer",
                   "reason": f"活跃开发者【{dev['name']}】({len(dev['skills'])}个技能，总安装 {dev['total_installs']:,})"}
            recommendations.append(rec)
            added_slugs.add(best["slug"])
            break

    # ── D7: tencent_official × 1(可选) — 腾讯官方认证 ──
    verified_skills = [s for s in candidates if s.get("verified")]
    if verified_skills:
        verified_skills.sort(key=lambda x: x.get("downloads", 0), reverse=True)
        for s in verified_skills[:1]:
            if s["slug"] not in added_slugs:
                rec = {**s, "dimension": "tencent_official",
                       "reason": "腾讯官方认证，品质保障"}
                recommendations.append(rec)
                added_slugs.add(s["slug"])

    # 如果不足 8 个，从 scene_match 补充
    if len(recommendations) < 8:
        for s, pp in scored:
            if s["slug"] not in added_slugs:
                top_scene = max(pp, key=pp.get)
                rec = {**s, "dimension": "scene_match",
                       "reason": f"痛点匹配【{top_scene}】（补充）"}
                recommendations.append(rec)
                added_slugs.add(s["slug"])
                if len(recommendations) >= 8:
                    break

    return recommendations[:8]


def _next_action(rec, scene):
    """生成下一步行动建议"""
    cat = rec.get("category", "")
    templates = {
        "office-efficiency": "试试用 {name} 优化你的办公流程",
        "dev-programming": "在 IDE 中安装 {name} 并试试效果",
        "content-creation": "用 {name} 改写你最近一篇内容",
        "data-analysis": "用 {name} 分析你手头的数据",
        "ai-agent": "把 {name} 加入你的 Agent 工具箱",
        "design-media": "用 {name} 生成你的下一个设计稿",
        "professional": "用 {name} 加速你的专业工作流",
        "it-ops-security": "用 {name} 加强你的运维安全",
        "life-service": "试试 {name} 提升日常效率",
        "business-ops": "用 {name} 优化你的商业运营",
    }
    tmpl = templates.get(cat, "安装 {name} 试试看")
    return tmpl.format(name=rec.get("name", rec.get("slug", "")))


def _capability_summary(rec):
    """生成能力解读（0 token，基于字段拼装）"""
    cat_zh = rec.get("category_zh", "")
    parts = []
    if cat_zh:
        parts.append(f"面向「{cat_zh}」场景")
    subs = rec.get("subCategories", [])
    if subs:
        names = [sc.get("name", "") if isinstance(sc, dict) else str(sc) for sc in subs[:3]]
        names = [n for n in names if n]
        if names:
            parts.append("整合 " + "、".join(names) + " 等能力")
    if rec.get("requires_api_key"):
        parts.append("需配置密钥")
    if rec.get("verified"):
        parts.append("腾讯官方认证")
    return "，".join(parts) if parts else "通用工具类技能"


def _matched_scenes(rec):
    """返回该技能匹配的痛点场景列表"""
    pp = pain_point_score(rec)
    return list(pp.keys())


def _scene_icon(scene):
    """痛点场景 emoji"""
    icons = {
        "自动化办公": "🤖", "开发工具": "🛠️", "内容创作": "✍️",
        "数据采集": "🕷️", "AI 增强": "🧠", "中文支持": "🇨🇳", "金融分析": "💰",
    }
    return icons.get(scene, "📌")


def generate_briefing_md(recommendations, date_str, meta=None, dev_summary=None):
    """生成中文简报 Markdown（参考 ClawHub Daily 风格，突出 SkillHub Daily 差异化）"""
    lines = []

    # ── Header ──
    lines.append(f"# 🐙 SkillHub Daily | {date_str}")
    lines.append("")
    lines.append(f"> 每日扫描 SkillHub.cn 7.5 万+ 技能生态 | 与 ClawHub Daily 互补：聚焦**国内适配**、**活跃开发者**、**双实验室安全审计**")
    lines.append("")

    # ── 统计栏 ──
    total = meta.get("total_scanned", 0) if meta else 0
    dedup = meta.get("dedup_count", 0) if meta else 0
    mem_kw = meta.get("memory_kw_count", 0) if meta else 0
    lines.append(f"📦 扫描: {total} | 🆕 推荐: {len(recommendations)} | 🚫 去重: {dedup} | 🧠 记忆碰撞: {mem_kw} 关键词")
    lines.append("")

    # ── TL;DR ──
    all_scenes = set()
    for rec in recommendations:
        for s in _matched_scenes(rec):
            all_scenes.add(s)
    scene_str = "、".join(f"{_scene_icon(s)} {s}" for s in sorted(all_scenes)) if all_scenes else "无"
    lines.append("## TL;DR")
    lines.append("")
    china_count = sum(1 for r in recommendations if r.get("dimension") == "china_first")
    dev_count = sum(1 for r in recommendations if r.get("dimension") == "active_developer")
    lines.append(f"今天推荐 **{len(recommendations)}** 个 Skill，其中 **{china_count}** 个国内优先、**{dev_count}** 个来自活跃开发者 | 场景匹配: {scene_str}")
    lines.append("")

    # ── 特色定位 ──
    lines.append("> **SkillHub Daily 特色**：🇨🇳 国内优先 | 👤 活跃开发者发现 | 🔬 双实验室安全审计 | 📊 AI 6维质量评估 | 与 ClawHub Daily（口碑精品/趋势洞察）互补")
    lines.append("")

    lines.append("---")
    lines.append("")

    # ── 活跃开发者速览 ──
    if dev_summary:
        lines.append("## 👤 活跃开发者速览")
        lines.append("")
        lines.append("> SkillHub Daily 独有维度：追踪高产开发者，帮你发现值得关注的技能作者")
        lines.append("")
        for dev in dev_summary[:5]:
            top_slugs = dev["skills"][:3]
            lines.append(f"- **{dev['name']}** — {len(dev['skills'])} 个技能 | "
                        f"总安装 {dev['total_installs']:,} | 上榜 {dev['ranking_count']} 次 | "
                        f"代表作: `{', '.join(top_slugs)}`")
        lines.append("")
        lines.append("---")
        lines.append("")

    # ── 推荐详情（按维度分组）──
    dim_icons = {
        "trending_surge": "🔥", "newcomers": "🚀", "scene_match": "🎯",
        "memory_collision": "🧠", "china_first": "🇨🇳", "active_developer": "👤",
        "tencent_official": "🏢",
    }
    dim_names = {
        "trending_surge": "趋势飙升", "newcomers": "新星上线",
        "scene_match": "痛点匹配", "memory_collision": "记忆碰撞",
        "china_first": "国内优先", "active_developer": "活跃开发者",
        "tencent_official": "官方认证",
    }
    dim_descriptions = {
        "trending_surge": "同时登上 hot + trending 双榜的技能，热度与趋势兼具",
        "newcomers": "30 天内上线的新技能，安装量快速增长中",
        "scene_match": "基于 7 大痛点场景库匹配，直击你的工作需求",
        "memory_collision": "与你项目记忆关键词碰撞，个性化推荐",
        "china_first": "深度适配国内生态（飞书/微信/钉钉/小红书等），SkillHub Daily 独有",
        "active_developer": "来自高产开发者的代表作，SkillHub Daily 独有",
        "tencent_official": "腾讯官方认证技能，品质保障",
    }

    # 按维度分组
    dim_groups = {}
    for rec in recommendations:
        d = rec.get("dimension", "other")
        dim_groups.setdefault(d, []).append(rec)

    # 按维度优先级排序输出
    dim_order = ["trending_surge", "newcomers", "china_first", "active_developer", "memory_collision", "scene_match", "tencent_official"]

    for dim_key in dim_order:
        recs_in_dim = dim_groups.get(dim_key, [])
        if not recs_in_dim:
            continue
        icon = dim_icons.get(dim_key, "📌")
        dim_name = dim_names.get(dim_key, dim_key)
        dim_desc = dim_descriptions.get(dim_key, "")

        lines.append(f"## {icon} {dim_name}")
        if dim_desc:
            lines.append(f"> {dim_desc}")
        lines.append("")

        for idx, rec in enumerate(recs_in_dim, 1):
            name = rec.get("name", rec.get("slug", "unknown"))
            slug = rec.get("slug", "")
            owner = rec.get("ownerName", "")
            lines.append(f"### {idx}. {name}")
            lines.append("")
            # 作者 + 链接
            if owner:
                lines.append(f"- **作者**: {owner} (`{slug}`)")
            else:
                lines.append(f"- **Slug**: `{slug}`")
            if rec.get("homepage"):
                lines.append(f"- **链接**: {rec['homepage']}")
            # 数据指标
            downloads = rec.get("downloads", 0)
            installs = rec.get("installs", 0)
            stars = rec.get("stars", 0)
            score = rec.get("score", 0)
            install_rate = f"{installs / max(downloads, 1) * 100:.1f}%" if downloads > 0 else "N/A"
            lines.append(f"- **数据**: ⭐ {stars:,} | 📥 {downloads:,} | 📊 安装 {installs:,} | 📈 安装率 {install_rate} | 评分 {score:.0f}")
            # 能力解读
            lines.append(f"- **能力解读**: {_capability_summary(rec)}")
            # 匹配场景
            scenes = _matched_scenes(rec)
            if scenes:
                scene_display = "、".join(f"{_scene_icon(s)} {s}" for s in scenes)
                lines.append(f"- **匹配场景**: {scene_display}")
            # 推荐理由
            lines.append(f"- **推荐理由**: {rec.get('reason', '')}")
            # 下一步
            lines.append(f"- **下一步**: {_next_action(rec, scenes[0] if scenes else '')}")
            # 原文摘要（折叠）
            desc = rec.get("description_zh", "") or rec.get("description", "")
            if desc:
                desc_short = desc[:200]
                lines.append(f"- <details><summary>原文摘要</summary>{desc_short}</details>")
            # evaluation 亮点
            eval_data = rec.get("evaluation")
            if eval_data:
                overall = eval_data.get("overall_score") or eval_data.get("score")
                if overall is not None:
                    lines.append(f"- **AI 质量评估**: {overall}/100")
            # reports 亮点
            reports_data = rec.get("reports")
            if reports_data:
                issues = reports_data.get("total_issues") or reports_data.get("critical_count")
                if issues is not None:
                    lines.append(f"- **安全审计**: {issues} 个问题")
            lines.append("")

        lines.append("---")
        lines.append("")

    # ── 痛点匹配按场景分组 ──
    scene_map = {}
    for rec in recommendations:
        for s in _matched_scenes(rec):
            scene_map.setdefault(s, []).append(rec)
    if scene_map:
        lines.append("## 🎯 痛点匹配（按场景分组）")
        lines.append("")
        for scene in sorted(scene_map.keys()):
            lines.append(f"### {_scene_icon(scene)} {scene}")
            for rec in scene_map[scene]:
                name = rec.get("name", rec.get("slug", ""))
                cap = _capability_summary(rec)
                lines.append(f"- **{name}** — {cap}")
            lines.append("")

    lines.append("---")
    lines.append("")

    # ── 数据说明 ──
    lines.append("## 📌 数据说明")
    lines.append("")
    lines.append(f"- **数据源**: SkillHub.cn（7.5 万+ 技能） + skillhub CLI")
    lines.append(f"- **扫描规模**: 7 排行榜 × 100 + 11 分类 × 20 搜索 + 6 关键词 × 20 搜索 ≈ 1000+ 候选")
    lines.append(f"- **去重窗口**: 7 天跨维度去重")
    lines.append(f"- **深度评估**: evaluation（6 维度 AI 评分） + reports（双实验室安全审计）")
    lines.append("")
    lines.append("## 🐙 与 ClawHub Daily 互补")
    lines.append("")
    lines.append("| | SkillHub Daily | ClawHub Daily |")
    lines.append("|---|---|---|")
    lines.append("| 平台 | SkillHub.cn（7.5 万+） | ClawHub.ai（500） |")
    lines.append("| 特色 | 🇨🇳 国内优先 / 👤 开发者 / 🔬 安全审计 | 🦞 口碑精品 / 趋势洞察 |")
    lines.append("| 评估 | AI 6维评分 + 双实验室审计 | 口碑率 + 活跃度 |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("觉得推荐不准？调整 `scripts/daily_recommend.py` 中的 `PAIN_POINTS` 和 `MEMORY_SEARCH_KEYWORDS`。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SkillHub.cn 每日推荐 v3.0")
    parser.add_argument("--date", default=None, help="日期 YYYY-MM-DD")
    parser.add_argument("--data-dir", default="data", help="数据目录")
    parser.add_argument("--skip-eval", action="store_true", help="跳过 evaluation/reports 调用")
    args = parser.parse_args()

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    data_dir = Path(args.data_dir)

    # 加载快照
    snapshot_path = data_dir / "snapshots" / f"{date_str}.json"
    if not snapshot_path.exists():
        print(f"快照不存在: {snapshot_path}")
        return 1

    with open(snapshot_path, "r", encoding="utf-8") as f:
        snapshot = json.load(f)
    skills = snapshot.get("skills", [])
    print(f"[Recommend] 加载 {len(skills)} 个技能")

    # 加载去重集合
    dedup_set = load_dedup_set(str(data_dir))
    print(f"[Recommend] 7 天去重: {len(dedup_set)} 个历史推荐")

    # 加载用户记忆
    user_keywords = load_user_memory_keywords()
    print(f"[Recommend] 记忆关键词: {len(user_keywords)} 个")

    # 生成推荐
    recommendations = recommend(skills, user_keywords, dedup_set)
    print(f"[Recommend] 生成 {len(recommendations)} 个推荐")

    # 开发者速览
    dev_summary = find_active_developers(skills)
    print(f"[Recommend] 活跃开发者: {len(dev_summary)} 位")

    # 深度评估（对最终推荐调用 evaluation + reports）
    if not args.skip_eval:
        print(f"[Recommend] 深度评估中...")
        for i, rec in enumerate(recommendations):
            slug = rec.get("slug", "")
            print(f"  [{i+1}/{len(recommendations)}] {slug[:30]}", end="", flush=True)

            eval_data = fetch_evaluation(slug)
            if eval_data:
                rec["evaluation"] = eval_data
                print(" eval OK", end="")
            else:
                print(" eval SKIP", end="")

            reports_data = fetch_reports(slug)
            if reports_data:
                rec["reports"] = reports_data
                print(" reports OK", end="")
            else:
                print(" reports SKIP", end="")

            print()
            time.sleep(0.5)

    # 保存
    rec_dir = data_dir / "recommended"
    rec_dir.mkdir(parents=True, exist_ok=True)

    rec_data = {
        "date": date_str,
        "version": "3.0",
        "total_scanned": len(skills),
        "dedup_count": len(dedup_set),
        "memory_keyword_count": len(user_keywords),
        "dimensions": ["trending_surge", "newcomers", "scene_match", "memory_collision", "china_first", "active_developer", "tencent_official"],
        "recommendations": [{k: v for k, v in r.items() if k not in ("_rankings",)} for r in recommendations]
    }

    rec_json = rec_dir / f"{date_str}.json"
    with open(rec_json, "w", encoding="utf-8") as f:
        json.dump(rec_data, f, ensure_ascii=False, indent=2)

    briefing = generate_briefing_md(recommendations, date_str, {
        "total_scanned": len(skills), "dedup_count": len(dedup_set),
        "memory_kw_count": len(user_keywords)
    }, dev_summary=dev_summary[:5])
    rec_md = rec_dir / f"{date_str}.md"
    with open(rec_md, "w", encoding="utf-8") as f:
        f.write(briefing)

    print(f"[Recommend] JSON: {rec_json}")
    print(f"[Recommend] MD: {rec_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
