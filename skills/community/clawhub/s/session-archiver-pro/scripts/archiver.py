#!/usr/bin/env python3
"""
Session Archiver Pro — Extract structured memory from AI chat sessions.

Usage:
  python3 archiver.py --file session.log
  python3 archiver.py --dir ./sessions/ --format json
  python3 archiver.py --file session.log --tags --graph
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


# ─── Category regex patterns ──────────────────────────────────────────────────

DECISION_PATTERNS = [
    r"(?i)(?:we|i|let's)\s+(?:decided?|chose?|selected?|settled?\s+on|opted?\s+for)",
    r"(?i)(?:final|ultimate|conclusive)\s+(?:decision|choice|pick)",
    r"(?i)(?:the\s+)?(?:plan|approach|strategy|direction)\s+(?:is|will\s+be|should\s+be)",
    r"(?i)(?:going\s+with|let's\s+go\s+with|we'll\s+(?:use|do|go))",
]

ACTION_PATTERNS = [
    r"(?i)(?:todo|to-do|action\s+item|next\s+step|follow[- ]up)",
    r"(?i)(?:need[s]?\s+to|have\s+to|must|should)\s+\w+",
    r"(?i)(?:by\s+\w+(?:\s+\d+)?|deadline|due\s+date|before\s+\w+)",
    r"(?i)assign(?:ed|ment)?\s+(?:to\s+)?@?\w+",
]

KNOWLEDGE_PATTERNS = [
    r"(?i)(?:key\s+)?(?:insight|takeaway|lesson|finding)",
    r"(?i)(?:importantly|notably|interestingly|crucially)",
    r"(?i)(?:did\s+you\s+know|as\s+it\s+turns\s+out|turns?\s+out\s+that)",
    r"(?i)(?:according\s+to|studies?\s+show|research\s+indicates?)",
]

PREFERENCE_PATTERNS = [
    r"(?i)(?:I\s+(?:prefer|like|love|enjoy|dislike|hate|don't\s+like))",
    r"(?i)(?:I'd\s+rather|I'm\s+(?:more\s+)?comfortable\s+with)",
    r"(?i)(?:not\s+my\s+(?:thing|style|preference))",
    r"(?i)(?:better\s+(?:suit|fit|match)|works\s+better\s+for\s+me)",
]

RISK_PATTERNS = [
    r"(?i)(?:risk|danger|concern|problem|issue|warning|caveat)",
    r"(?i)(?:watch\s+out\s+for|be\s+careful\s+about|potential\s+pitfall)",
    r"(?i)(?:might\s+not\s+work|could\s+be\s+a\s+problem|may\s+cause)",
    r"(?i)(?:bottleneck|single\s+point\s+of\s+failure|technical\s+debt)",
]


def parse_session_log(filepath: str) -> dict:
    """Parse a session log file into a structured dialogue list."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.split("\n")
    dialogue = []
    current_role = "unknown"
    current_text = []

    for line in lines:
        stripped = line.strip()
        if re.match(r"^(?:##\s*)?(?:User|Human|Me)\s*[:：]", stripped, re.I):
            if current_text:
                dialogue.append({"role": current_role, "text": "\n".join(current_text).strip()})
            current_role = "user"
            current_text = [re.sub(r"^(?:##\s*)?(?:User|Human|Me)\s*[:：]\s*", "", stripped, flags=re.I)]
        elif re.match(r"^(?:##\s*)?(?:Assistant|AI|Bot|Claude|GPT|DeepSeek)\s*[:：]", stripped, re.I):
            if current_text:
                dialogue.append({"role": current_role, "text": "\n".join(current_text).strip()})
            current_role = "assistant"
            current_text = [re.sub(r"^(?:##\s*)?(?:Assistant|AI|Bot|Claude|GPT|DeepSeek)\s*[:：]\s*", "", stripped, flags=re.I)]
        elif re.match(r"^\[?(?:Tool|Function|Plugin)\s*(?:Call|Result|Response)?\]?\s*[:：]", stripped, re.I):
            if current_text:
                dialogue.append({"role": current_role, "text": "\n".join(current_text).strip()})
            current_role = "tool"
            current_text = [re.sub(r"^\[?(?:Tool|Function|Plugin)\s*(?:Call|Result|Response)?\]?\s*[:：]\s*", "", stripped, flags=re.I)]
        elif stripped:
            current_text.append(stripped)

    if current_text:
        dialogue.append({"role": current_role, "text": "\n".join(current_text).strip()})

    return {
        "file": path.name,
        "dialogue": dialogue,
        "metadata": {
            "lines": len(lines),
            "turns": sum(1 for d in dialogue if d["role"] in ("user", "assistant")),
        },
    }


def extract_categories(dialogue: list) -> dict:
    """Extract 5 categories from dialogue using pattern matching."""
    categories = {
        "decisions": [],
        "actions": [],
        "knowledge": [],
        "preferences": [],
        "risks": [],
    }
    seen_texts = set()

    for turn in dialogue:
        text = turn["text"]
        role = turn["role"]

        # Decisions
        for pat in DECISION_PATTERNS:
            for m in re.finditer(pat, text):
                snippet = text[max(0, m.start()-40):m.end()+80].strip()
                if snippet not in seen_texts:
                    seen_texts.add(snippet)
                    categories["decisions"].append({
                        "text": snippet,
                        "role": role,
                        "confidence": "high" if m.group().startswith(("we", "The")) else "medium",
                    })

        # Actions
        for pat in ACTION_PATTERNS:
            for m in re.finditer(pat, text):
                snippet = text[max(0, m.start()-20):m.end()+60].strip()
                if snippet not in seen_texts:
                    seen_texts.add(snippet)
                    categories["actions"].append({
                        "text": snippet,
                        "role": role,
                    })

        # Knowledge
        for pat in KNOWLEDGE_PATTERNS:
            for m in re.finditer(pat, text):
                snippet = text[max(0, m.start()-10):m.end()+100].strip()
                if snippet not in seen_texts:
                    seen_texts.add(snippet)
                    categories["knowledge"].append({
                        "text": snippet,
                        "role": role,
                    })

        # Preferences
        for pat in PREFERENCE_PATTERNS:
            for m in re.finditer(pat, text):
                snippet = text[max(0, m.start()-5):m.end()+80].strip()
                if snippet not in seen_texts:
                    seen_texts.add(snippet)
                    categories["preferences"].append({
                        "text": snippet,
                        "role": role,
                    })

        # Risks
        for pat in RISK_PATTERNS:
            for m in re.finditer(pat, text):
                snippet = text[max(0, m.start()-15):m.end()+85].strip()
                if snippet not in seen_texts:
                    seen_texts.add(snippet)
                    categories["risks"].append({
                        "text": snippet,
                        "role": role,
                    })

    return categories


def generate_tags(categories: dict) -> list:
    """Auto-generate topic tags from extracted content."""
    tag_scores = defaultdict(int)
    keyword_map = {
        "pricing": ["pricing", "price", "cost", "budget", "revenue", "fee"],
        "product": ["product", "feature", "roadmap", "mvp", "launch"],
        "design": ["design", "ui", "ux", "mockup", "prototype", "wireframe"],
        "technical": ["api", "database", "architecture", "deploy", "migration", "backend"],
        "business": ["strategy", "market", "competitor", "growth", "saas"],
        "people": ["hire", "team", "role", "interview", "onboard"],
        "risk": ["risk", "concern", "danger", "warning", "compliance"],
        "legal": ["contract", "license", "nda", "compliance", "regulation"],
        "user-research": ["customer", "interview", "feedback", "survey", "persona"],
    }

    all_text = " ".join(
        item["text"] for cat in categories.values() for item in cat
    ).lower()

    for tag, keywords in keyword_map.items():
        score = sum(1 for kw in keywords if kw in all_text)
        if score >= 2:
            tag_scores[tag] = score

    sorted_tags = [t for t, _ in sorted(tag_scores.items(), key=lambda x: -x[1])]
    return sorted_tags[:8]


def build_cross_session_graph(sessions: list) -> list:
    """Build links between related items across sessions (placeholder)."""
    links = []
    for i, s1 in enumerate(sessions):
        for j, s2 in enumerate(sessions):
            if i >= j:
                continue
            # Simple overlap: shared category types
            for cat_name in ["decisions", "knowledge", "risks"]:
                items1 = s1.get("categories", {}).get(cat_name, [])
                items2 = s2.get("categories", {}).get(cat_name, [])
                if items1 and items2:
                    links.append({
                        "from": {"session": s1["file"], "category": cat_name, "count": len(items1)},
                        "to": {"session": s2["file"], "category": cat_name, "count": len(items2)},
                        "relation": f"shared {cat_name} category",
                    })
    return links


def generate_summary(categories: dict) -> str:
    """Generate a 5-sentence executive summary."""
    parts = []
    if categories["decisions"]:
        parts.append(f"📌 {len(categories['decisions'])} key decisions identified.")
    if categories["actions"]:
        parts.append(f"✅ {len(categories['actions'])} action items to follow up.")
    if categories["knowledge"]:
        parts.append(f"📚 {len(categories['knowledge'])} knowledge points extracted.")
    if categories["preferences"]:
        parts.append(f"⭐ {len(categories['preferences'])} user preferences noted.")
    if categories["risks"]:
        parts.append(f"⚠️ {len(categories['risks'])} risks or issues flagged.")
    parts.append("Session archived successfully.")
    return " ".join(parts)


def format_markdown(session_data: list, tags: list, summary: str, graph: list) -> str:
    """Format output as Markdown."""
    lines = [
        "# Session Memory Report",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        f"\n## Executive Summary\n{summary}\n",
    ]

    for session in session_data:
        cat = session["categories"]
        has_content = any(cat.values())
        if not has_content:
            continue
        lines.append(f"\n## Session: {session['file']}\n")

        for cat_name, label, emoji in [
            ("decisions", "Key Decisions", "📌"),
            ("actions", "Action Items", "✅"),
            ("knowledge", "Knowledge Points", "📚"),
            ("preferences", "User Preferences", "⭐"),
            ("risks", "Risks & Issues", "⚠️"),
        ]:
            items = cat.get(cat_name, [])
            if items:
                lines.append(f"\n### {emoji} {label} ({len(items)})")
                for i, item in enumerate(items[:10], 1):
                    confidence = item.get("confidence", "")
                    tag = f" [{confidence.upper()}]" if confidence else ""
                    lines.append(f"{i}. {item['text'][:120]}{'...' if len(item['text']) > 120 else ''}{tag}")

    if tags:
        lines.append(f"\n## Tags\n`{'`, `'.join(tags)}`\n")

    if graph:
        lines.append("## Cross-Session Links\n")
        for link in graph[:5]:
            lines.append(f"- \"{link['from']['session']}\" ↔ \"{link['to']['session']}\" ({link['relation']})")

    return "\n".join(lines)


def format_json(session_data: list, tags: list, summary: str, graph: list) -> str:
    """Format output as JSON."""
    output = {
        "generated": datetime.now().isoformat(),
        "summary": summary,
        "sessions": [
            {
                "file": s["file"],
                "categories": s["categories"],
            }
            for s in session_data
        ],
        "tags": tags,
        "cross_session_links": graph,
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


def format_obsidian(session_data: list, tags: list, summary: str, graph: list) -> str:
    """Format output as Obsidian-compatible notes."""
    lines = [
        "---",
        f"created: {datetime.now().strftime('%Y-%m-%d')}",
        f"tags: [{'/'.join(tags) if tags else 'session-archiver'}]",
        "---",
        "",
        f"# Session Memory Report",
        summary,
        "",
    ]

    for session in session_data:
        cat = session["categories"]
        lines.append(f"## [[{session['file'].replace('.', '_')}]]\n")
        for cat_name, label, emoji in [
            ("decisions", "Key Decisions", "📌"),
            ("actions", "Action Items", "✅"),
            ("knowledge", "Knowledge Points", "📚"),
            ("preferences", "User Preferences", "⭐"),
            ("risks", "Risks & Issues", "⚠️"),
        ]:
            items = cat.get(cat_name, [])
            if items:
                lines.append(f"### {emoji} {label}")
                for item in items[:10]:
                    lines.append(f"- {item['text'][:120]}")

    return "\n".join(lines)


def format_memory_inject(session_data: list, tags: list, summary: str, graph: list) -> str:
    """Format for agent long-term memory injection."""
    inject = {
        "source": "session-archiver-pro",
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "tags": tags,
        "memory_entries": [],
    }
    for session in session_data:
        for cat_name in ["decisions", "knowledge", "preferences"]:
            for item in session["categories"].get(cat_name, []):
                inject["memory_entries"].append({
                    "type": cat_name,
                    "content": item["text"][:200],
                    "source_session": session["file"],
                })
    return json.dumps(inject, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Session Archiver Pro — extract structured memory from AI chat logs")
    parser.add_argument("--file", type=str, help="Path to a single session log file")
    parser.add_argument("--dir", type=str, help="Directory containing session log files")
    parser.add_argument("--format", choices=["markdown", "json", "obsidian", "memory-inject"],
                        default="markdown", help="Output format")
    parser.add_argument("--tags", action="store_true", default=True, help="Enable auto-tagging")
    parser.add_argument("--graph", action="store_true", default=True, help="Enable cross-session linking")
    args = parser.parse_args()

    if not args.file and not args.dir:
        # Self-test mode: use embedded sample
        print("Session Archiver Pro — Self Test Mode\n")
        print("Usage: python3 archiver.py --file <session.log>")
        print("       python3 archiver.py --dir <session_dir> --format json\n")
        print("No input provided. Using embedded sample session...\n")

        sample = (
            "## User: Let's design our SaaS pricing model.\n\n"
            "We need to decide on a pricing structure. I've been thinking about usage-based.\n\n"
            "## Assistant: Great idea. Usage-based pricing aligns cost with value. What's our target?\n\n"
            "## User: I prefer targeting SMBs, 10-50 seats. Let's go with usage-based.\n\n"
            "## Assistant: Good choice. Competitors all do annual discounts of 15-20%.\n\n"
            "## User: But I'm not comfortable with annual-only billing. Monthly options only.\n\n"
            "## Assistant: Understood. Risk to watch: minimum commit could scare SMB segment.\n\n"
            "TODO: Validate competitive pricing by Friday.\n"
            "TODO: Conduct 5 customer interviews next week.\n"
        )

        Path("/tmp/_archiver_sample.log").write_text(sample)
        args.file = "/tmp/_archiver_sample.log"
        print("(Using sample session for demonstration)\n")

    sessions_data = []

    if args.file:
        parsed = parse_session_log(args.file)
        categories = extract_categories(parsed["dialogue"])
        parsed["categories"] = categories
        sessions_data.append(parsed)

    if args.dir:
        dir_path = Path(args.dir)
        if not dir_path.is_dir():
            print(f"Error: directory not found: {args.dir}", file=sys.stderr)
            sys.exit(1)
        for f in sorted(dir_path.glob("*")):
            if f.suffix in (".log", ".txt", ".json", ".md"):
                parsed = parse_session_log(str(f))
                categories = extract_categories(parsed["dialogue"])
                parsed["categories"] = categories
                sessions_data.append(parsed)

    if not sessions_data:
        print("No session data found.", file=sys.stderr)
        sys.exit(1)

    # Aggregate all categories for summary
    all_cats = {
        "decisions": [],
        "actions": [],
        "knowledge": [],
        "preferences": [],
        "risks": [],
    }
    for s in sessions_data:
        for k in all_cats:
            all_cats[k].extend(s["categories"].get(k, []))

    tags = generate_tags(all_cats) if args.tags else []
    summary = generate_summary(all_cats)
    graph = build_cross_session_graph(sessions_data) if args.graph else []

    # Format and print
    formatters = {
        "markdown": format_markdown,
        "json": format_json,
        "obsidian": format_obsidian,
        "memory-inject": format_memory_inject,
    }
    output = formatters[args.format](sessions_data, tags, summary, graph)
    print(output)


if __name__ == "__main__":
    main()
