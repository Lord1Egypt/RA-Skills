#!/usr/bin/env python3
"""
resume-story-spinr — turn flat resume bullets into STAR-method achievement
narratives that survive ATS filters and human skim-reads.

Subcommands: transform | ats | interview | demo

What it does:
  * TRANSFORM: "Responsible for payments API" →
    "Owned payments API serving 2.1M req/day; cut p99 latency 38% by
    introducing request batching — adopted as the team's default pattern"
    (Situation-Task-Action-Result, strong verb, quantified outcome)
  * ATS: score a resume (or bullet list) against a job description —
    keyword coverage, weak-phrase detection, formatting hazards
  * INTERVIEW: expand each bullet into the STAR story + likely follow-up
    questions, so the resume and the interview tell the same story

Runs offline, stdlib only. No LLM inside — this is the *structure* engine;
an agent (you) supplies the wording using the generated skeletons.
"""
import argparse
import json
import re
import sys

try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass

# ── Verb library: weak → strong replacements ────────────────────────────────
WEAK_OPENERS = {
    "responsible for": "Owned",
    "helped with": "Drove",
    "helped": "Drove",
    "worked on": "Built",
    "worked with": "Partnered with",
    "assisted with": "Delivered",
    "assisted in": "Delivered",
    "assisted": "Delivered",
    "involved in": "Drove",
    "participated in": "Contributed to",
    "was part of": "Contributed to",
    "tasked with": "Led",
    "duties included": "Delivered",
    "handled": "Managed",
    "did": "Executed",
    "made": "Built",
    "used": "Leveraged",
}

# Phrases that add zero information (resume "stop-words")
FILLER_PHRASE = [
    "hard worker", "team player", "detail oriented", "detail-oriented",
    "go-getter", "think outside the box", "results-driven", "self-starter",
    "excellent communication skills", "responsible for various",
    "various tasks", "as needed", "etc.", "and more", "familiar with",
]

WEAK_VERBS = ["was", "were", "is", "are", "been", "being", "had"]


# Gerunds → past-tense verbs, so "Worked on improving X" → "Improved X"
GERUND_FIX = {
    "improving": "Improved", "building": "Built", "migrating": "Migrated",
    "creating": "Created", "developing": "Developed", "managing": "Managed",
    "maintaining": "Maintained", "supporting": "Supported",
    "optimizing": "Optimized", "automating": "Automated",
    "testing": "Tested", "writing": "Wrote", "designing": "Designed",
    "implementing": "Implemented", "reducing": "Reduced",
    "increasing": "Increased", "streamlining": "Streamlined",
    "refactoring": "Refactored", "monitoring": "Monitored",
}


def title_case_verb(verb):
    return verb[0].upper() + verb[1:]


def strengthen_opener(text):
    """Replace weak openers with strong verbs; return (text, changed)."""
    lower = text.lstrip().lower()
    for weak, strong in WEAK_OPENERS.items():
        if lower.startswith(weak):
            rest = text.lstrip()[len(weak):].lstrip(" ,")
            # "Worked on improving X" → "Improved X" (gerund → past tense)
            first_word = rest.split(" ", 1)[0].lower() if rest else ""
            if first_word in GERUND_FIX:
                replacement = GERUND_FIX[first_word]
                rest_tail = rest.split(" ", 1)[1] if " " in rest else ""
                rest = (replacement + " " + rest_tail).strip() if rest_tail else replacement
                return rest, True
            return title_case_verb(strong) + (" " + rest if rest else ""), True
    return text, False


# ── Quantification detector ─────────────────────────────────────────────────
NUM_RE = re.compile(
    r"(?:[$€£]\s?\d[\d,.]*"
    r"|\d+(?:[.,]\d+)?\s*(?:%|percent|min\b|sec\b|ms\b|hrs?\b|hours?\b|days?\b|"
    r"weeks?\b|months?\b|years?\b|users?\b|customers?\b|clients?\b|requests?\b|"
    r"req/s|tickets?\b|engineers?\b|people\b|reports?\b|members?\b|teams?\b|"
    r"services?\b|systems?\b|k\b|m\b|x\b)"
    r"|\b\d+(?:\.\d+)?(?:k|m)\b"
    r"|\d+(?:,\d{3})+"
    r"|\b\d{2,}\b)",
    re.IGNORECASE)


def has_metrics(text):
    return bool(NUM_RE.search(text))


def metric_hint(text):
    """Suggest what to measure when a bullet lacks numbers."""
    dom = {
        "api": ["requests/sec served", "p95/p99 latency change", "error-rate delta"],
        "test": ["coverage % before→after", "flake rate", "escaped-bug count"],
        "lead": ["team size", "projects shipped/quarter", "cycle-time delta"],
        "migration": ["downtime", "systems migrated", "cost delta/month"],
        "design": ["adoption %", "task-completion time delta", "support tickets drop"],
        "sales": ["deal size", "win-rate delta", "pipeline $ created"],
        "support": ["tickets/day", "CSAT delta", "first-response time"],
        "cost": ["$ saved/yr", "% reduction"],
    }
    t = text.lower()
    hints = []
    for kw, hs in dom.items():
        if kw in t:
            hints.extend(hs)
    if not hints:
        hints = ["how many / how much / how often / % or time delta"]
    return hints[:3]


# ── STAR transform ──────────────────────────────────────────────────────────
def bullet_to_star(bullet, metrics=""):
    """Return STAR-structured dict for one bullet."""
    strengthened, changed = strengthen_opener(bullet.strip())
    star = {
        "original": bullet.strip(),
        "strengthened": strengthened,
        "verb_changed": changed,
        "quantified": has_metrics(strengthened) or bool(metrics),
        "s": None, "t": None, "a": None, "r": None,
    }

    # Heuristic split on common separators: ; because / which resulted in
    parts = re.split(r"\s*[;–—]\s*|\s+(?:which|resulting in|leading to|reducing)\s+",
                     strengthened, flags=re.IGNORECASE)
    star["a"] = parts[0].rstrip(".")
    if len(parts) > 1:
        star["r"] = parts[1].rstrip(".")
    if metrics:
        star["r"] = (star["r"] + f"; {metrics}" if star["r"] else metrics).rstrip(".; ")

    if not star["quantified"]:
        star["metric_hints"] = metric_hint(strengthened)
    return star


def render_star(star, style="resume"):
    """Render a STAR dict back to text. style: resume | story"""
    a = star["a"] or star["strengthened"]
    r = star["r"]
    if style == "resume":
        out = a
        if r:
            out += f" — {r}"
        return out.rstrip(".; ") + "."
    # story style
    s = star.get("s") or "[Set the scene: team size, system scale, why it mattered]"
    return (f"S: {s}\n"
            f"T: [What specifically had to be true at the end]\n"
            f"A: {a}\n"
            f"R: {r or '[Measured outcome — add a number]'}")


def followup_questions(star):
    """Interview questions an interviewer derives from this bullet."""
    qs = ["What was YOUR specific contribution vs the team's?"]
    if star.get("quantified"):
        qs.append("How did you measure that number? Walk me through the method.")
        qs.append("What would have happened if you hadn't done this?")
    else:
        qs.append("Can you put a number on the impact — time, money, users?")
    a = (star.get("a") or "").lower()
    if "led" in a or "owned" in a:
        qs.append("How did you handle disagreement within the team?")
    if "migration" in a or "rewrite" in a:
        qs.append("What went wrong? What would you do differently?")
    if "cut" in a or "reduced" in a or "improv" in a:
        qs.append("What was the baseline, and how did you establish it?")
    return qs[:5]


# ── ATS scoring ─────────────────────────────────────────────────────────────
def ats_score(resume_text, job_text):
    """Keyword-coverage + hazard scoring of resume vs job description."""
    STOP = {"the", "and", "for", "with", "you", "our", "will", "are", "have",
            "your", "who", "that", "this", "a", "an", "in", "to", "of", "on",
            "looking", "seeking", "join", "hire", "role", "position",
            "candidate", "experience", "years", "work", "working", "strong",
            "great", "good", "must", "plus", "etc", "us", "we", "team"}

    def tokens(t):
        raw = re.findall(r"[a-z][a-z+#.0-9]*", t.lower())
        return set(w.rstrip(".") for w in raw if w not in STOP and len(w) > 2)

    jt, rt = tokens(job_text), tokens(resume_text)
    if not jt:
        return {"error": "no job description tokens"}

    covered = jt & rt
    missing = jt - rt

    score = round(100 * len(covered) / len(jt))

    bullets = [b for b in resume_text.splitlines() if b.strip()]
    hazards = []
    weak_count = 0
    for b in bullets:
        low = b.lower()
        if any(low.startswith(w) for w in WEAK_OPENERS):
            weak_count += 1
        for ph in FILLER_PHRASE:
            if ph in low:
                hazards.append(f"filler phrase: '{ph}'")

    # formatting hazards (sections typically mangled by ATS parsers)
    if re.search(r"\t", resume_text):
        hazards.append("tab characters (use single-column, spaces)")
    if re.search(r"^\s*•", resume_text, re.M) or "●" in resume_text:
        hazards.append("fancy bullets (use plain '-')")
    if re.search(r"\btable(s)?\b", resume_text, re.I):
        pass  # can't detect tables from text; skip

    return {
        "match_score": score,
        "job_terms": len(jt),
        "covered": sorted(covered),
        "missing": sorted(missing),
        "weak_openers": weak_count,
        "filler_hazards": hazards,
        "bullets_analyzed": len(bullets),
    }


# ── CLI renderers ───────────────────────────────────────────────────────────
def run_transform(args):
    bullets = [b for b in (args.bullets or []).strip().splitlines() if b.strip()]
    if args.file:
        bullets = [b for b in open(args.file).read().splitlines() if b.strip()]
    if not bullets:
        print("no input bullets (use --bullets or --file)")
        return 1
    print(f"STAR TRANSFORM — {len(bullets)} bullet(s)")
    print("=" * 66)
    weak_total = 0
    unquant_total = 0
    for i, b in enumerate(bullets, 1):
        star = bullet_to_star(b, metrics=args.metrics or "")
        if star["verb_changed"]:
            weak_total += 1
        print(f"\n[{i}] BEFORE: {star['original']}")
        print(f"    AFTER:  {render_star(star, 'resume')}")
        if not star["quantified"]:
            unquant_total += 1
            print(f"    ⚠ No metric — add: {', '.join(star.get('metric_hints', []))}")
        print(f"    Interview follow-up: {followup_questions(star)[0]}")
    print()
    print(f"Summary: {len(bullets)} bullets, {weak_total} weak openers fixed, "
          f"{unquant_total} missing metrics")
    if unquant_total:
        print("Rule: every bullet needs a number. 'Improved performance' is")
        print("invisible; 'cut p99 38%' is an interview story.")
    return 0


def run_ats(args):
    resume = open(args.resume).read() if args.resume else sys.stdin.read()
    job = open(args.job).read() if args.job else sys.stdin.read()
    r = ats_score(resume, job)
    if "error" in r:
        print(r["error"]); return 1
    print("ATS MATCH REPORT")
    print("=" * 66)
    print(f"  Keyword coverage: {r['match_score']}%  "
          f"({len(r['covered'])}/{r['job_terms']} job terms found)")
    bar = "█" * (r["match_score"] // 5) + "░" * (20 - r["match_score"] // 5)
    print(f"  [{bar}]")
    if r["missing"]:
        print(f"\n  Missing from resume ({len(r['missing'])}):")
        for m in r["missing"][:20]:
            print(f"    - {m}")
    if r["weak_openers"]:
        print(f"\n  ⚠ {r['weak_openers']} bullet(s) start with weak openers")
        print("    (responsible for / worked on / helped …) — run transform")
    if r["filler_hazards"]:
        print(f"\n  ⚠ Filler phrases detected:")
        for h in r["filler_hazards"][:10]:
            print(f"    - {h}")
    print(f"\n  Note: 60-75% coverage is typical for a well-matched resume.")
    print("  100% is a red flag (keyword stuffing); mirror the JD's core")
    print("  terms in *true* statements only.")
    return 0


def run_interview(args):
    bullets = []
    if args.file:
        bullets = [b for b in open(args.file).read().splitlines() if b.strip()]
    elif args.bullet:
        bullets = [args.bullet]
    if not bullets:
        print("no bullet (use --bullet or --file)")
        return 1
    for b in bullets:
        star = bullet_to_star(b)
        print(f"BULLET: {star['original']}")
        print(render_star(star, "story"))
        print("  Likely follow-ups:")
        for q in followup_questions(star):
            print(f"   ? {q}")
        print()
    return 0


def run_demo(args):
    print("=== DEMO 1: weak → strong ===")
    for b in [
        "Responsible for the payments API",
        "Helped with migration of legacy services to Kubernetes",
        "Worked on improving test coverage",
    ]:
        star = bullet_to_star(b)
        print(f"  BEFORE: {star['original']}")
        print(f"  AFTER:  {render_star(star, 'resume')}")
        print()
    print("=== DEMO 2: quantified bullet → interview story ===")
    star = bullet_to_star(
        "Led migration of 14 services to Kubernetes; cut deploy time from 40min to 6min")
    print(f"  A: {star['a']}")
    print(f"  R: {star['r']}")
    print("  Follow-ups:")
    for q in followup_questions(star):
        print(f"   ? {q}")
    print()
    print("=== DEMO 3: ATS coverage ===")
    resume = """Senior Backend Engineer
- Owned payments API serving 2.1M requests/day
- Led migration of 14 services to Kubernetes; deploy time 40min→6min
- Cut p99 latency 38% via request batching and connection pooling
- Mentor 3 junior engineers; introduced pair-review rotation"""
    job = """Looking for: backend engineer with Kubernetes, Go, PostgreSQL,
gRPC, observability (Prometheus), CI/CD, on-call experience, mentoring."""
    rep = ats_score(resume, job)
    print(f"  Coverage: {rep['match_score']}% "
          f"({len(rep['covered'])}/{rep['job_terms']} terms)")
    print(f"  Missing: {', '.join(rep['missing'][:8]) or 'none'}")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")

    t = sub.add_parser("transform", help="bullets → STAR achievements")
    t.add_argument("--bullets", help="newline-separated bullets")
    t.add_argument("--file", help="file with one bullet per line")
    t.add_argument("--metrics", default="", help="extra metric to append")

    a = sub.add_parser("ats", help="score resume vs job description")
    a.add_argument("--resume", required=True)
    a.add_argument("--job", required=True)

    i = sub.add_parser("interview", help="expand bullet into STAR story + Qs")
    i.add_argument("--bullet", help="single bullet")
    i.add_argument("--file", help="file with one bullet per line")

    sub.add_parser("demo")

    args = p.parse_args()
    handlers = {"transform": run_transform, "ats": run_ats,
                "interview": run_interview, "demo": run_demo}
    if args.cmd in handlers:
        return handlers[args.cmd](args) or 0
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
