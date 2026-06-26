#!/usr/bin/env python3
"""
Skill Net — Deep Dependency & Ecosystem Analyzer v3.0
Full-spectrum analysis with detailed impact analysis and enhanced visualization.
"""
import json, os, re, sys
from collections import defaultdict
from datetime import datetime

# Pre-compiled regex patterns for performance
RE_COMPILED = {
    "frontmatter_key": re.compile(r"^(\w+):\s*(.*)$"),
    "slug_mention": re.compile(r"(?:[`'\"]|/|[\b]){slug}(?:[`'\"]|/|[\b]|<)".replace("{slug}", r"([a-z][a-z0-9_-]{{4,30}})"), re.I),
    "backtick_slug": re.compile(r"`([a-z][a-z0-9_-]{{4,30})`"),
    "trigger": re.compile(r"\b(use when|trigger|activates|use this skill)\b", re.I),
    "trigger_section": re.compile(r"(?:trigger|when to use|use when|activates)[\s:]*([^\n]+(?:\n(?!\n)[^\n]+){{0,5}})", re.I),
    "protocol_style": re.compile(r"^#\s+/[a-z][a-z0-9_-]+\s*[-—]", re.M),
    "meta_block": re.compile(r"metadata:\s*\{{([^}}]+)\}"),
    "meta_kv": re.compile(r'"(\w+)":\s*"?([^"]+)"?'),
}

SKILLS_DIRS = [
    os.path.expanduser("~/.openclaw/workspace/skills"),
    os.path.expanduser("~/.openclaw/skills"),
]

# Functional categories for human-readable impact reports
CATEGORY_TAGS = {
    "engineering": ["engineering", "frontend", "backend", "devops", "security", "firmware", "technical-writer"],
    "marketing": ["marketing", "content", "seo", "social", "reddit", "twitter", "instagram", "tiktok", "bilibili", "xiaohongshu", "kuaishou", "baidu", "zhihu", "wechat-official"],
    "design": ["design", "ui", "ux", "brand", "visual", "image", "whimsy", "inclusive"],
    "testing": ["testing", "test", "benchmark", "evidence", "accessibility", "api"],
    "project-management": ["project", "jira", "studio", "experiment", "shepherd", "sprint", "product"],
    "support": ["support", "finance", "legal", "analytics", "executive-summary", "infrastructure"],
    "data": ["data", "analytics", "automation", "gupiao", "stock", "pdf", "excel"],
    "protocol": ["review", "qa", "careful", "cso", "office-hours"],
    "communication": ["weixin", "feishu", "whatsapp", "tts", "summarize", "whisper"],
    "personal": ["bazi", "productivity", "humanizer", "nuwa", "perspective", "ontology"],
    "meta": ["skill-factory", "skill-net", "skill-vetter", "find-skills", "proactive-agent", "self-improving"],
}

PROTOCOL_SKILLS = {"review", "qa", "careful", "cso", "office-hours", "summarize", "weather"}


def tag_skill(slug):
    """Return the functional category for a skill."""
    slug_lower = slug.lower()
    for cat, keywords in CATEGORY_TAGS.items():
        for kw in keywords:
            if kw in slug_lower:
                return cat
    if slug in PROTOCOL_SKILLS:
        return "protocol"
    return "general"


def parse_frontmatter(content):
    """Parse frontmatter from skill content.
    
    Returns (frontmatter_dict, body_str).
    frontmatter is a dict of key->value from YAML frontmatter.
    body is everything after the closing '---' delimiter.
    """
    frontmatter = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 2:
            for line in parts[1].split("\n"):
                m = RE_COMPILED["frontmatter_key"].match(line.strip())
                if m:
                    frontmatter[m.group(1)] = m.group(2).strip()
            body = parts[2] if len(parts) > 2 else ""
    return frontmatter, body


def scan_all_skills():
    skills = {}
    all_slugs = set()

    # First pass: collect all slugs
    for base_dir in SKILLS_DIRS:
        if not os.path.exists(base_dir):
            continue
        for entry in os.scandir(base_dir):
            if entry.is_dir():
                all_slugs.add(entry.name)

    # Second pass: analyze each skill
    for base_dir in SKILLS_DIRS:
        if not os.path.exists(base_dir):
            continue
        for entry in os.scandir(base_dir):
            if not entry.is_dir():
                continue
            slug = entry.name
            sk_path = os.path.join(entry.path, "SKILL.md")
            if not os.path.exists(sk_path):
                continue

            with open(sk_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()

            frontmatter, body = parse_frontmatter(content)

            # Extract ALL skill name mentions
            all_mentions = set()
            for other in all_slugs:
                if other == slug:
                    continue
                pat = re.compile(
                    r"(?:[`'\"]|/|[\b])" + re.escape(other) + r"(?:[`'\"]|/|[\b]|<)",
                    re.I
                )
                if pat.search(body):
                    all_mentions.add(other)

            # Also find backtick-quoted slugs
            for found in RE_COMPILED["backtick_slug"].findall(body):
                if found != slug and found in all_slugs:
                    all_mentions.add(found)

            # Detect triggers — check both body and frontmatter description
            desc = frontmatter.get("description", "")
            has_triggers = bool(RE_COMPILED["trigger"].search(body) or RE_COMPILED["trigger"].search(desc))
            trigger_section = RE_COMPILED["trigger_section"].search(body) or RE_COMPILED["trigger_section"].search(desc)
            trigger_text = trigger_section.group(1).strip()[:200] if trigger_section else ""

            # Protocol-style detection: starts with # /command or ## /command
            is_protocol = bool(RE_COMPILED["protocol_style"].search(body))

            # Metadata
            meta_block = {}
            meta_m = RE_COMPILED["meta_block"].search(content)
            if meta_m:
                for kv in RE_COMPILED["meta_kv"].findall(meta_m.group(1)):
                    meta_block[kv[0]] = kv[1]

            # ClawHub origin data
            origin_path = os.path.join(entry.path, ".clawhub", "origin.json")
            origin = {}
            if os.path.exists(origin_path):
                try:
                    with open(origin_path) as f:
                        origin = json.load(f)
                except: pass

            desc = frontmatter.get("description", "")

            skills[slug] = {
                "path": sk_path,
                "frontmatter": frontmatter,
                "mentions": all_mentions,
                "referenced_by": set(),
                "has_triggers": has_triggers,
                "is_protocol": is_protocol,
                "trigger_text": trigger_text,
                "meta_block": meta_block,
                "lines": content.count("\n"),
                "origin": origin,
                "category": tag_skill(slug),
                "is_role_based": _is_role_based(desc),
                "has_meaningful_desc": _has_meaningful_desc(desc, content.count("\n")),
            }

    # Resolve references
    for slug, data in skills.items():
        for mentioned in data["mentions"]:
            if mentioned in skills:
                skills[mentioned]["referenced_by"].add(slug)

    return skills


def classify_skills(skills):
    core, bridge, leaf, isolated = [], [], [], []
    for slug, data in skills.items():
        refs = len(data["mentions"])
        refd = len(data.get("referenced_by", set()))
        if refd >= 3:
            core.append((slug, data))
        elif refs > 0 and refd > 0:
            bridge.append((slug, data))
        elif refs > 0:
            leaf.append((slug, data))
        else:
            isolated.append((slug, data))
    return core, bridge, leaf, isolated


def _is_role_based(desc):
    """Role-based agent: description starts with 'You are' and has a role name."""
    stripped = desc.strip()
    return stripped.startswith("You are") and len(stripped) > 20


def _has_meaningful_desc(desc, body_lines):
    """Has substantive content beyond role definition."""
    if not desc or len(desc.strip()) < 15:
        return False
    # Penalize generic placeholder descriptions
    placeholder_phrases = ["to be written", "tbd", "todo", "under development",
                          "not yet implemented", "coming soon"]
    desc_lower = desc.lower()
    if any(p in desc_lower for p in placeholder_phrases):
        return False
    return True


def _has_identity(skill_data):
    """A skill has identity if it has any form of self-definition."""
    if skill_data.get("has_triggers"):
        return True
    if skill_data.get("is_protocol"):
        return True
    desc = skill_data.get("frontmatter", {}).get("description", "")
    if _is_role_based(desc):
        return True
    if _has_meaningful_desc(desc, skill_data.get("lines", 0)):
        return True
    return False


def detect_orphans(skills):
    """Detect skills with no trigger, protocol style, or meaningful identity."""
    return [(s, d["lines"], d["frontmatter"].get("name", s), d["category"])
            for s, d in skills.items()
            if not _has_identity(d)]


def ecosystem_health_score(skills):
    total = len(skills)
    if total == 0:
        return 0
    desc_not_empty = sum(1 for d in skills.values() if d["frontmatter"].get("description", "").strip())
    desc_substantive = sum(1 for d in skills.values()
                           if len(d["frontmatter"].get("description", "").strip()) >= 20)
    body_has_content = sum(1 for d in skills.values() if d.get("lines", 0) >= 20)
    has_identity = sum(1 for d in skills.values() if _has_identity(d))
    score = (
        (desc_not_empty / total) * 20 +
        (desc_substantive / total) * 25 +
        (body_has_content / total) * 15 +
        (has_identity / total) * 40
    )
    return round(score, 1)


def build_impact_report(skills, slug):
    """Build detailed impact report for deleting a specific skill."""
    data = skills.get(slug, {})
    dependents = sorted(data.get("referenced_by", set()))
    if not dependents:
        return None

    # Group dependents by category
    by_category = defaultdict(list)
    for dep in dependents:
        cat = skills[dep]["category"] if dep in skills else "general"
        by_category[cat].append(dep)

    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  🗑️  IMPACT REPORT: DELETE `{slug}`")
    lines.append(f"{'='*60}")
    lines.append(f"  Affects {len(dependents)} skill(s) across {len(by_category)} category(ies)")

    for cat, members in sorted(by_category.items(), key=lambda x: -len(x[1])):
        lines.append(f"\n  [{cat.upper()}] — {len(members)} skill(s)")
        for m in members:
            name = skills[m]["frontmatter"].get("name", m)
            protocol_style = "📋" if skills[m]["is_protocol"] else "🏷️"
            triggers = "✅" if skills[m]["has_triggers"] else "⚠️"
            lines.append(f"    {protocol_style} {triggers} `{m}` ({name})")

            # What specifically would break
            if slug in skills[m]["mentions"]:
                lines.append(f"        → `{m}` explicitly mentions `{slug}`")
            else:
                lines.append(f"        → `{m}` references this skill's protocol/command")

    lines.append(f"\n  {'─'*60}")
    lines.append(f"  TOTAL BLAST RADIUS: {len(dependents)} skill(s)")
    lines.append(f"  {'─'*60}")
    return "\n".join(lines)


def render_markdown_table(skills):
    """Render skills as a Markdown table sorted by impact."""
    core, bridge, leaf, isolated = classify_skills(skills)

    rows = []
    rows.append("# OpenClaw Skill Ecosystem — Markdown Tables\n")

    # Table 1: Core Hubs (sorted by dependents desc)
    rows.append("## 🔵 Core Hub Skills (referenced by 3+)\n")
    rows.append("| Skill | Name | Category | Referenced By | References | Protocol Style |")
    rows.append("|-------|------|----------|---------------|------------|----------------|")
    for slug, data in sorted(core, key=lambda x: -len(x[1].get("referenced_by", []))):
        name = data["frontmatter"].get("name", "")
        cat = data["category"]
        refd = len(data.get("referenced_by", []))
        refs = len(data["mentions"])
        protocol = "✅" if data["is_protocol"] else "—"
        rows.append(f"| `{slug}` | {name} | {cat} | **{refd}** | {refs} | {protocol} |")

    # Table 2: Bridges
    rows.append("\n## 🟡 Bridge Skills (both references and referenced)\n")
    rows.append("| Skill | Name | Category | References | Referenced By |")
    rows.append("|-------|------|----------|------------|---------------|")
    for slug, data in sorted(bridge, key=lambda x: -len(x[1]["mentions"])):
        name = data["frontmatter"].get("name", "")
        cat = data["category"]
        refs = len(data["mentions"])
        refd = len(data.get("referenced_by", []))
        rows.append(f"| `{slug}` | {name} | {cat} | {refs} | {refd} |")

    # Table 3: Top Leaf skills (most references)
    rows.append("\n## 🟢 Top Leaf Skills (most outgoing references)\n")
    rows.append("| Skill | Name | Category | References |")
    rows.append("|-------|------|----------|------------|")
    for slug, data in sorted(leaf, key=lambda x: -len(x[1]["mentions"]))[:15]:
        name = data["frontmatter"].get("name", "")
        cat = data["category"]
        refs = len(data["mentions"])
        rows.append(f"| `{slug}` | {name} | {cat} | {refs} |")

    # Table 4: Orphan skills by category
    orphans = detect_orphans(skills)
    by_cat = defaultdict(list)
    for s, lines_cnt, name, cat in orphans:
        by_cat[cat].append((s, lines_cnt, name))

    rows.append("\n## ⚠️ Orphan Skills (no trigger conditions, by category)\n")
    for cat in sorted(by_cat.keys(), key=lambda c: -len(by_cat[c])):
        members = by_cat[cat]
        rows.append(f"\n### [{cat.upper()}] — {len(members)} orphan(s)\n")
        rows.append("| Skill | Lines | Name |")
        rows.append("|-------|-------|------|")
        for s, lc, name in sorted(members, key=lambda x: -x[1])[:10]:
            rows.append(f"| `{s}` | {lc} | {name} |")

    # Table 5: Full impact analysis (delete X → breaks Y)
    rows.append("\n## 🗑️ Delete Impact Matrix\n")
    rows.append("| If You Delete | Breaks These Skills | Count |")
    rows.append("|---------------|---------------------|-------|")
    impacts = []
    for slug, data in skills.items():
        refd = list(data.get("referenced_by", []))
        if len(refd) >= 2:
            impacts.append((slug, refd, len(refd)))
    for slug, refd, count in sorted(impacts, key=lambda x: -x[2]):
        skill_names = ", ".join(f"`{r}`" for r in refd[:5])
        if count > 5:
            skill_names += f" +{count-5} more"
        rows.append(f"| `{slug}` | {skill_names} | **{count}** |")

    return "\n".join(rows)


def render_full_report(skills):
    core, bridge, leaf, isolated = classify_skills(skills)
    orphans = detect_orphans(skills)
    health = ecosystem_health_score(skills)

    lines = []
    lines.append("=" * 60)
    lines.append("  SKILL NET v3.0 — OpenClaw Ecosystem Analysis")
    lines.append("=" * 60)
    lines.append(f"  {len(skills)} skills scanned | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"  🌡️  Ecosystem Health Score: {health}/100")
    lines.append("=" * 60)

    total = len(skills)
    desc_not_empty = sum(1 for d in skills.values() if d["frontmatter"].get("description", "").strip())
    desc_substantive = sum(1 for d in skills.values()
                           if len(d["frontmatter"].get("description", "").strip()) >= 20)
    body_has_content = sum(1 for d in skills.values() if d.get("lines", 0) >= 20)
    has_identity = sum(1 for d in skills.values() if _has_identity(d))
    with_triggers = sum(1 for d in skills.values() if d["has_triggers"])  # keep for other uses
    with_meta = sum(1 for d in skills.values() if d.get("meta_block"))  # keep for other uses

    lines.append(f"\n  📊 Ecosystem Composition:")
    lines.append(f"     🔵 Core hubs:    {len(core)} skill(s)")
    lines.append(f"     🟡 Bridges:     {len(bridge)} skill(s)")
    lines.append(f"     🟢 Leaf:        {len(leaf)} skill(s)")
    lines.append(f"     ⚪ Isolated:    {len(isolated)} skill(s)")
    lines.append(f"     ⚠️  Orphans:     {len(orphans)} skill(s)")

    lines.append(f"\n  📊 Health Breakdown:")
    lines.append(f"     Description present:  {desc_not_empty}/{total} ({100*desc_not_empty//total}%)")
    lines.append(f"     Description quality: {desc_substantive}/{total} ({100*desc_substantive//total}%)")
    lines.append(f"     Body content:        {body_has_content}/{total} ({100*body_has_content//total}%)")
    lines.append(f"     Identity coverage:  {has_identity}/{total} ({100*has_identity//total}%)")

    # Core hubs
    lines.append(f"\n{'🔵 CORE HUB SKILLS (ref by 3+)':=^60}")
    for slug, data in sorted(core, key=lambda x: -len(x[1].get("referenced_by", []))):
        name = data["frontmatter"].get("name", slug)
        refd = len(data.get("referenced_by", []))
        cat = data["category"]
        protocol = "📋" if data["is_protocol"] else "🏷️"
        dependents = sorted(data["referenced_by"])
        lines.append(f"\n  {protocol} 🔵 `{slug}` ({name}) | {cat} | ← {refd}")
        if refd <= 10:
            lines.append(f"      → {', '.join(dependents)}")
        else:
            lines.append(f"      → {', '.join(dependents[:8])} +{refd-8} more")

    # Bridge skills
    lines.append(f"\n{'🟡 BRIDGE SKILLS':=^60}")
    for slug, data in sorted(bridge, key=lambda x: -len(x[1]["mentions"])):
        name = data["frontmatter"].get("name", slug)
        cat = data["category"]
        refs = len(data["mentions"])
        refd = len(data.get("referenced_by", []))
        lines.append(f"  🟡 `{slug}` ({name}) | → {refs} ← {refd} | {cat}")

    # Orphans
    lines.append(f"\n{'⚠️  ORPHAN SKILLS (SKILL.md without trigger conditions)':=^60}")
    lines.append(f"  Total: {len(orphans)} skills\n")
    by_cat = defaultdict(list)
    for s, lc, name, cat in orphans:
        by_cat[cat].append((s, lc, name))
    for cat in sorted(by_cat.keys(), key=lambda c: -len(by_cat[c])):
        members = by_cat[cat]
        extra = f" +{len(members)-5} more" if len(members) > 5 else ""
        lines.append(f"  [{cat.upper()}] {len(members)}: {', '.join(f'`{s}`' for s, _, _ in members[:5])}{extra}")

    # Full impact table
    lines.append(f"\n{'🗑️  DELETE IMPACT TABLE (2+ dependents)':=^60}")
    lines.append(f"  {'Skill':<35} {'Category':<15} {'Count':<6} {'Depends On It'}")
    lines.append(f"  {'─'*60}")
    impacts = [(s, d, sorted(d.get("referenced_by", [])), len(d.get("referenced_by", [])))
               for s, d in skills.items() if len(d.get("referenced_by", [])) >= 2]
    for slug, data, refd, count in sorted(impacts, key=lambda x: -x[3]):
        cat = data["category"]
        lines.append(f"  🗑️  `{slug}`")
        lines.append(f"     {cat:<15} {count:>4} skills: {', '.join(refd[:4])}{'+' if count > 4 else ''}")

    # ASCII map
    lines.append(f"\n{'📋 SKILL ECOSYSTEM MAP':=^60}")
    ranked = sorted(skills.items(), key=lambda x: len(x[1].get("referenced_by", set())), reverse=True)
    shown = 0
    for slug, data in ranked:
        if not data.get("referenced_by") and not data["mentions"]:
            continue
        if shown >= 15:
            break
        refd = len(data.get("referenced_by", set()))
        refs = len(data["mentions"])
        indent = "  " * shown
        if refd >= 3:
            lines.append(f"{indent}📦 {slug} ← {refd}")
        elif refd > 0:
            lines.append(f"{indent}🔗 {slug} → {refs} ← {refd}")
        elif refs > 0:
            lines.append(f"{indent}🍃 {slug} → {refs}")
        shown += 1

    lines.append("\n" + "=" * 60)
    lines.append("  LEGEND")
    lines.append("  🔵 Core = ref by 3+ (high blast radius) | 🟡 Bridge = in+out | 🟢 Leaf = out only | ⚪ Isolated = none")
    lines.append("  📋 = protocol-style skill | 🏷️ = standard trigger-style skill | ⚠️ = orphan (no triggers)")
    lines.append("=" * 60)

    return "\n".join(lines), health, orphans



# ── BILINGUAL LABELS ───────────────────────────────────────────────────────
L = {
    "skills_scanned":       ("skills scanned",               "个技能已扫描"),
    "health_score":         ("Ecosystem Health Score",       "生态健康分"),
    "composition":          ("Ecosystem Composition",         "生态构成"),
    "core_hubs":            ("Core Hub Skills",               "核心枢纽技能"),
    "bridges":              ("Bridge Skills",                "桥接技能"),
    "leaf_skills":          ("Leaf Skills",                   "叶节点技能"),
    "isolated_skills":      ("Isolated Skills",              "孤立技能"),
    "orphan_skills":        ("Orphan Skills",                "孤儿技能"),
    "delete_impact":        ("Delete Impact Analysis",       "删除影响分析"),
    "health_breakdown":     ("Health Breakdown",             "健康度明细"),
    "desc_present":         ("Description Present",          "Description存在"),
    "desc_quality":         ("Description Quality",          "Description质量"),
    "body_content":         ("Body Content",                  "Body内容"),
    "identity_cov":         ("Identity Coverage",             "身份覆盖"),
    "referenced_by":        ("referenced by",                "被引用"),
    "references":           ("references",                   "外联引用"),
    "affected":             ("affected skill(s)",             "受影响技能"),
    "no_triggers":          ("no trigger conditions",         "无触发条件"),
    "no_orphans":           ("No orphans found",             "无孤儿技能"),
    "no_impact":            ("No high-impact skills",        "无高频影响技能"),
    "delete":               ("DELETE",                       "删除"),
    "breaks":               ("breaks",                       "将影响"),
    "across":               ("across",                       "跨"),
    "categories":           ("categories",                   "个功能类别"),
    "legend":               ("LEGEND",                       "图例"),
    "ecosystem_map":        ("Skill Ecosystem Map",         "技能生态地图"),
    "health_note_en":       ("Health: content(60%) + identity(40%)",  ""),
    "health_note_zh":       ("", "健康分：触发词x30% + metadatax20% + 跨引用x20% + 内聚度x30%"),
    "orphan_note2_en":       ("Many use /protocol activation -- not broken, different design",         ""),
    "orphan_note2_zh":      ("", "许多孤儿使用/protocol激活风格 -- 非损坏，仅设计风格不同"),
}

def l(en_key):
    pair = L.get(en_key, (en_key, en_key))
    return pair[0] if lang == "EN" else pair[1]


# ── BILINGUAL REPORT RENDERER ───────────────────────────────────────────────
def le(en_key):  # returns (en, zh) tuple
    return L.get(en_key, (en_key, en_key))

def render_bilingual(skills, lang="EN"):
    def l(en_key):  # returns single string for current lang
        pair = L.get(en_key, (en_key, en_key))
        return pair[0] if lang == "EN" else pair[1]
    core, bridge, leaf, isolated = classify_skills(skills)
    orphans = detect_orphans(skills)
    health = ecosystem_health_score(skills)
    total = len(skills)

    lines = []
    W = 60
    title = "SKILL NET -- Ecosystem Analysis" if lang == "EN" else "SKILL NET -- 技能生态分析"
    lines.append("=" * W)
    lines.append("  " + title)
    lines.append("=" * W)
    lines.append("  " + str(total) + " " + l("skills_scanned") + " | " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    lines.append("  [Health] " + l("health_score") + ": " + str(health) + "/100")
    lines.append("=" * W)

    desc_not_empty = sum(1 for d in skills.values() if d["frontmatter"].get("description", "").strip())
    desc_substantive = sum(1 for d in skills.values()
                           if len(d["frontmatter"].get("description", "").strip()) >= 20)
    body_has_content = sum(1 for d in skills.values() if d.get("lines", 0) >= 20)
    has_identity = sum(1 for d in skills.values() if _has_identity(d))
    eco_nodes = sum(1 for d in skills.values() if d.get("referenced_by"))


    lines.append("")
    lines.append("  [Composition] " + l("composition") + ":")
    lines.append("     [Core] " + l("core_hubs") + ":    " + str(len(core)))
    lines.append("     [Bridge] " + l("bridges") + ":     " + str(len(bridge)))
    lines.append("     [Leaf] " + l("leaf_skills") + ":        " + str(len(leaf)))
    lines.append("     [Isolated] " + l("isolated_skills") + ":    " + str(len(isolated)))
    lines.append("     [Orphan] " + l("orphan_skills") + ":     " + str(len(orphans)))

    lines.append("")
    lines.append("  [Health] " + l("health_breakdown") + ":")
    lines.append("     " + l("desc_present") + ":  " + str(desc_not_empty) + "/" + str(total) + " (" + str(100*desc_not_empty//total) + "%)")
    lines.append("     " + l("desc_quality") + ":  " + str(desc_substantive) + "/" + str(total) + " (" + str(100*desc_substantive//total) + "%)")
    lines.append("     " + l("body_content") + ":   " + str(body_has_content) + "/" + str(total) + " (" + str(100*body_has_content//total) + "%)")
    lines.append("     " + l("identity_cov") + ":   " + str(has_identity) + "/" + str(total) + " (" + str(100*has_identity//total) + "%)")
    lines.append("     " + l("eco_nodes") + ":             " + str(eco_nodes) + "/" + str(total))

    if lang == "EN":
        lines.append("  * Health: content(60%) + identity(40%)")
    else:
        lines.append("  * 健康分：内容完整性(60%) + 身份覆盖(40%)")

    # Core hubs
    hub_title = "[Core] " + l("core_hubs") + " (ref by 3+)"
    lines.append("")
    lines.append(hub_title)
    lines.append("=" * W)
    if core:
        for slug, data in sorted(core, key=lambda x: -len(x[1].get("referenced_by", []))):
            name  = data["frontmatter"].get("name", slug)
            refd  = len(data.get("referenced_by", []))
            cat   = data["category"]
            proto = "[P]" if data["is_protocol"] else "[T]"
            deps  = sorted(data["referenced_by"])
            lines.append("")
            lines.append("  " + proto + " [Core] " + slug + " / " + name)
            lines.append("     " + cat + " | <- " + str(refd) + " " + l("referenced_by"))
            if refd <= 6:
                lines.append("     -> " + ", ".join(deps))
            else:
                lines.append("     -> " + ", ".join(deps[:6]) + " +" + str(refd-6) + " more")
    else:
        lines.append("  -- " + l("no_impact"))

    # Bridges
    bridge_title = "[Bridge] " + l("bridges")
    lines.append("")
    lines.append(bridge_title)
    lines.append("=" * W)
    for slug, data in sorted(bridge, key=lambda x: -len(x[1]["mentions"])):
        name  = data["frontmatter"].get("name", slug)
        cat   = data["category"]
        refs  = len(data["mentions"])
        refd  = len(data.get("referenced_by", []))
        lines.append("  [Bridge] " + slug + " / " + name + " | ->" + str(refs) + " <-" + str(refd) + " | " + cat)

    # Delete impact
    di_title = "[Delete Impact] " + l("delete_impact") + "  (X -> breaks Y)"
    lines.append("")
    lines.append(di_title)
    lines.append("=" * W)
    impacts = [(s, data, sorted(data.get("referenced_by", [])), len(data.get("referenced_by", [])))
               for s, data in skills.items() if len(data.get("referenced_by", [])) >= 2]
    if impacts:
        for slug, data, refd, count in sorted(impacts, key=lambda x: -x[3]):
            cat = data["category"]
            by_cat = defaultdict(list)
            for dep in refd:
                dep_cat = skills[dep]["category"] if dep in skills else "general"
                by_cat[dep_cat].append(dep)
            lines.append("")
            lines.append("  [X] DELETE " + slug + " / " + cat)
            lines.append("     " + l("affected") + ": " + str(count))
            for c, members in sorted(by_cat.items(), key=lambda x: -len(x[1])):
                lines.append("     [" + c.upper() + "] " + str(len(members)) + ": " + ", ".join(members[:5]) + ("+" if len(members)>5 else ""))
    else:
        lines.append("  -- " + l("no_impact"))

    # Orphans by category
    or_title = "[Orphan] " + l("orphan_skills") + "  (" + l("no_triggers") + ")"
    lines.append("")
    lines.append(or_title)
    lines.append("=" * W)
    if lang == "EN":
        lines.append("  * Many use /protocol activation -- not broken, different design")
    else:
        lines.append("  * 许多孤儿使用/protocol激活风格 -- 非损坏，仅设计风格不同")
    lines.append("")
    by_cat = defaultdict(list)
    for s, lc, name, cat in orphans:
        by_cat[cat].append(s)
    for cat in sorted(by_cat.keys(), key=lambda c: -len(by_cat[c])):
        members = by_cat[cat]
        names_short = ", ".join(s for s in members[:5])
        extra = " +" + str(len(members)-5) + " more" if len(members) > 5 else ""
        lines.append("  [" + cat.upper() + "] " + str(len(members)) + ": " + names_short + extra)

    # Ecosystem map
    map_title = "[Ecosystem Map] " + l("ecosystem_map")
    lines.append("")
    lines.append(map_title)
    lines.append("=" * W)
    ranked = sorted(skills.items(), key=lambda x: len(x[1].get("referenced_by", set())), reverse=True)
    shown = 0
    for slug, data in ranked:
        if shown >= 12:
            break
        refd = len(data.get("referenced_by", set()))
        refs = len(data["mentions"])
        if refd == 0 and refs == 0:
            continue
        if refd >= 3:
            lines.append("  [Hub] " + slug + " <- " + str(refd))
        elif refd > 0:
            lines.append("  [Bridge] " + slug + " ->" + str(refs) + " <-" + str(refd))
        else:
            lines.append("  [Leaf] " + slug + " ->" + str(refs))
        shown += 1

    # Legend
    leg_title = "[Legend] " + l("legend")
    lines.append("")
    lines.append(leg_title)
    lines.append("=" * W)
    if lang == "EN":
        lines.append("  [Core] = ref by 3+ (high blast radius)")
        lines.append("  [Bridge] = refs others + is referenced")
        lines.append("  [Leaf] = refs others, nothing refs it")
        lines.append("  [Isolated] = self-contained, no dependencies")
        lines.append("  [Orphan] = has SKILL.md, no triggers detected")
        lines.append("  [P] = protocol-style (/command activation)")
        lines.append("  [T] = trigger-style (use when phrases)")
    else:
        lines.append("  [核心] = 被3个以上技能引用（高爆炸半径）")
        lines.append("  [桥接] = 既引用他人也被他人引用")
        lines.append("  [叶节点] = 引用他人但无人引用它")
        lines.append("  [孤立] = 完全自洽，无依赖关系")
        lines.append("  [孤儿] = 有SKILL.md但未检测到触发词")
        lines.append("  [协议型] = 使用 /command 激活风格")
        lines.append("  [触发词型] = 使用 use when 短语激活")

    lines.append("=" * W)
    return "\n".join(lines)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Skill Net — Ecosystem Analyzer")
    parser.add_argument("--lang", choices=["EN", "ZH", "BOTH"], default="BOTH",
                        help="Language: EN, ZH, or BOTH (default)")
    parser.add_argument("--impact", type=str, default=None,
                        help="Show detailed impact for a specific skill")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    skills = scan_all_skills()

    if args.json:
        print(json.dumps({k: {**v, 'referenced_by': list(v.get('referenced_by', set())), 'mentions': list(v['mentions'])} for k, v in skills.items()}, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.impact:
        report = build_impact_report(skills, args.impact)
        if report:
            print(report)
        else:
            print(f"No impact data for `{args.impact}` (0 or 1 dependent)")
        sys.exit(0)

    if args.lang in ("ZH", "BOTH"):
        print(render_bilingual(skills, "ZH"))
    if args.lang in ("EN", "BOTH"):
        if args.lang == "BOTH":
            print("\n" + "=" * 60 + "\n")
        print(render_bilingual(skills, "EN"))

    # Save
    output_dir = os.path.expanduser("~/.openclaw/workspace/skills/skill-net/data")
    os.makedirs(output_dir, exist_ok=True)


    serializable = {k: {"mentions": list(v["mentions"]), "referenced_by": list(v.get("referenced_by", set())),
                    "has_triggers": v["has_triggers"], "is_protocol": v["is_protocol"],
                    "trigger_text": v["trigger_text"], "meta_block": v["meta_block"],
                    "lines": v["lines"], "frontmatter": v["frontmatter"],
                    "category": v["category"], "health_score": ecosystem_health_score(skills)}
                   for k, v in skills.items()}

    with open(os.path.join(output_dir, "ecosystem.json"), "w") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)

    # Markdown tables
    md_table = render_markdown_table(skills)
    with open(os.path.join(output_dir, "report.md"), "w") as f:
        f.write(md_table)

    orphans = detect_orphans(skills)
    print(f"\n💾 ecosystem.json + report.md saved")
    print(f"🌡️  Health: {ecosystem_health_score(skills)}/100 | ⚠️  Orphans: {len(orphans)}")
