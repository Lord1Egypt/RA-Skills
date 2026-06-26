#!/usr/bin/env python3
import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional


DEFAULT_SOURCES = [
    Path.home() / ".openclaw" / "workspace" / ".learnings" / "FEATURE_REQUESTS.md",
    Path.home() / ".openclaw" / "workspace" / ".learnings" / "ERRORS.md",
    Path.home() / ".openclaw" / "workspace" / ".learnings" / "LEARNINGS.md",
]

STOPWORDS = {
    "the", "and", "for", "that", "with", "from", "this", "have", "your", "will",
    "when", "what", "into", "they", "them", "then", "than", "need", "help",
    "skill", "agent", "users", "user", "openclaw", "request",
    "task", "tasks", "ability", "capability",
    "requested", "context", "dedicated", "support", "summary", "suggested",
    "fix", "using", "same", "across", "repeated", "manual", "notes",
    "outputs", "created", "keeps", "add", "way", "section", "sections",
}

TEMPLATE_KEYWORDS = {
    "academic": {
        "citation", "bibliography", "references", "apa", "mla", "harvard",
        "chicago", "essay", "paper", "coursework", "assignment", "literature",
    },
    "product": {
        "prd", "mvp", "roadmap", "competitor", "onboarding", "feature",
        "requirements", "user-story", "acceptance", "pricing", "ux",
    },
    "integration": {
        "api", "oauth", "webhook", "token", "notion", "telegram", "github",
        "database", "sync", "connector", "credentials",
    },
    "script": {
        "export", "convert", "validate", "lint", "parse", "generate",
        "migration", "report", "batch", "cli",
    },
}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-{2,}", "-", value).strip("-")


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", text.lower())
    clean = []
    for word in words:
        if re.match(r"^(feat|err|lrn)-\d{8}", word):
            continue
        if word not in STOPWORDS:
            clean.append(word)
    return clean


def read_sources(paths: list[Path]) -> dict[str, str]:
    result = {}
    for path in paths:
        if path.exists() and path.is_file():
            result[str(path)] = path.read_text(encoding="utf-8", errors="ignore")
    return result


def extract_sections(text: str) -> list[str]:
    sections = re.split(r"\n##\s+", "\n" + text)
    return [section.strip() for section in sections if section.strip()]


def explicit_skill_name(section: str) -> Optional[str]:
    first_line = section.splitlines()[0] if section.splitlines() else ""
    match = re.search(r"\]\s+([a-zA-Z][a-zA-Z0-9_-]{2,})", first_line)
    if match:
        return slugify(match.group(1))
    return None


def infer_template(tokens: list[str]) -> str:
    scores = {}
    token_set = set(tokens)
    for template, keywords in TEMPLATE_KEYWORDS.items():
        scores[template] = len(token_set & keywords)
    best = max(scores.items(), key=lambda item: item[1])
    return best[0] if best[1] else "workflow"


def pick_triggers(tokens: list[str], limit: int = 8) -> list[str]:
    counts = Counter(tokens)
    triggers = []
    for word, _ in counts.most_common():
        if word not in triggers:
            triggers.append(word)
        if len(triggers) >= limit:
            break
    return triggers


def detect_opportunities(contents: dict[str, str], top_n: int = 8) -> list[dict]:
    candidates: dict[str, dict] = {}
    keyword_counter = Counter()
    keyword_evidence = defaultdict(list)

    for source, text in contents.items():
        for section in extract_sections(text):
            tokens = tokenize(section)
            if not tokens:
                continue

            snippet = " ".join(section.split())[:240]
            explicit = explicit_skill_name(section)
            local_terms = Counter(tokens)

            if explicit:
                item = candidates.setdefault(
                    explicit,
                    {
                        "suggested_skill_name": explicit,
                        "score": 0,
                        "evidence": [],
                        "tokens": [],
                    },
                )
                item["score"] += 6 + len(set(tokens[:12])) // 3
                item["tokens"].extend(tokens)
                if len(item["evidence"]) < 4:
                    item["evidence"].append({"source": source, "snippet": snippet})

            for token, count in local_terms.items():
                keyword_counter[token] += count
                if len(keyword_evidence[token]) < 3:
                    keyword_evidence[token].append({"source": source, "snippet": snippet})

    for token, score in keyword_counter.items():
        if score < 2:
            continue
        name = slugify(token)
        item = candidates.setdefault(
            name,
            {
                "suggested_skill_name": name,
                "score": 0,
                "evidence": [],
                "tokens": [],
            },
        )
        item["score"] += score
        item["tokens"].extend([token] * score)
        item["evidence"].extend(keyword_evidence[token])
        item["evidence"] = item["evidence"][:4]

    opportunities = []
    for item in candidates.values():
        tokens = item.pop("tokens")
        template = infer_template(tokens + [item["suggested_skill_name"]])
        triggers = pick_triggers(tokens)
        confidence = min(0.95, 0.35 + item["score"] / 20)
        opportunities.append(
            {
                **item,
                "recommended_template": template,
                "confidence": round(confidence, 2),
                "triggers": triggers,
                "reason": (
                    f"Recurring {template} capability pattern detected for "
                    f"'{item['suggested_skill_name']}'."
                ),
            }
        )

    opportunities.sort(key=lambda item: (item["score"], item["confidence"]), reverse=True)
    return opportunities[:top_n]


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect recurring skill opportunities from learnings/logs.")
    parser.add_argument("--source", action="append", default=[], help="Source markdown/text file.")
    parser.add_argument("--top", type=int, default=8, help="Number of opportunities to return.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    paths = [Path(p).expanduser() for p in args.source] or DEFAULT_SOURCES
    contents = read_sources(paths)
    opportunities = detect_opportunities(contents, top_n=args.top)
    payload = {"sources_read": list(contents.keys()), "opportunities": opportunities}

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print("Skill opportunities")
    print()
    for item in opportunities:
        print(
            f"- {item['suggested_skill_name']} "
            f"template={item['recommended_template']} score={item['score']} "
            f"confidence={item['confidence']}"
        )
        print(f"  reason: {item['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
