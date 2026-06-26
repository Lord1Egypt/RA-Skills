#!/usr/bin/env python3
"""
classify_memory.py — Analyze and tag memory entries with type prefixes.

Scans MEMORY.md and memory/*.md for untagged entries and suggests/applies
type classifications: [PREF], [PROJ], [TECH], [LESSON], [PEOPLE].
Uses keyword matching + character n-gram similarity for CJK/mixed text.
"""

import argparse
import os
import re
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")))

# Keywords that hint at each memory type
TYPE_KEYWORDS = {
    "PREF": [
        "prefer", "like", "dislike", "hate", "favorite", "favourite", "style",
        "习惯", "喜欢", "讨厌", "偏好", "风格", "颜色", "color", "always use",
        "never use", "default", "communication", "口味", "爱好", "爱用",
        "不用", "倾向", "方式", "comfortable", "uncomfortable",
    ],
    "PROJ": [
        "project", "repo", "repository", "deploy", "website", "app", "service",
        "项目", "网站", "仓库", "部署", "located at", "working on", "building",
        "http://", "https://", "github.com", "domain", "功能", "模块", "需求",
        "开发", "上线", "版本", "release", "milestone", "sprint",
    ],
    "TECH": [
        "config", "database", "sqlite", "api", "endpoint", "port", "server",
        "技术", "配置", "数据库", "端口", "服务器", "prompt", "template",
        "node", "python", "docker", "nginx", "ssh", "函数", "方法", "接口",
        "框架", "library", "package", "依赖", "npm", "pip", "环境",
    ],
    "LESSON": [
        "lesson", "learned", "mistake", "error", "bug", "don't", "never",
        "教训", "错误", "记住", "always verify", "make sure", "reminder",
        "before building", "workflow", "坑", "踩过", "注意", "别",
        "warning", "gotcha", "trap", "fix",
    ],
    "PEOPLE": [
        "user", "person", "name", "he", "she", "they", "team", "colleague",
        "用户", "人", "名字", "老板", "老大", "朋友", "同事", "客户",
        "partner", "contact", "contributor", "maintainer",
    ],
}

TYPE_TAG_PATTERN = re.compile(r"\[(PREF|PROJ|TECH|LESSON|PEOPLE|TEMP)\]", re.IGNORECASE)
SECTION_HEADER = re.compile(r"^##\s+(?:\[([A-Z]+)\]\s+)?(.+)$")


def char_ngrams(s: str, n: int = 2) -> set:
    """Generate character n-grams from a string."""
    s = s.lower()
    if len(s) < n:
        return {s} if s else set()
    return {s[i:i+n] for i in range(len(s) - n + 1)}


def ngram_similarity(text: str, keywords: list[str], n: int = 2) -> float:
    """Calculate max character n-gram overlap between text and any keyword."""
    text_ngrams = char_ngrams(text, n)
    if not text_ngrams:
        return 0.0

    max_score = 0.0
    for kw in keywords:
        kw_ngrams = char_ngrams(kw, n)
        if not kw_ngrams:
            continue
        overlap = len(text_ngrams & kw_ngrams)
        score = overlap / max(len(text_ngrams), len(kw_ngrams))
        max_score = max(max_score, score)

    return max_score


def classify_line(line: str) -> tuple[str | None, float]:
    """Classify a line by keyword matching + n-gram similarity. Returns (type, confidence)."""
    lower = line.lower()
    scores = {}

    for mem_type, keywords in TYPE_KEYWORDS.items():
        # Exact keyword match (weight: 1.0 each)
        exact_score = sum(1 for kw in keywords if kw in lower)

        # N-gram similarity for top keywords (weight: 2.0 max)
        ngram_score = ngram_similarity(lower, keywords[:8]) * 2

        total = exact_score + ngram_score
        if total > 0:
            scores[mem_type] = total

    if not scores:
        return None, 0.0

    best = max(scores, key=scores.get)
    total = sum(scores.values())
    confidence = scores[best] / total if total > 0 else 0.0
    return best, round(confidence, 2)


def analyze_file(filepath: Path) -> list[dict]:
    """Analyze a memory file and return untagged entries with suggestions."""
    results = []
    content = filepath.read_text(encoding="utf-8")
    current_section_type = None

    for i, line in enumerate(content.split("\n"), 1):
        # Track current section type from headers
        header_match = SECTION_HEADER.match(line)
        if header_match:
            tag = header_match.group(1)
            if tag:
                current_section_type = tag.upper()
            continue

        # Skip lines that already have type tags
        if TYPE_TAG_PATTERN.search(line):
            continue

        # Only classify non-empty list items or meaningful lines
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("```"):
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            suggested_type, confidence = classify_line(stripped)

            # If we're in a typed section, inherit section type if no better suggestion
            if current_section_type and not suggested_type:
                suggested_type = current_section_type
                confidence = 0.5

            if suggested_type:
                results.append({
                    "file": str(filepath),
                    "line": i,
                    "content": stripped[:100],
                    "suggested_type": suggested_type,
                    "confidence": confidence,
                    "section_type": current_section_type,
                })

    return results


def check_duplicates(filepath: Path, new_entry: str) -> bool:
    """Check if a similar entry already exists in MEMORY.md."""
    memory_file = WORKSPACE / "MEMORY.md"
    if not memory_file.exists() or filepath == memory_file:
        return False

    content = memory_file.read_text(encoding="utf-8").lower()
    new_lower = new_entry.lower().strip()

    # Check for exact substring match
    if new_lower in content:
        return True

    # Check n-gram similarity (>0.7 = likely duplicate)
    new_ngrams = char_ngrams(new_lower, 3)
    for line in content.split("\n"):
        line_ngrams = char_ngrams(line.lower().strip(), 3)
        if new_ngrams and line_ngrams:
            overlap = len(new_ngrams & line_ngrams)
            sim = overlap / max(len(new_ngrams), len(line_ngrams))
            if sim > 0.7:
                return True

    return False


def apply_tags(filepath: Path, suggestions: list[dict], dry_run: bool) -> int:
    """Apply type tags to a file. Returns count of modifications."""
    if not suggestions:
        return 0

    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")
    applied = 0
    skipped_dupes = 0

    # Sort by line number descending to avoid offset issues
    suggestions.sort(key=lambda x: x["line"], reverse=True)

    for sugg in suggestions:
        line_idx = sugg["line"] - 1
        if line_idx >= len(lines):
            continue

        line = lines[line_idx]
        if TYPE_TAG_PATTERN.search(line):
            continue

        # Check for duplicates in MEMORY.md before applying
        if check_duplicates(filepath, sugg["content"]):
            skipped_dupes += 1
            continue

        tag = f"[{sugg['suggested_type']}]"
        # Insert tag after the list marker
        if line.strip().startswith("- "):
            new_line = line.replace("- ", f"- {tag} ", 1)
        elif line.strip().startswith("* "):
            new_line = line.replace("* ", f"* {tag} ", 1)
        else:
            new_line = f"{tag} {line}"

        if not dry_run:
            lines[line_idx] = new_line
        applied += 1

    if not dry_run and applied > 0:
        filepath.write_text("\n".join(lines), encoding="utf-8")

    if skipped_dupes > 0:
        print(f"  Skipped {skipped_dupes} duplicate entries (already in MEMORY.md)")

    return applied


def find_related(query: str, max_results: int = 10) -> list[dict]:
    """Find memories related to a query using n-gram similarity + type matching."""
    query_lower = query.lower()
    query_ngrams = char_ngrams(query_lower, 3)

    # Detect query type
    query_type, _ = classify_line(f"- {query}")

    memory_dir = WORKSPACE / "memory"
    files = [WORKSPACE / "MEMORY.md"]
    if memory_dir.exists():
        files.extend(f for f in memory_dir.glob("*.md")
                     if f.name != "archive" and not f.name.startswith("."))

    results = []
    seen = set()

    for filepath in files:
        if not filepath.exists():
            continue
        content = filepath.read_text(encoding="utf-8")
        for i, line in enumerate(content.split("\n"), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("```"):
                continue
            if not (stripped.startswith("- ") or stripped.startswith("* ")):
                continue

            # Skip exact duplicates
            line_key = stripped.lower()[:80]
            if line_key in seen:
                continue
            seen.add(line_key)

            # Calculate similarity
            line_ngrams = char_ngrams(stripped.lower(), 3)
            if not line_ngrams or not query_ngrams:
                continue
            overlap = len(query_ngrams & line_ngrams)
            sim = overlap / max(len(query_ngrams), len(line_ngrams))

            # Boost if same type
            line_type = detect_type(stripped)
            if query_type and line_type and query_type == line_type:
                sim = min(sim * 1.3, 1.0)

            if sim > 0.15:
                results.append({
                    "file": filepath.name,
                    "line": i,
                    "text": stripped[:200],
                    "similarity": round(sim, 3),
                    "type": line_type or "—",
                })

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:max_results]


def detect_type(line: str) -> str | None:
    """Detect memory type tag in a line."""
    m = TYPE_TAG_PATTERN.search(line)
    return m.group(1).upper() if m else None


def main():
    parser = argparse.ArgumentParser(description="Classify and tag memory entries")
    parser.add_argument("--file", type=Path, help="Specific file to analyze")
    parser.add_argument("--dry-run", action="store_true", help="Show suggestions without applying")
    parser.add_argument("--apply", action="store_true", help="Apply suggested tags")
    parser.add_argument("--min-confidence", type=float, default=0.3,
                        help="Minimum confidence threshold (default: 0.3)")
    parser.add_argument("--summary", action="store_true",
                        help="Show summary stats only, no per-line details")
    parser.add_argument("--related", type=str, metavar="QUERY",
                        help="Find memories related to QUERY")
    parser.add_argument("--top", type=int, default=10,
                        help="Max results for --related (default: 10)")
    args = parser.parse_args()

    # Related search mode
    if args.related:
        results = find_related(args.related, args.top)
        if not results:
            print(f"No related memories found for: \"{args.related}\"")
            return
        print(f"Related to: \"{args.related}\"\n")
        for r in results:
            print(f"  [{r['similarity']:.2f}] {r['file']}:{r['line']} [{r['type']}]")
            print(f"    {r['text']}")
            print()
        return

    # Determine files to process
    if args.file:
        files = [args.file]
    else:
        memory_dir = WORKSPACE / "memory"
        files = [WORKSPACE / "MEMORY.md"]
        if memory_dir.exists():
            files.extend(f for f in memory_dir.glob("*.md") if f.name != "archive")

    all_suggestions = []
    for filepath in files:
        if not filepath.exists():
            continue
        suggestions = analyze_file(filepath)
        suggestions = [s for s in suggestions if s["confidence"] >= args.min_confidence]
        all_suggestions.extend(suggestions)

        if suggestions:
            if not args.summary:
                print(f"\n--- {filepath} ---")
                for s in suggestions:
                    print(f"  L{s['line']}: [{s['suggested_type']}] (conf: {s['confidence']}) {s['content']}")

            if args.apply:
                count = apply_tags(filepath, suggestions, dry_run=False)
                if not args.summary:
                    print(f"  Applied {count} tags.")
            elif args.dry_run and not args.summary:
                print(f"  Would apply {len(suggestions)} tags.")

    if not all_suggestions:
        print("No untagged entries found. Memory is well-organized!")
    else:
        # Summary stats
        type_counts = {}
        for s in all_suggestions:
            t = s["suggested_type"]
            type_counts[t] = type_counts.get(t, 0) + 1

        if args.summary or not args.apply:
            print(f"\nTotal: {len(all_suggestions)} entries need classification.")
            print("By type:", ", ".join(f"[{t}]: {c}" for t, c in sorted(type_counts.items())))
            if not args.apply and not args.dry_run:
                print("Run with --apply to apply tags, or --dry-run to preview.")
        elif args.apply:
            print(f"\nApplied tags to {len(all_suggestions)} entries across {len(files)} files.")


if __name__ == "__main__":
    main()
