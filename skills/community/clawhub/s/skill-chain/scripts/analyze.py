#!/usr/bin/env python3
"""
SkillChain analyze: supply chain analysis on the graph built by ingest.py.

Usage:
    python3 scripts/analyze.py stats
    python3 scripts/analyze.py categories
    python3 scripts/analyze.py top [--by stars|downloads|installs] [--limit N]
    python3 scripts/analyze.py profile --skill <slug>
    python3 scripts/analyze.py supply-chain --skill <slug>
    python3 scripts/analyze.py packages [--top N]
    python3 scripts/analyze.py find-users --package <name>
    python3 scripts/analyze.py report [--out <file>]
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Graph loading (mirrors ingest.py, no duplication of business logic)
# ---------------------------------------------------------------------------

SKILL_CHAIN_ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = str(SKILL_CHAIN_ROOT / "memory" / "skillchain" / "graph.jsonl")

_ONTOLOGY_SCRIPT = Path(__file__).resolve().parent.parent.parent / "ontology" / "scripts" / "ontology.py"
if _ONTOLOGY_SCRIPT.exists():
    sys.path.insert(0, str(_ONTOLOGY_SCRIPT.parent))

try:
    from ontology import load_graph
    _load = load_graph
except ImportError:
    def _load(path: str) -> tuple[dict, list]:  # type: ignore[misc]
        entities: dict = {}
        relations: list = []
        p = Path(path)
        if not p.exists():
            return entities, relations
        with open(p) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                op = rec.get("op")
                if op == "create":
                    e = rec["entity"]
                    entities[e["id"]] = e
                elif op == "update":
                    eid = rec["id"]
                    if eid in entities:
                        entities[eid]["properties"].update(rec.get("properties", {}))
                elif op == "delete":
                    entities.pop(rec["id"], None)
                elif op == "relate":
                    relations.append({
                        "from": rec["from"], "rel": rec["rel"],
                        "to": rec["to"], "properties": rec.get("properties", {}),
                    })
        return entities, relations


# ---------------------------------------------------------------------------
# Graph helpers
# ---------------------------------------------------------------------------

def load() -> tuple[dict, list]:
    entities, relations = _load(GRAPH_PATH)
    if not entities:
        print("Graph is empty. Run: python3 scripts/ingest.py scan")
        sys.exit(1)
    return entities, relations


def by_type(entities: dict, t: str) -> list[dict]:
    return [e for e in entities.values() if e["type"] == t]


def outgoing(relations: list, from_id: str, rel: str | None = None) -> list[dict]:
    return [r for r in relations
            if r["from"] == from_id and (rel is None or r["rel"] == rel)]


def incoming(relations: list, to_id: str, rel: str | None = None) -> list[dict]:
    return [r for r in relations
            if r["to"] == to_id and (rel is None or r["rel"] == rel)]


def entity_by_slug(entities: dict, slug: str) -> dict | None:
    for e in entities.values():
        if e["type"] == "Skill":
            p = e["properties"]
            if p.get("slug") == slug or p.get("name") == slug:
                return e
    return None


def entity_name(e: dict) -> str:
    p = e["properties"]
    return p.get("slug") or p.get("name", e["id"])


# ---------------------------------------------------------------------------
# Supply chain traversal
# ---------------------------------------------------------------------------

def supply_chain_tree(skill_id: str, entities: dict, relations: list,
                      depth: int = 0, visited: set | None = None) -> list[str]:
    """Return lines of a supply-chain tree rooted at skill_id."""
    if visited is None:
        visited = set()
    if skill_id in visited or depth > 6:
        return []
    visited.add(skill_id)

    lines: list[str] = []
    indent = "  " * depth

    # Invocation channel (allowed-tools)
    for r in outgoing(relations, skill_id, "invoked_via"):
        tool = entities.get(r["to"])
        if not tool:
            continue
        tname   = tool["properties"].get("name", r["to"])
        pattern = r["properties"].get("pattern", "*")
        lines.append(f"{indent}├─ [invoked_via] {tname}  (pattern: {pattern})")

    # Runtime binary requirements (metadata.requires.bins)
    for r in outgoing(relations, skill_id, "requires_tool"):
        tool = entities.get(r["to"])
        if not tool:
            continue
        tname = tool["properties"].get("name", r["to"])
        tkind = tool["properties"].get("kind", "")
        lines.append(f"{indent}├─ [requires_bin:{tkind}] {tname}")

    # Detected tool usage (from SKILL.md text heuristics)
    for r in outgoing(relations, skill_id, "uses_tool"):
        tool = entities.get(r["to"])
        if not tool:
            continue
        tname = tool["properties"].get("name", r["to"])
        tkind = tool["properties"].get("kind", "")
        lines.append(f"{indent}├─ [tool:{tkind}] {tname}")
        for r2 in outgoing(relations, r["to"], "backed_by_package"):
            pkg = entities.get(r2["to"])
            if pkg:
                pname = pkg["properties"].get("name", r2["to"])
                peco  = pkg["properties"].get("ecosystem", "")
                lines.append(f"{indent}│    └─ [{peco}] {pname}")

    # Direct package dependencies
    for r in outgoing(relations, skill_id, "requires_package"):
        pkg = entities.get(r["to"])
        if not pkg:
            continue
        pname = pkg["properties"].get("name", r["to"])
        peco  = pkg["properties"].get("ecosystem", "")
        src   = pkg["properties"].get("source", "")
        src_tag = f"  ← {src}" if src and not src.startswith("import:") else ""
        lines.append(f"{indent}├─ [pkg:{peco}] {pname}{src_tag}")

    # Skill dependencies (recursive)
    for r in outgoing(relations, skill_id, "depends_on_skill"):
        dep = entities.get(r["to"])
        if not dep:
            continue
        dname = entity_name(dep)
        lines.append(f"{indent}├─ [skill] {dname}")
        lines.extend(supply_chain_tree(r["to"], entities, relations, depth + 1, visited))

    return lines


def detect_cycles(entities: dict, relations: list) -> list[list[str]]:
    """DFS cycle detection on depends_on_skill relation."""
    graph: dict[str, list[str]] = defaultdict(list)
    for r in relations:
        if r["rel"] == "depends_on_skill":
            graph[r["from"]].append(r["to"])

    visited: set[str] = set()
    stack: list[str] = []
    cycles: list[list[str]] = []

    def dfs(node: str) -> bool:
        visited.add(node)
        stack.append(node)
        for nxt in graph.get(node, []):
            if nxt in stack:
                cycle_start = stack.index(nxt)
                cycles.append(stack[cycle_start:] + [nxt])
                return True
            if nxt not in visited:
                dfs(nxt)
        stack.pop()
        return False

    for node in list(graph.keys()):
        if node not in visited:
            dfs(node)
    return cycles


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_stats(entities: dict, relations: list) -> None:
    skills  = by_type(entities, "Skill")
    cats    = by_type(entities, "SkillCategory")
    tools   = by_type(entities, "Tool")
    pkgs    = by_type(entities, "SoftwarePackage")

    enriched = [s for s in skills if s["properties"].get("stars") is not None]

    print("=== SkillChain Ecosystem Stats ===\n")
    print(f"  Skills        : {len(skills)}")
    print(f"  Categories    : {len(cats)}")
    print(f"  Tools         : {len(tools)}")
    print(f"  Packages      : {len(pkgs)}")
    print(f"  Relations     : {len(relations)}")
    print(f"  Online-enriched: {len(enriched)}/{len(skills)} skills")

    if enriched:
        total_stars = sum(s["properties"].get("stars", 0) or 0 for s in enriched)
        total_dl    = sum(s["properties"].get("downloads", 0) or 0 for s in enriched)
        print(f"\n  Total stars (enriched subset)    : {total_stars:,}")
        print(f"  Total downloads (enriched subset): {total_dl:,}")

    # Sources
    sources = Counter(s["properties"].get("source", "unknown") for s in skills)
    print("\n  By source:")
    for src, n in sources.most_common():
        print(f"    {src:<15} {n}")

    # Moderation
    mods = Counter(s["properties"].get("moderation", "unreviewed") for s in skills
                   if s["properties"].get("moderation"))
    if mods:
        print("\n  Moderation verdicts:")
        for verdict, n in mods.most_common():
            flag = " ⚠️ " if verdict in ("suspicious", "blocked") else ""
            print(f"    {verdict:<15}{flag} {n}")

    # Cycles
    cycles = detect_cycles(entities, relations)
    if cycles:
        print(f"\n  ⚠️  Circular skill dependencies detected: {len(cycles)}")
    else:
        print("\n  ✓ No circular skill dependencies.")


def cmd_categories(entities: dict, relations: list) -> None:
    skills = {e["id"]: e for e in by_type(entities, "Skill")}
    cats   = {e["id"]: e for e in by_type(entities, "SkillCategory")}

    cat_skills: dict[str, list[str]] = defaultdict(list)
    for r in relations:
        if r["rel"] == "belongs_to_category":
            sid, cid = r["from"], r["to"]
            if sid in skills and cid in cats:
                cat_skills[cid].append(
                    skills[sid]["properties"].get("slug") or
                    skills[sid]["properties"].get("name", sid)
                )

    print("=== Skill Categories ===\n")
    if not cat_skills:
        print("  No category data. Run `ingest scan` first.")
        return

    for cid, slug_list in sorted(cat_skills.items(), key=lambda x: -len(x[1])):
        cat_name = cats[cid]["properties"].get("name", cid)
        bar = "█" * len(slug_list)
        print(f"  {cat_name:<22} {bar} {len(slug_list)}")
        for slug in sorted(slug_list)[:6]:
            print(f"    · {slug}")
        if len(slug_list) > 6:
            print(f"    … and {len(slug_list)-6} more")
        print()


def cmd_top(entities: dict, relations: list, by: str, limit: int) -> None:
    skills = by_type(entities, "Skill")
    enriched = [s for s in skills if s["properties"].get(by) is not None]

    if not enriched:
        print(f"No '{by}' data. Run `ingest enrich` to pull online metadata.")
        return

    ranked = sorted(enriched, key=lambda s: s["properties"].get(by, 0) or 0, reverse=True)
    print(f"=== Top {limit} Skills by {by} ===\n")
    for i, s in enumerate(ranked[:limit], 1):
        p = s["properties"]
        slug   = p.get("slug") or p.get("name", s["id"])
        val    = p.get(by, 0)
        mod    = p.get("moderation", "")
        flag   = " ⚠️ " if mod in ("suspicious", "blocked") else ""
        stars  = p.get("stars", "")
        dl     = p.get("downloads", "")
        extra  = f"  ★{stars} ↓{dl}" if by != "stars" else f"  ↓{dl}"
        print(f"  {i:>3}. {slug:<35} {by}={val:>8,}{flag}{extra}")


def cmd_profile(entities: dict, relations: list, slug: str) -> None:
    skill = entity_by_slug(entities, slug)
    if not skill:
        print(f"Skill '{slug}' not found. Check with: python3 scripts/analyze.py stats")
        return

    p = skill["properties"]
    sid = skill["id"]
    print(f"=== Skill Profile: {p.get('slug') or p.get('name')} ===\n")
    for field in ("description", "version", "license", "source",
                  "stars", "downloads", "installs_current",
                  "owner_handle", "moderation", "local_path", "last_scanned"):
        val = p.get(field)
        if val is not None and val != "":
            print(f"  {field:<20} {val}")

    # Categories
    cat_ids = [r["to"] for r in outgoing(relations, sid, "belongs_to_category")]
    cats = [entities[cid]["properties"].get("name", cid)
            for cid in cat_ids if cid in entities]
    if cats:
        print(f"\n  Categories: {', '.join(cats)}")

    # Tools
    tool_rels = outgoing(relations, sid, "uses_tool")
    if tool_rels:
        print("\n  Tools used:")
        for r in tool_rels:
            t = entities.get(r["to"])
            if t:
                print(f"    [{t['properties'].get('kind','')}] {t['properties'].get('name','')}")

    # Packages
    pkg_rels = outgoing(relations, sid, "requires_package")
    if pkg_rels:
        print("\n  Package dependencies:")
        for r in pkg_rels:
            pkg = entities.get(r["to"])
            if pkg:
                eco  = pkg["properties"].get("ecosystem", "")
                name = pkg["properties"].get("name", "")
                spec = pkg["properties"].get("spec", "")
                print(f"    [{eco}] {spec or name}")

    # Skill deps
    dep_rels = outgoing(relations, sid, "depends_on_skill")
    if dep_rels:
        print("\n  Depends on skills:")
        for r in dep_rels:
            dep = entities.get(r["to"])
            if dep:
                print(f"    {entity_name(dep)}")

    # Reverse: which skills depend on this?
    rev_rels = incoming(relations, sid, "depends_on_skill")
    if rev_rels:
        print("\n  Used by skills:")
        for r in rev_rels:
            src = entities.get(r["from"])
            if src:
                print(f"    {entity_name(src)}")


def cmd_supply_chain(entities: dict, relations: list, slug: str) -> None:
    skill = entity_by_slug(entities, slug)
    if not skill:
        print(f"Skill '{slug}' not found.")
        return
    print(f"=== Supply Chain: {entity_name(skill)} ===\n")
    lines = supply_chain_tree(skill["id"], entities, relations)
    if lines:
        for line in lines:
            print(" ", line)
    else:
        print("  No tool, package, or skill dependencies recorded.")
        print("  Tip: check if requirements.txt or SKILL.md tool references exist.")


def cmd_packages(entities: dict, relations: list, top: int) -> None:
    pkgs   = {e["id"]: e for e in by_type(entities, "SoftwarePackage")}
    skills = {e["id"]: e for e in by_type(entities, "Skill")}

    # Count how many skills require each package (direct + via tool)
    pkg_users: dict[str, set[str]] = defaultdict(set)
    for r in relations:
        if r["rel"] == "requires_package" and r["from"] in skills and r["to"] in pkgs:
            pkg_users[r["to"]].add(r["from"])
        if r["rel"] == "backed_by_package" and r["to"] in pkgs:
            # find which skills use the tool
            tool_id = r["from"]
            for r2 in incoming(relations, tool_id, "uses_tool"):
                if r2["from"] in skills:
                    pkg_users[r["to"]].add(r2["from"])

    ranked = sorted(pkgs.items(), key=lambda x: -len(pkg_users.get(x[0], set())))
    print(f"=== Top {top} Packages by Skill Coverage ===\n")
    for pid, pkg in ranked[:top]:
        p = pkg["properties"]
        user_count = len(pkg_users.get(pid, set()))
        eco  = p.get("ecosystem", "")
        name = p.get("name", pid)
        bar  = "█" * min(user_count, 20)
        print(f"  [{eco:<5}] {name:<30} {bar} {user_count} skill(s)")


def cmd_find_users(entities: dict, relations: list, pkg_name: str) -> None:
    pkgs   = {e["id"]: e for e in by_type(entities, "SoftwarePackage")}
    skills = {e["id"]: e for e in by_type(entities, "Skill")}

    target_ids = {pid for pid, p in pkgs.items()
                  if p["properties"].get("name", "").lower() == pkg_name.lower()}
    if not target_ids:
        print(f"Package '{pkg_name}' not found in graph.")
        return

    users: set[str] = set()
    for r in relations:
        if r["rel"] == "requires_package" and r["to"] in target_ids:
            users.add(r["from"])
        if r["rel"] == "backed_by_package" and r["to"] in target_ids:
            tool_id = r["from"]
            for r2 in incoming(relations, tool_id, "uses_tool"):
                users.add(r2["from"])

    print(f"=== Skills using '{pkg_name}' ===\n")
    if not users:
        print("  None found.")
        return
    for sid in users:
        skill = skills.get(sid)
        if skill:
            print(f"  · {entity_name(skill)}")


def _skill_health_score(skill: dict, entities: dict, relations: list) -> tuple[int, list[str]]:
    """Score a skill 0-100 on completeness. Returns (score, list_of_issues)."""
    p = skill["properties"]
    sid = skill["id"]
    score = 0
    issues: list[str] = []

    # Description (20pts)
    desc = (p.get("description") or "").strip()
    if len(desc) >= 40:
        score += 20
    elif len(desc) > 0:
        score += 8
        issues.append("description too short (<40 chars)")
    else:
        issues.append("no description")

    # Non-uncategorized category (15pts)
    cat_rels = outgoing(relations, sid, "belongs_to_category")
    cat_names = [entities[r["to"]]["properties"].get("name", "") for r in cat_rels
                 if r["to"] in entities]
    if cat_names and any(c != "uncategorized" for c in cat_names):
        score += 15
    else:
        issues.append("uncategorized (no meaningful category)")

    # Version (10pts)
    if (p.get("version") or "").strip():
        score += 10
    else:
        issues.append("no version")

    # License (10pts)
    if (p.get("license") or "").strip():
        score += 10
    else:
        issues.append("no license")

    # Dependency declaration: packages OR bins OR allowed-tools (20pts)
    has_pkg  = bool(outgoing(relations, sid, "requires_package"))
    has_bin  = bool(outgoing(relations, sid, "requires_tool"))
    has_tool = bool(outgoing(relations, sid, "invoked_via")) or bool(outgoing(relations, sid, "uses_tool"))
    if has_pkg or has_bin or has_tool:
        score += 20
    else:
        issues.append("no declared dependencies (no packages, bins, or allowed-tools)")

    # read_when triggers (15pts)
    if p.get("read_when_count", 0) > 0:
        score += 15
    else:
        # fallback: check if description has trigger-like keywords
        trigger_words = ["trigger", "when", "use when", "use this", "read_when"]
        if any(kw in desc.lower() for kw in trigger_words):
            score += 8
        else:
            issues.append("no read_when / trigger conditions declared")

    # From clawhub / has meta (10pts)
    if p.get("source") == "clawhub" or p.get("stars") is not None:
        score += 10

    return min(score, 100), issues


def cmd_health(entities: dict, relations: list) -> None:
    """Print a completeness health report for every skill."""
    skills = sorted(by_type(entities, "Skill"),
                    key=lambda s: s["properties"].get("slug") or s["properties"].get("name", ""))
    print("=== Skill Health Report ===\n")
    print(f"  {'Skill':<30} {'Score':>5}  Issues")
    print(f"  {'-'*30} {'-'*5}  {'─'*40}")

    total = 0
    for skill in skills:
        score, issues = _skill_health_score(skill, entities, relations)
        total += score
        slug = skill["properties"].get("slug") or skill["properties"].get("name", skill["id"])
        dots = "●" * (score // 20) + "○" * (5 - score // 20)
        issue_str = "; ".join(issues) if issues else "✓ complete"
        print(f"  {slug:<30} {dots} {score:>3}  {issue_str}")

    avg = total // len(skills) if skills else 0
    print(f"\n  Average score: {avg}/100  ({len(skills)} skills)")
    low = [s for s in skills if _skill_health_score(s, entities, relations)[0] < 50]
    if low:
        print(f"\n  ⚠️  {len(low)} skill(s) score below 50 — consider improving:")
        for s in low:
            print(f"     · {s['properties'].get('slug') or s['properties'].get('name','?')}")


def _detect_overlaps(entities: dict, relations: list) -> list[tuple[str, str, str, float]]:
    """Find skill pairs that likely overlap or complement each other.

    Returns list of (slug_a, slug_b, reason, confidence 0-1).
    """
    skills = by_type(entities, "Skill")

    # Build index: skill_id → {cats, pkgs, tools, keywords}
    cat_map: dict[str, set[str]] = defaultdict(set)
    pkg_map: dict[str, set[str]] = defaultdict(set)
    tool_map: dict[str, set[str]] = defaultdict(set)
    for r in relations:
        if r["rel"] == "belongs_to_category":
            cat_map[r["from"]].add(r["to"])
        elif r["rel"] in ("requires_package", ):
            pkg_map[r["from"]].add(r["to"])
        elif r["rel"] in ("uses_tool", "requires_tool", "invoked_via"):
            tool_map[r["from"]].add(r["to"])

    # Keyword extraction from description
    def _keywords(skill: dict) -> set[str]:
        desc = (skill["properties"].get("description") or "").lower()
        stop = {"a","the","an","and","or","for","to","of","in","on","with",
                "that","this","when","use","used","using","which","from",
                "can","is","are","be","it","its","as","by","at","you","your",
                "will","how","what","also","any","all","each","not","no","but"}
        words = re.findall(r"[a-z]{3,}", desc)
        return {w for w in words if w not in stop}

    results: list[tuple[str, str, str, float]] = []
    checked: set[frozenset] = set()

    for i, s1 in enumerate(skills):
        for s2 in skills[i+1:]:
            pair = frozenset([s1["id"], s2["id"]])
            if pair in checked:
                continue
            checked.add(pair)

            slug1 = s1["properties"].get("slug") or s1["properties"].get("name", "?")
            slug2 = s2["properties"].get("slug") or s2["properties"].get("name", "?")

            reasons: list[str] = []
            conf = 0.0

            # Shared categories
            shared_cats = cat_map[s1["id"]] & cat_map[s2["id"]]
            if len(shared_cats) >= 2:
                cnames = [entities[c]["properties"].get("name","") for c in shared_cats if c in entities]
                reasons.append(f"share {len(shared_cats)} categories: {', '.join(cnames[:3])}")
                conf += 0.3 * min(len(shared_cats) / 3, 1.0)

            # Shared packages (strong overlap signal)
            shared_pkgs = pkg_map[s1["id"]] & pkg_map[s2["id"]]
            if shared_pkgs:
                pnames = [entities[p]["properties"].get("name","") for p in shared_pkgs if p in entities]
                reasons.append(f"share package(s): {', '.join(pnames[:3])}")
                conf += 0.4 * min(len(shared_pkgs) / 2, 1.0)

            # Shared tools
            shared_tools = tool_map[s1["id"]] & tool_map[s2["id"]]
            if shared_tools:
                tnames = [entities[t]["properties"].get("name","") for t in shared_tools if t in entities]
                reasons.append(f"share tool(s): {', '.join(tnames[:3])}")
                conf += 0.2 * min(len(shared_tools) / 2, 1.0)

            # Keyword overlap in descriptions
            kw1 = _keywords(s1)
            kw2 = _keywords(s2)
            if kw1 and kw2:
                overlap = kw1 & kw2
                jaccard = len(overlap) / len(kw1 | kw2)
                if jaccard >= 0.30:
                    reasons.append(f"description keywords overlap {jaccard:.0%}")
                    conf += jaccard * 0.3

            if conf >= 0.35 and reasons:
                results.append((slug1, slug2, "; ".join(reasons), min(conf, 1.0)))

    results.sort(key=lambda x: -x[3])
    return results


def cmd_overlaps(entities: dict, relations: list) -> None:
    """Detect skills that likely overlap in function or share significant dependencies."""
    pairs = _detect_overlaps(entities, relations)
    print("=== Skill Overlap / Complement Analysis ===\n")
    if not pairs:
        print("  No significant overlaps detected.")
        return
    print(f"  {'Skill A':<25} {'Skill B':<25} {'Conf':>5}  Reason")
    print(f"  {'-'*25} {'-'*25} {'-'*5}  {'─'*40}")
    for slug1, slug2, reason, conf in pairs[:20]:
        bar = "▓" * round(conf * 5)
        print(f"  {slug1:<25} {slug2:<25} {bar:<5}  {reason}")


def _generate_insights(entities: dict, relations: list) -> list[str]:
    """Generate human-readable insight bullets for the report."""
    insights: list[str] = []
    skills  = by_type(entities, "Skill")
    pkgs    = {e["id"]: e for e in by_type(entities, "SoftwarePackage")}

    # 1. Most shared package (single-point dependency risk)
    pkg_users: dict[str, set[str]] = defaultdict(set)
    for r in relations:
        if r["rel"] == "requires_package" and r["to"] in pkgs:
            pkg_users[r["to"]].add(r["from"])
    if pkg_users:
        top_pid = max(pkg_users, key=lambda p: len(pkg_users[p]))
        top_n   = len(pkg_users[top_pid])
        top_pkg = pkgs[top_pid]["properties"].get("name", top_pid)
        if top_n >= 2:
            insights.append(
                f"**Single-point dependency risk**: `{top_pkg}` is used by {top_n} skills "
                f"— upgrading or replacing it will have broad impact."
            )

    # 2. Category gaps
    all_cats = {e["properties"].get("name","") for e in by_type(entities, "SkillCategory")}
    expected = {"database", "cloud-infra", "testing", "monitoring", "security"}
    missing  = expected - all_cats
    if missing:
        insights.append(
            f"**Category gaps**: No skills found for: {', '.join(sorted(missing))}. "
            f"These areas may be under-served in your ecosystem."
        )

    # 3. Low-health skills
    low = [s for s in skills if _skill_health_score(s, entities, relations)[0] < 50]
    if low:
        slugs = ", ".join(
            s["properties"].get("slug") or s["properties"].get("name","?") for s in low[:5]
        )
        insights.append(
            f"**Low-completeness skills** ({len(low)} skill(s) score <50): {slugs}. "
            f"Run `analyze health` for detailed breakdown."
        )

    # 4. Uncategorized skills
    skill_ids = {e["id"] for e in skills}
    cat_ids   = {e["id"] for e in by_type(entities, "SkillCategory")}
    uncat = None
    for e in by_type(entities, "SkillCategory"):
        if e["properties"].get("name") == "uncategorized":
            uncat = e["id"]
            break
    if uncat:
        uncat_skills = [r["from"] for r in relations
                        if r["rel"] == "belongs_to_category" and r["to"] == uncat
                        and r["from"] in skill_ids]
        if uncat_skills:
            names = [entities[sid]["properties"].get("slug") or
                     entities[sid]["properties"].get("name","?")
                     for sid in uncat_skills]
            insights.append(
                f"**Uncategorized skills**: {', '.join(names)} — add a description "
                f"or `read_when` field so they can be auto-categorized."
            )

    # 5. Skills with CLI invocation channel (security note)
    cli_skills = []
    for r in relations:
        if r["rel"] == "invoked_via" and r["from"] in skill_ids:
            tool = entities.get(r["to"])
            if tool and tool["properties"].get("kind") == "shell":
                slug = entities[r["from"]]["properties"].get("slug") or \
                       entities[r["from"]]["properties"].get("name","?")
                cli_skills.append(slug)
    if cli_skills:
        insights.append(
            f"**CLI-invoked skills** ({len(cli_skills)}): {', '.join(cli_skills[:5])} — "
            f"these call external binaries via shell. Verify trust level before use."
        )

    # 6. Overlapping skills
    pairs = _detect_overlaps(entities, relations)
    if pairs:
        top = pairs[0]
        insights.append(
            f"**Potential overlap**: `{top[0]}` and `{top[1]}` share significant "
            f"functionality ({top[2]}). Consider clarifying their division of responsibility."
        )

    # 7. No deps skills (might be doc-only, might be incomplete)
    no_deps = []
    for s in skills:
        sid = s["id"]
        has_any = (outgoing(relations, sid, "requires_package") or
                   outgoing(relations, sid, "requires_tool") or
                   outgoing(relations, sid, "invoked_via") or
                   outgoing(relations, sid, "uses_tool"))
        if not has_any:
            no_deps.append(s["properties"].get("slug") or s["properties"].get("name","?"))
    if no_deps:
        insights.append(
            f"**No dependency info** for {len(no_deps)} skill(s): {', '.join(no_deps[:5])}. "
            f"Add `requirements.txt`, `package.json`, or `allowed-tools` if applicable."
        )

    return insights


def cmd_report(entities: dict, relations: list, out_path: str | None) -> None:
    lines: list[str] = []
    skills = by_type(entities, "Skill")
    cats   = by_type(entities, "SkillCategory")
    pkgs   = by_type(entities, "SoftwarePackage")
    tools  = by_type(entities, "Tool")

    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines += [
        f"# SkillChain Ecosystem Report",
        f"",
        f"_Generated: {now}_",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Skills | {len(skills)} |",
        f"| Categories | {len(cats)} |",
        f"| Tools | {len(tools)} |",
        f"| Packages | {len(pkgs)} |",
        f"| Relations | {len(relations)} |",
        f"",
    ]

    # Category breakdown
    cat_map = {e["id"]: e for e in cats}
    cat_skills: dict[str, list[str]] = defaultdict(list)
    for r in relations:
        if r["rel"] == "belongs_to_category" and r["to"] in cat_map:
            skill = entities.get(r["from"])
            if skill:
                cat_skills[r["to"]].append(
                    skill["properties"].get("slug") or skill["properties"].get("name", ""))
    lines += ["## Category Distribution", ""]
    lines += ["| Category | Count | Skills |", "|----------|-------|--------|"]
    for cid, slugs in sorted(cat_skills.items(), key=lambda x: -len(x[1])):
        cname = cat_map[cid]["properties"].get("name", cid)
        sample = ", ".join(sorted(slugs)[:4])
        if len(slugs) > 4:
            sample += f", +{len(slugs)-4} more"
        lines.append(f"| {cname} | {len(slugs)} | {sample} |")
    lines.append("")

    # Top by stars (if enriched)
    enriched = [s for s in skills if s["properties"].get("stars") is not None]
    if enriched:
        top_stars = sorted(enriched, key=lambda s: s["properties"].get("stars", 0) or 0, reverse=True)[:10]
        lines += ["## Top 10 by Stars", ""]
        lines += ["| # | Skill | Stars | Downloads | Moderation |",
                  "|---|-------|-------|-----------|------------|"]
        for i, s in enumerate(top_stars, 1):
            p = s["properties"]
            sname = p.get("slug") or p.get("name", s["id"])
            mod   = p.get("moderation", "unreviewed")
            flag  = "⚠️" if mod in ("suspicious", "blocked") else "✓"
            lines.append(f"| {i} | {sname} | {p.get('stars','?')} | {p.get('downloads','?')} | {flag} {mod} |")
        lines.append("")

    # Top packages
    pkg_map = {e["id"]: e for e in pkgs}
    skill_ids = {e["id"] for e in skills}
    pkg_users: dict[str, set[str]] = defaultdict(set)
    for r in relations:
        if r["rel"] == "requires_package" and r["from"] in skill_ids and r["to"] in pkg_map:
            pkg_users[r["to"]].add(r["from"])
    top_pkgs = sorted(pkg_map.items(), key=lambda x: -len(pkg_users.get(x[0], set())))[:15]
    if top_pkgs:
        lines += ["## Most-Used Packages", ""]
        lines += ["| Package | Ecosystem | Used by N skills |", "|---------|-----------|-----------------|"]
        for pid, pkg in top_pkgs:
            p = pkg["properties"]
            lines.append(f"| {p.get('name',pid)} | {p.get('ecosystem','')} | {len(pkg_users.get(pid, set()))} |")
        lines.append("")

    # Moderation issues
    suspicious = [s for s in skills
                  if s["properties"].get("moderation") in ("suspicious", "blocked")]
    if suspicious:
        lines += ["## ⚠️  Security Flags", ""]
        lines += ["| Skill | Verdict |", "|-------|---------|"]
        for s in suspicious:
            p = s["properties"]
            lines.append(f"| {p.get('slug') or p.get('name',s['id'])} | {p.get('moderation','')} |")
        lines.append("")

    # Cycles
    cycles = detect_cycles(entities, relations)
    if cycles:
        lines += ["## ⚠️  Circular Skill Dependencies", ""]
        for cycle in cycles:
            names = [entity_name(entities[n]) if n in entities else n for n in cycle]
            lines.append(f"- {' → '.join(names)}")
        lines.append("")

    # Key Insights (auto-generated)
    insights = _generate_insights(entities, relations)
    if insights:
        lines += ["## 🔍 Key Insights", ""]
        for ins in insights:
            lines.append(f"- {ins}")
        lines.append("")

    report = "\n".join(lines)

    if out_path:
        Path(out_path).write_text(report)
        print(f"Report written to: {out_path}")
    else:
        print(report)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="SkillChain analysis")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("stats",      help="Ecosystem overview")
    sub.add_parser("categories", help="Category distribution")
    sub.add_parser("health",     help="Skill completeness health scores")
    sub.add_parser("overlaps",   help="Detect overlapping / complementary skills")

    p_top = sub.add_parser("top", help="Top skills by metric")
    p_top.add_argument("--by", default="stars",
                       choices=["stars", "downloads", "installs_current"])
    p_top.add_argument("--limit", type=int, default=10)

    p_profile = sub.add_parser("profile", help="Skill profile card")
    p_profile.add_argument("--skill", required=True)

    p_sc = sub.add_parser("supply-chain", help="Supply chain tree for a skill")
    p_sc.add_argument("--skill", required=True)

    p_pkgs = sub.add_parser("packages", help="Most-used packages")
    p_pkgs.add_argument("--top", type=int, default=20)

    p_fu = sub.add_parser("find-users", help="Skills using a specific package")
    p_fu.add_argument("--package", required=True)

    p_rep = sub.add_parser("report", help="Full markdown report with insights")
    p_rep.add_argument("--out", help="Write report to file")

    args = parser.parse_args()
    entities, relations = load()

    if args.cmd == "stats":
        cmd_stats(entities, relations)
    elif args.cmd == "categories":
        cmd_categories(entities, relations)
    elif args.cmd == "health":
        cmd_health(entities, relations)
    elif args.cmd == "overlaps":
        cmd_overlaps(entities, relations)
    elif args.cmd == "top":
        cmd_top(entities, relations, args.by, args.limit)
    elif args.cmd == "profile":
        cmd_profile(entities, relations, args.skill)
    elif args.cmd == "supply-chain":
        cmd_supply_chain(entities, relations, args.skill)
    elif args.cmd == "packages":
        cmd_packages(entities, relations, args.top)
    elif args.cmd == "find-users":
        cmd_find_users(entities, relations, args.package)
    elif args.cmd == "report":
        cmd_report(entities, relations, getattr(args, "out", None))


if __name__ == "__main__":
    main()
