#!/usr/bin/env python3
import argparse
import json
import sys

MANDATORY_CORE = [
    ("web-scraper", "Verify source pages, extract claims, and capture current details."),
    ("self-improvement", "Run a lightweight quality check on the approach."),
    ("supermemory", "Recall prior decisions, preferences, and related context."),
    ("brainstorming", "Clarify the angle, compare approaches, and tighten the question."),
    ("zo-research-topic", "Do the general research and synthesis layer."),
    ("market-research", "Pull market, industry, and quantitative context when relevant."),
]

DOMAIN_RULES = [
    ("seo-audit", ["seo", "rank", "ranking", "crawl", "index", "organic", "traffic", "technical seo"]),
    ("marketing-psychology", ["psychology", "persuasion", "bias", "behaviour", "behavior", "decision", "framing", "mental model"]),
    ("marketing-ideas", ["marketing", "growth", "acquisition", "campaign", "channel", "promotion"]),
    ("pricing-strategy", ["pricing", "tier", "tiers", "package", "packaging", "freemium", "willingness to pay", "monetization", "monetisation"]),
    ("free-tool-strategy", ["tool", "calculator", "generator", "lead gen", "leadgen", "engineering as marketing", "free tool"]),
    ("launch-strategy", ["launch", "beta", "product hunt", "early access", "waitlist", "announcement", "rollout"]),
    ("zo-daily-news-digest", ["news digest", "daily news", "headlines", "current news", "digest"]),
    ("competitor-alternatives", ["alternative", "alternatives", " vs ", "compare", "comparison", "competitor"]),
    ("analytics-tracking", ["analytics", "tracking", "ga4", "gtm", "conversion", "event", "measurement", "attribution"]),
    ("programmatic-seo", ["programmatic seo", "template pages", "directory pages", "location pages", "pages at scale", "comparison pages"]),
]

WEB_NEEDLES = ["http://", "https://", "www.", "source", "sources", "quote", "current", "latest", "fresh", "verify", "website", "page", "pages"]


def normalise(text: str) -> str:
    return " ".join(text.strip().lower().split())


def needs_clarification(query: str) -> bool:
    words = [w for w in query.split() if w]
    if len(words) <= 3:
        return True
    vague = {"help", "idea", "research", "future", "best", "topic", "language", "strategy"}
    return normalise(query) in vague


def classify(query: str):
    q = normalise(query)
    skills = []
    seen = set()

    for name, _ in MANDATORY_CORE:
        if name not in seen:
            skills.append(name)
            seen.add(name)

    if any(token in q for token in WEB_NEEDLES) and "web-scraper" not in seen:
        skills.append("web-scraper")
        seen.add("web-scraper")

    for name, needles in DOMAIN_RULES:
        if any(needle in q for needle in needles) and name not in seen:
            skills.append(name)
            seen.add(name)

    if "web-scraper" not in seen and any(token in q for token in ["evidence", "source", "sources", "verify", "citation"]):
        skills.append("web-scraper")
        seen.add("web-scraper")

    question_breakdown = [f"Main ask: {query.strip()}"]
    if needs_clarification(query):
        question_breakdown.append("Ambiguity: the prompt is too broad to route with high confidence.")

    evidence = [
        "Use `web-scraper` to verify source pages, extract claims, and capture current details.",
        "Use `supermemory` to recover prior decisions and preferences before making assumptions.",
    ]
    if "market-research" in skills:
        evidence.append("Use `market-research` for industry and quantitative context.")

    next_steps = ["Ask one clarifying question and wait."] if needs_clarification(query) else ["Run the routing stack, then synthesise once."]

    return {
        "query": query.strip(),
        "needs_clarification": needs_clarification(query),
        "clarifying_question": "What angle do you want: prediction, comparison, decision support, or a general overview?" if needs_clarification(query) else "",
        "question_breakdown": question_breakdown,
        "skills_used": skills,
        "evidence": evidence,
        "recommendation": "Use the minimum necessary specialist skills, then merge the results into one structured answer.",
        "next_steps": next_steps,
    }


def render_text(plan):
    lines = []
    lines.append("Question breakdown")
    for item in plan["question_breakdown"]:
        lines.append(f"- {item}")
    if plan["needs_clarification"]:
        lines.append("")
        lines.append("Clarifying question")
        lines.append(f"- {plan['clarifying_question']}")
    lines.append("")
    lines.append("Skills used")
    for skill in plan["skills_used"]:
        lines.append(f"- {skill}")
    lines.append("")
    lines.append("Evidence")
    for item in plan["evidence"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Recommendation")
    lines.append(f"- {plan['recommendation']}")
    lines.append("")
    lines.append("Next steps")
    for item in plan["next_steps"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Deterministic routing helper for Ultimate Research")
    parser.add_argument("query", nargs="*", help="User query to route")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    query = " ".join(args.query).strip()
    if not query and not sys.stdin.isatty():
        query = sys.stdin.read().strip()
    if not query:
        print("Provide a query.", file=sys.stderr)
        sys.exit(1)

    plan = classify(query)
    if args.json:
        print(json.dumps(plan, indent=2, ensure_ascii=False))
    else:
        print(render_text(plan))


if __name__ == "__main__":
    main()
