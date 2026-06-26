#!/usr/bin/env python3
"""
Self-Improving Agent → ExpertPack Converter

Converts a Self-Improving Agent skill's .learnings/ directory into a structured
ExpertPack. Handles: LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md, and promoted
content from workspace files (CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md).

Usage:
    python3 convert.py --workspace /path/to/workspace --output ~/expertpacks/my-learnings
    python3 convert.py --workspace . --output ./export --name "My Learnings" --type process
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# --- Secret patterns to strip ---
SECRET_PATTERNS = [
    re.compile(r'sk-[a-zA-Z0-9]{20,}'),
    re.compile(r'ghp_[a-zA-Z0-9]{36,}'),
    re.compile(r'xoxb-[a-zA-Z0-9\-]+'),
    re.compile(r'(?:api[_-]?key|token|secret|password|bearer)\s*[:=]\s*\S+', re.IGNORECASE),
]

# Entry header pattern: ## [TYPE-YYYYMMDD-XXX] description
ENTRY_HEADER = re.compile(r'^##\s+\[((?:LRN|ERR|FEAT)-\d{8}-\w+)\]\s*(.*)', re.MULTILINE)

# Metadata field pattern: **Key**: value
META_FIELD = re.compile(r'^\*\*(\w[\w\s-]*)\*\*:\s*(.+)$', re.MULTILINE)


def strip_secrets(text: str) -> tuple[str, list[str]]:
    """Strip secret patterns from text. Returns (cleaned_text, warnings)."""
    warnings = []
    for pat in SECRET_PATTERNS:
        matches = pat.findall(text)
        if matches:
            warnings.append(f"Stripped {len(matches)} potential secret(s) matching {pat.pattern[:40]}...")
            text = pat.sub("[REDACTED]", text)
    return text, warnings


# --- Parsing ---

def parse_entries(filepath: Path) -> list[dict]:
    """Parse a .learnings/ file into structured entries."""
    if not filepath.exists():
        return []

    content = filepath.read_text(errors="replace")
    content, _ = strip_secrets(content)

    entries = []
    # Split on entry headers
    parts = ENTRY_HEADER.split(content)

    # parts[0] = preamble (before first entry), then groups of 3: (id, desc_after_bracket, body)
    i = 1
    while i + 2 <= len(parts):
        entry_id = parts[i]
        category_or_name = parts[i + 1].strip()
        body = parts[i + 2] if i + 2 < len(parts) else ""
        i += 3

        # Parse metadata fields from body
        meta = {}
        for m in META_FIELD.finditer(body):
            key = m.group(1).strip().lower().replace(" ", "_").replace("-", "_")
            meta[key] = m.group(2).strip()

        # Extract named sections from body
        sections = {}
        current_section = None
        current_lines = []
        for line in body.split("\n"):
            if line.startswith("### "):
                if current_section and current_lines:
                    sections[current_section] = "\n".join(current_lines).strip()
                current_section = line[4:].strip().lower()
                current_lines = []
            elif current_section is not None:
                current_lines.append(line)
        if current_section and current_lines:
            sections[current_section] = "\n".join(current_lines).strip()

        # Determine entry type from ID prefix
        entry_type = "learning"
        if entry_id.startswith("ERR"):
            entry_type = "error"
        elif entry_id.startswith("FEAT"):
            entry_type = "feature_request"

        entries.append({
            "id": entry_id,
            "type": entry_type,
            "category": category_or_name,
            "meta": meta,
            "sections": sections,
            "raw_body": body.strip(),
        })

    return entries


def parse_promoted_content(workspace: Path) -> dict[str, str]:
    """Check workspace files for content that was promoted from learnings."""
    promoted = {}
    for fname in ["CLAUDE.md", "AGENTS.md", "SOUL.md", "TOOLS.md",
                   ".github/copilot-instructions.md"]:
        fpath = workspace / fname
        if fpath.exists():
            content = fpath.read_text(errors="replace")
            content, _ = strip_secrets(content)
            # Only include if it references learnings or self-improvement
            if any(kw in content.lower() for kw in
                   ["learning", "self-improv", "lrn-", "err-", "feat-", ".learnings"]):
                promoted[fname] = content
    return promoted


# --- Classification ---

def classify_learning(entry: dict) -> str:
    """Classify a learning entry into an EP directory."""
    category = entry.get("category", "").lower()
    meta = entry.get("meta", {})
    status = meta.get("status", "").lower()

    # Promoted entries → mind (they're proven rules)
    if status == "promoted":
        return "mind"

    # By category
    category_map = {
        "best_practice": "mind",
        "correction": "facts",
        "knowledge_gap": "facts",
        "convention": "mind",
        "workflow": "mind",
        "pattern": "summaries",
        "simplify": "mind",
        "harden": "mind",
        "security": "mind",
        "tool": "operational",
        "integration": "operational",
        "api": "operational",
        "config": "operational",
        "behavioral": "mind",
    }

    for key, ep_dir in category_map.items():
        if key in category:
            return ep_dir

    # By area metadata
    area = meta.get("area", "").lower()
    area_map = {
        "frontend": "facts",
        "backend": "facts",
        "infra": "operational",
        "tests": "operational",
        "docs": "facts",
        "config": "operational",
    }

    for key, ep_dir in area_map.items():
        if key in area:
            return ep_dir

    return "facts"


def classify_error(entry: dict) -> str:
    """Classify an error entry into an EP directory."""
    meta = entry.get("meta", {})
    status = meta.get("status", "").lower()

    # Resolved errors with fixes → operational (they're reference material)
    if status == "resolved":
        return "operational"

    # Recurring errors → summaries (pattern analysis)
    sections = entry.get("sections", {})
    if "see also" in entry.get("raw_body", "").lower():
        return "summaries"

    return "operational"


def classify_feature(entry: dict) -> str:
    """Classify a feature request into an EP directory."""
    meta = entry.get("meta", {})
    complexity = meta.get("complexity_estimate", "").lower()

    if complexity == "complex":
        return "summaries"  # architectural discussion

    return "facts"  # desired capabilities


# --- EP Generation ---

def format_entry_body(entry: dict) -> str:
    """Format an entry into readable markdown content."""
    parts = []
    meta = entry.get("meta", {})
    sections = entry.get("sections", {})

    # Metadata line
    meta_parts = []
    if meta.get("priority"):
        meta_parts.append(f"Priority: {meta['priority']}")
    if meta.get("status"):
        meta_parts.append(f"Status: {meta['status']}")
    if meta.get("area"):
        meta_parts.append(f"Area: {meta['area']}")
    if meta.get("logged"):
        meta_parts.append(f"Logged: {meta['logged'][:10]}")
    if meta_parts:
        parts.append(f"*{' | '.join(meta_parts)}*")

    # Key sections
    for sec_name in ["summary", "details", "error", "context", "suggested action",
                     "suggested fix", "requested capability", "user context",
                     "suggested implementation", "resolution"]:
        if sec_name in sections and sections[sec_name].strip():
            content = sections[sec_name].strip()
            # Strip metadata lines from section content
            content_lines = [l for l in content.split("\n")
                             if not META_FIELD.match(l)]
            cleaned = "\n".join(content_lines).strip()
            if cleaned:
                parts.append(cleaned)

    # Tags and cross-references
    tags = meta.get("tags")
    see_also = None
    for sec_name in ["metadata"]:
        if sec_name in sections:
            see_match = re.search(r'See Also:\s*(.+)', sections[sec_name])
            if see_match:
                see_also = see_match.group(1).strip()
            tag_match = re.search(r'Tags:\s*(.+)', sections[sec_name])
            if tag_match and not tags:
                tags = tag_match.group(1).strip()

    if tags:
        parts.append(f"*Tags: {tags}*")
    if see_also:
        parts.append(f"*See also: {see_also}*")

    # Pattern tracking
    pattern_key = meta.get("pattern_key") or meta.get("pattern-key")
    recurrence = meta.get("recurrence_count") or meta.get("recurrence-count")
    if pattern_key:
        pat_line = f"*Pattern: {pattern_key}"
        if recurrence:
            pat_line += f" (seen {recurrence}x)"
        pat_line += "*"
        parts.append(pat_line)

    return "\n\n".join(parts) if parts else entry.get("raw_body", "").strip()[:500]


def write_content_file(output_dir: Path, directory: str, filename: str,
                       title: str, lead: str, body: str) -> Path:
    """Write a content file to the EP structure."""
    dir_path = output_dir / directory
    dir_path.mkdir(parents=True, exist_ok=True)

    filepath = dir_path / filename
    content = f"# {title}\n\n> **Lead summary:** {lead}\n\n{body}\n"

    # ~3KB soft limit
    if len(content.encode()) > 3500:
        content = content[:3400] + "\n\n*[Truncated — see source files for full content]*\n"

    with open(filepath, "w") as f:
        f.write(content)

    return filepath


def write_index(output_dir: Path, directory: str, entries: list[tuple[str, str]]) -> None:
    """Write _index.md for a directory."""
    dir_path = output_dir / directory
    if not dir_path.exists():
        return

    content = f"# {directory.replace('/', '').title()}\n\n"
    for filename, desc in entries:
        name = filename.replace(".md", "").replace("-", " ").title()
        content += f"- [{name}]({filename}) — {desc}\n"

    with open(dir_path / "_index.md", "w") as f:
        f.write(content)


def generate_manifest(output_dir: Path, name: str, pack_type: str, subtype: str,
                      stats: dict) -> None:
    """Generate manifest.yaml."""
    manifest = {
        "name": name,
        "slug": re.sub(r'[^a-z0-9-]', '-', name.lower()).strip('-'),
        "type": pack_type,
        "version": "1.0.0",
        "schema_version": "2.3",
        "description": (
            f"ExpertPack converted from Self-Improving Agent learnings. "
            f"{stats['total_entries']} entries across {stats['source_files']} source files."
        ),
        "entry_point": "overview.md",
        "author": "self-improving-to-expertpack converter",
        "created": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }

    if subtype:
        manifest["subtype"] = subtype

    always_files = ["overview.md"]
    searchable_dirs = []
    for d in ["mind", "facts", "summaries", "operational", "relationships"]:
        if (output_dir / d).exists():
            searchable_dirs.append(f"{d}/")

    manifest["context"] = {
        "always": always_files,
        "searchable": searchable_dirs,
    }

    with open(output_dir / "manifest.yaml", "w") as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, width=120)


def generate_overview(output_dir: Path, name: str, stats: dict,
                      warnings: list[str]) -> None:
    """Generate overview.md."""
    content = f"""# {name}

> **Lead summary:** Agent knowledge pack converted from Self-Improving Agent learnings. Contains {stats['total_entries']} entries ({stats.get('learnings', 0)} learnings, {stats.get('errors', 0)} errors, {stats.get('features', 0)} feature requests) distilled into structured ExpertPack format.

## Source Summary

| Source | Entries | Status |
|--------|---------|--------|
| LEARNINGS.md | {stats.get('learnings', 0)} | {"✅ Converted" if stats.get('learnings') else "⬜ Not found"} |
| ERRORS.md | {stats.get('errors', 0)} | {"✅ Converted" if stats.get('errors') else "⬜ Not found"} |
| FEATURE_REQUESTS.md | {stats.get('features', 0)} | {"✅ Converted" if stats.get('features') else "⬜ Not found"} |
| Promoted content | {stats.get('promoted_files', 0)} files | {"✅ Cross-referenced" if stats.get('promoted_files') else "⬜ None detected"} |

## Priority Breakdown

| Priority | Count |
|----------|-------|
| Critical | {stats.get('priority_critical', 0)} |
| High | {stats.get('priority_high', 0)} |
| Medium | {stats.get('priority_medium', 0)} |
| Low | {stats.get('priority_low', 0)} |
| Unset | {stats.get('priority_unset', 0)} |

## Status Breakdown

| Status | Count |
|--------|-------|
| Resolved | {stats.get('status_resolved', 0)} |
| Promoted | {stats.get('status_promoted', 0)} |
| Pending | {stats.get('status_pending', 0)} |
| In Progress | {stats.get('status_in_progress', 0)} |
| Won't Fix | {stats.get('status_wont_fix', 0)} |
| Other | {stats.get('status_other', 0)} |

## Category Distribution

"""
    for cat, count in sorted(stats.get("categories", {}).items(), key=lambda x: -x[1]):
        content += f"- **{cat}**: {count}\n"

    if stats.get("pattern_keys"):
        content += "\n## Recurring Patterns\n\n"
        for pk, count in sorted(stats["pattern_keys"].items(), key=lambda x: -x[1]):
            content += f"- `{pk}` — seen {count}x\n"

    if stats.get("see_also_links"):
        content += f"\n## Cross-References\n\n{stats['see_also_links']} See Also links detected and mapped to relations.yaml.\n"

    content += "\n## Notes\n\n"
    content += "- Entries with status `promoted` were already elevated to workspace files (CLAUDE.md, AGENTS.md, etc.).\n"
    content += "- Secrets were automatically stripped during conversion.\n"
    content += "- Recurring patterns (Recurrence-Count ≥ 3) are marked as high-value knowledge.\n"

    if warnings:
        content += "\n## Warnings\n\n"
        for w in warnings:
            content += f"- {w}\n"

    content += f"\n---\n*Converted: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*\n"

    with open(output_dir / "overview.md", "w") as f:
        f.write(content)


# --- Relation Graph ---

def build_relations(all_entries: list[dict]) -> dict:
    """Build relations.yaml from See Also links and shared tags."""
    entities = []
    relations = []
    entity_ids = set()

    # Build entity list
    for entry in all_entries:
        eid = entry["id"]
        entity_ids.add(eid)
        etype = {
            "learning": "concept",
            "error": "event",
            "feature_request": "concept",
        }.get(entry["type"], "concept")

        category = entry.get("category", "")
        entities.append({
            "id": eid,
            "type": etype,
            "label": f"{entry['type'].replace('_', ' ').title()}: {category}",
        })

    # Build relations from See Also links
    see_also_count = 0
    for entry in all_entries:
        body = entry.get("raw_body", "")
        see_matches = re.findall(r'See Also[:\s]*([A-Z]+-\d{8}-\w+)', body)
        for target_id in see_matches:
            if target_id in entity_ids:
                relations.append({
                    "source": entry["id"],
                    "target": target_id,
                    "type": "related_to",
                    "label": "See Also",
                })
                see_also_count += 1

    # Build relations from shared tags
    tag_groups: dict[str, list[str]] = {}
    for entry in all_entries:
        meta = entry.get("meta", {})
        tags_str = meta.get("tags", "")
        if not tags_str:
            # Check sections metadata
            sections = entry.get("sections", {})
            if "metadata" in sections:
                tag_match = re.search(r'Tags:\s*(.+)', sections["metadata"])
                if tag_match:
                    tags_str = tag_match.group(1).strip()

        if tags_str:
            for tag in re.split(r'[,;]\s*', tags_str):
                tag = tag.strip().lower()
                if tag:
                    tag_groups.setdefault(tag, []).append(entry["id"])

    # Connect entries that share tags (max 3 tags to limit explosion)
    tag_relations_added = 0
    for tag, members in tag_groups.items():
        if len(members) > 1 and tag_relations_added < 50:
            for i in range(len(members)):
                for j in range(i + 1, min(i + 4, len(members))):
                    relations.append({
                        "source": members[i],
                        "target": members[j],
                        "type": "shares_tag",
                        "label": f"Tag: {tag}",
                    })
                    tag_relations_added += 1

    return {
        "entities": entities,
        "relations": relations,
        "see_also_count": see_also_count,
    }


# --- Main Conversion ---

def convert(workspace: Path, output: Path, name: str, pack_type: str,
            learnings_dir: Path | None = None) -> None:
    """Run the full conversion."""

    print(f"\n{'='*60}")
    print(f"Self-Improving Agent → ExpertPack Converter")
    print(f"Workspace: {workspace}")
    print(f"Output: {output}")
    print(f"{'='*60}\n")

    output.mkdir(parents=True, exist_ok=True)
    all_warnings: list[str] = []
    all_entries: list[dict] = []

    # Locate .learnings/ directory
    if learnings_dir is None:
        learnings_dir = workspace / ".learnings"

    if not learnings_dir.exists():
        print(f"⚠️  .learnings/ directory not found at {learnings_dir}")
        print(f"   Trying workspace root...")
        # Some users might have the files at root level
        if (workspace / "LEARNINGS.md").exists():
            learnings_dir = workspace
        else:
            print(f"❌ No learnings files found. Nothing to convert.")
            sys.exit(1)

    # --- Parse all entry files ---
    source_files = 0

    learnings_file = learnings_dir / "LEARNINGS.md"
    learnings = parse_entries(learnings_file)
    if learnings:
        source_files += 1
        all_entries.extend(learnings)
        print(f"✅ LEARNINGS.md: {len(learnings)} entries")
    else:
        print(f"⬜ LEARNINGS.md: not found or empty")

    errors_file = learnings_dir / "ERRORS.md"
    errors = parse_entries(errors_file)
    if errors:
        source_files += 1
        all_entries.extend(errors)
        print(f"✅ ERRORS.md: {len(errors)} entries")
    else:
        print(f"⬜ ERRORS.md: not found or empty")

    features_file = learnings_dir / "FEATURE_REQUESTS.md"
    features = parse_entries(features_file)
    if features:
        source_files += 1
        all_entries.extend(features)
        print(f"✅ FEATURE_REQUESTS.md: {len(features)} entries")
    else:
        print(f"⬜ FEATURE_REQUESTS.md: not found or empty")

    if not all_entries:
        print(f"\n❌ No entries found in any source file. Nothing to convert.")
        sys.exit(1)

    # --- Compute stats ---
    stats = {
        "total_entries": len(all_entries),
        "source_files": source_files,
        "learnings": len(learnings),
        "errors": len(errors),
        "features": len(features),
        "categories": {},
        "pattern_keys": {},
        "see_also_links": 0,
    }

    # Priority/status counters
    for p in ["critical", "high", "medium", "low"]:
        stats[f"priority_{p}"] = 0
    stats["priority_unset"] = 0

    for s in ["resolved", "promoted", "pending", "in_progress", "wont_fix"]:
        stats[f"status_{s}"] = 0
    stats["status_other"] = 0

    for entry in all_entries:
        meta = entry.get("meta", {})

        # Category
        cat = entry.get("category", "uncategorized")
        stats["categories"][cat] = stats["categories"].get(cat, 0) + 1

        # Priority
        priority = meta.get("priority", "").lower()
        if priority in ["critical", "high", "medium", "low"]:
            stats[f"priority_{priority}"] += 1
        else:
            stats["priority_unset"] += 1

        # Status
        status = meta.get("status", "").lower().replace(" ", "_")
        if status in ["resolved", "promoted", "pending", "in_progress", "wont_fix"]:
            stats[f"status_{status}"] += 1
        else:
            stats["status_other"] += 1

        # Pattern keys
        pk = meta.get("pattern_key") or meta.get("pattern-key")
        if pk:
            rc_str = meta.get("recurrence_count") or meta.get("recurrence-count") or "1"
            try:
                rc = int(rc_str)
            except ValueError:
                rc = 1
            stats["pattern_keys"][pk] = max(stats["pattern_keys"].get(pk, 0), rc)

    # --- Check for promoted content ---
    promoted_content = parse_promoted_content(workspace)
    stats["promoted_files"] = len(promoted_content)
    if promoted_content:
        print(f"\n✅ Promoted content found in: {', '.join(promoted_content.keys())}")

    # --- Classify and group entries ---
    index_entries: dict[str, list[tuple[str, str]]] = {}
    classified: dict[str, list[dict]] = {}

    for entry in all_entries:
        if entry["type"] == "learning":
            ep_dir = classify_learning(entry)
        elif entry["type"] == "error":
            ep_dir = classify_error(entry)
        else:
            ep_dir = classify_feature(entry)
        classified.setdefault(ep_dir, []).append(entry)

    # --- Write content files ---
    print(f"\nWriting ExpertPack files...")

    for ep_dir, entries in classified.items():
        # Group by sub-category for better organization
        by_type: dict[str, list[dict]] = {}
        for e in entries:
            by_type.setdefault(e["type"], []).append(e)

        for entry_type, type_entries in by_type.items():
            # Sort: promoted/resolved first, then by priority
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            status_order = {"promoted": 0, "resolved": 1, "in_progress": 2, "pending": 3}

            type_entries.sort(key=lambda e: (
                status_order.get(e.get("meta", {}).get("status", "").lower(), 4),
                priority_order.get(e.get("meta", {}).get("priority", "").lower(), 4),
            ))

            # Build body
            body_parts = []
            for e in type_entries:
                header = f"## {e['id']}: {e['category']}"
                body = format_entry_body(e)
                body_parts.append(f"{header}\n\n{body}")

            type_label = entry_type.replace("_", " ").title()
            slug = entry_type.replace("_", "-")
            filename = f"{slug}s.md"

            lead = (
                f"{len(type_entries)} {type_label.lower()} entries classified as "
                f"{ep_dir} knowledge."
            )

            write_content_file(
                output, ep_dir, filename,
                f"{type_label}s — {ep_dir.title()}",
                lead,
                "\n\n---\n\n".join(body_parts)
            )
            index_entries.setdefault(ep_dir, []).append(
                (filename, f"{len(type_entries)} {type_label.lower()} entries")
            )
            print(f"  📄 {ep_dir}/{filename} ({len(type_entries)} entries)")

    # --- Write promoted content as separate reference file ---
    if promoted_content:
        body_parts = []
        for fname, content in promoted_content.items():
            body_parts.append(f"## From {fname}\n\n{content}")

        write_content_file(
            output, "mind", "promoted-rules.md",
            "Promoted Rules & Conventions",
            f"Rules and patterns promoted from learnings to {len(promoted_content)} workspace files.",
            "\n\n---\n\n".join(body_parts)
        )
        index_entries.setdefault("mind", []).append(
            ("promoted-rules.md", f"Rules promoted to {len(promoted_content)} workspace files")
        )
        print(f"  📄 mind/promoted-rules.md ({len(promoted_content)} source files)")

    # --- Write _index.md files ---
    for ep_dir, idx_entries in index_entries.items():
        write_index(output, ep_dir, idx_entries)

    # --- Build and write relations.yaml ---
    relations_data = build_relations(all_entries)
    stats["see_also_links"] = relations_data["see_also_count"]

    if relations_data["entities"]:
        rel_output = {
            "entities": relations_data["entities"],
            "relations": relations_data["relations"],
        }
        with open(output / "relations.yaml", "w") as f:
            yaml.dump(rel_output, f, default_flow_style=False, sort_keys=False, width=120)
        print(f"  📄 relations.yaml ({len(relations_data['entities'])} entities, "
              f"{len(relations_data['relations'])} relations)")

    # --- Build glossary from tags and categories ---
    all_tags = set()
    for entry in all_entries:
        meta = entry.get("meta", {})
        tags_str = meta.get("tags", "")
        if not tags_str:
            sections = entry.get("sections", {})
            if "metadata" in sections:
                tag_match = re.search(r'Tags:\s*(.+)', sections["metadata"])
                if tag_match:
                    tags_str = tag_match.group(1).strip()
        if tags_str:
            for tag in re.split(r'[,;]\s*', tags_str):
                tag = tag.strip()
                if tag:
                    all_tags.add(tag)

    all_categories = set(e.get("category", "") for e in all_entries if e.get("category"))

    if all_tags or all_categories:
        glossary_parts = []
        if all_categories:
            glossary_parts.append("## Categories\n")
            for cat in sorted(all_categories):
                glossary_parts.append(f"- **{cat}** — Learning category")
        if all_tags:
            glossary_parts.append("\n## Tags\n")
            for tag in sorted(all_tags):
                glossary_parts.append(f"- **{tag}**")

        with open(output / "glossary.md", "w") as f:
            f.write("# Glossary\n\n" + "\n".join(glossary_parts) + "\n")
        print(f"  📄 glossary.md ({len(all_categories)} categories, {len(all_tags)} tags)")

    # --- Determine pack type ---
    detected_subtype = ""
    if pack_type == "auto":
        # Self-improving learnings are typically process knowledge
        pack_type = "process"
        print(f"\n  Auto-detected pack type: process (agent improvement workflow)")
    elif pack_type == "agent":
        pack_type = "person"
        detected_subtype = "agent"

    # --- Generate manifest and overview ---
    generate_manifest(output, name, pack_type, detected_subtype, stats)
    generate_overview(output, name, stats, all_warnings)

    # --- Summary ---
    file_count = sum(1 for _ in output.rglob("*.md")) + sum(1 for _ in output.rglob("*.yaml"))
    total_size = sum(f.stat().st_size for f in output.rglob("*") if f.is_file())

    print(f"\n{'='*60}")
    print(f"Conversion Complete")
    print(f"{'='*60}")
    print(f"Pack: {name}")
    print(f"Type: {pack_type}" + (f" (subtype: {detected_subtype})" if detected_subtype else ""))
    print(f"Total entries: {stats['total_entries']}")
    print(f"  Learnings: {stats['learnings']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Feature Requests: {stats['features']}")
    print(f"Files generated: {file_count}")
    print(f"Total size: {total_size / 1024:.1f} KB")
    print(f"Output: {output}")

    if all_warnings:
        print(f"\n⚠️  {len(all_warnings)} warnings:")
        for w in all_warnings[:5]:
            print(f"  - {w}")

    print(f"\nNext steps:")
    print(f"  1. Review overview.md and manifest.yaml")
    print(f"  2. Run chunker: python3 chunk.py --pack {output} --output {output}/.chunks")
    print(f"  3. Measure EK: python3 eval-ek.py {output}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Self-Improving Agent learnings into an ExpertPack"
    )
    parser.add_argument("--workspace", "-w", type=Path, required=True,
                        help="Path to the OpenClaw workspace containing .learnings/")
    parser.add_argument("--output", "-o", type=Path, required=True,
                        help="Output directory for the ExpertPack")
    parser.add_argument("--name", "-n", type=str, default="Agent Learnings",
                        help="Pack name (default: 'Agent Learnings')")
    parser.add_argument("--type", "-t", type=str, default="auto",
                        choices=["auto", "person", "agent", "product", "process"],
                        help="Pack type (default: auto-detect)")
    parser.add_argument("--learnings", "-l", type=Path, default=None,
                        help="Path to .learnings/ directory (auto-detected if omitted)")

    args = parser.parse_args()

    if not args.workspace.exists():
        print(f"Error: Workspace not found: {args.workspace}", file=sys.stderr)
        sys.exit(1)

    convert(
        workspace=args.workspace,
        output=args.output,
        name=args.name,
        pack_type=args.type,
        learnings_dir=args.learnings,
    )


if __name__ == "__main__":
    main()
