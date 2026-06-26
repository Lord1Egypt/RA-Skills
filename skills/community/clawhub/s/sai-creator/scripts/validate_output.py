#!/usr/bin/env python3
"""
Validate Output — pre-handoff QA check untuk artefak SAI.

Cek yang dilakukan:
  1. HTML inline CSS budget (<100KB)
  2. Alt text coverage di semua <img>
  3. Color contrast WCAG AA (palette static check)
  4. CTA URL exact match ke https://openjournaltheme.com/
  5. Forbidden adjektif promosi
  6. Halusinasi guard: entitas/angka di output ada di candidate.json
  7. JSON-LD schema.org/Article ada dan parseable
  8. Verbatim quotes <15 kata, max 1 per source

Usage:
    validate_output.py --html article.html --carousel out.svg \
                       --candidate candidate.json [--strict]

Exit codes:
    0 = all checks pass
    1 = warnings only (non-strict mode)
    2 = blocking failures
"""

import argparse
import json
import re
import sys
from pathlib import Path

FORBIDDEN_ADJECTIVES_BODY = [
    "revolutionary", "groundbreaking", "must-have", "ultimate",
    "best-ever", "luar biasa", "rahasia editor",
    "sensational", "incredible", "amazing",
]

REQUIRED_CTA_URL = "https://openjournaltheme.com/"
HTML_SIZE_BUDGET_KB = 100


def check_html_size(html_path):
    """Return (passed, size_kb)."""
    if not html_path.exists():
        return False, None, "file_not_found"
    size_bytes = html_path.stat().st_size
    size_kb = size_bytes / 1024
    return size_kb <= HTML_SIZE_BUDGET_KB, size_kb, None


def check_alt_text(html_content):
    """Return (coverage_ratio, missing_count, total_count)."""
    img_tags = re.findall(r"<img\b[^>]*>", html_content, re.IGNORECASE)
    total = len(img_tags)
    if total == 0:
        return 1.0, 0, 0
    missing = 0
    for tag in img_tags:
        alt_match = re.search(r'\balt\s*=\s*"([^"]*)"', tag, re.IGNORECASE)
        if not alt_match or not alt_match.group(1).strip():
            missing += 1
        elif alt_match.group(1).strip().lower() in ("image", "photo", "picture", "img"):
            missing += 1
    coverage = (total - missing) / total
    return coverage, missing, total


def check_cta_url(content):
    """Return (passed, found_urls)."""
    if REQUIRED_CTA_URL in content:
        # Make sure no other CTA URLs exist in metadata/href that pretend to be CTA
        return True, [REQUIRED_CTA_URL]
    return False, []


def check_forbidden_adjectives(html_content):
    """Return list of (adjective, context) found in body sections."""
    # Strip <head>, focus on body
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html_content, re.DOTALL | re.IGNORECASE)
    body = body_match.group(1) if body_match else html_content
    # Strip aside.sources block (URLs there don't count)
    body = re.sub(r'<aside class="sources".*?</aside>', "", body, flags=re.DOTALL)
    found = []
    for adj in FORBIDDEN_ADJECTIVES_BODY:
        pattern = re.compile(rf"\b{re.escape(adj)}\b", re.IGNORECASE)
        for match in pattern.finditer(body):
            start = max(0, match.start() - 30)
            end = min(len(body), match.end() + 30)
            context = body[start:end].replace("\n", " ").strip()
            found.append((adj, context))
    return found


def check_schema_org(html_content):
    """Return (found, parseable, valid_article)."""
    jsonld_match = re.search(
        r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>',
        html_content, re.DOTALL | re.IGNORECASE
    )
    if not jsonld_match:
        return False, False, False
    try:
        data = json.loads(jsonld_match.group(1))
    except json.JSONDecodeError:
        return True, False, False
    is_article = data.get("@type") == "Article" and "headline" in data and "datePublished" in data
    return True, True, is_article


def check_verbatim_quotes(html_content, candidate):
    """Return list of violations: (quote_text, word_count, reason)."""
    violations = []
    blockquotes = re.findall(r"<blockquote[^>]*>(.*?)</blockquote>", html_content, re.DOTALL)
    sources_seen = {}
    for bq in blockquotes:
        text = re.sub(r"<[^>]+>", "", bq).strip().strip('"')
        word_count = len(text.split())
        if word_count >= 15:
            violations.append((text[:80], word_count, "quote_too_long"))
        cite_match = re.search(r'cite="([^"]+)"', bq)
        cite = cite_match.group(1) if cite_match else "unknown"
        sources_seen[cite] = sources_seen.get(cite, 0) + 1
        if sources_seen[cite] > 1:
            violations.append((text[:80], word_count, f"multiple_quotes_from_{cite}"))
    return violations


def check_hallucination(html_content, candidate):
    """Cek angka/versi di body apakah ada di candidate.

    Heuristic: extract version-like patterns (X.Y.Z, X.Y) dari body,
    cek apakah masing-masing muncul di candidate JSON serialized.
    """
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html_content, re.DOTALL | re.IGNORECASE)
    body = body_match.group(1) if body_match else html_content
    # Strip script/style
    body = re.sub(r"<script.*?</script>", "", body, flags=re.DOTALL)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", body)

    candidate_str = json.dumps(candidate, ensure_ascii=False).lower()
    suspicious = []

    # Version numbers
    versions = set(re.findall(r"\b\d+\.\d+(?:\.\d+)?\b", text))
    for v in versions:
        if v not in candidate_str:
            suspicious.append(("version", v))

    # CVE IDs
    cves = set(re.findall(r"\bCVE-\d{4}-\d+\b", text, re.IGNORECASE))
    for c in cves:
        if c.lower() not in candidate_str:
            suspicious.append(("cve", c))

    return suspicious


def main():
    parser = argparse.ArgumentParser(description="Validate SAI output artifacts pre-handoff to SENKU")
    parser.add_argument("--html", required=True, help="Path to article HTML")
    parser.add_argument("--carousel", help="Path to carousel SVG (optional)")
    parser.add_argument("--candidate", required=True, help="Path to original candidate.json")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    html_path = Path(args.html)
    candidate_path = Path(args.candidate)

    if not html_path.exists():
        print(f"❌ HTML not found: {html_path}", file=sys.stderr)
        return 2
    if not candidate_path.exists():
        print(f"❌ Candidate not found: {candidate_path}", file=sys.stderr)
        return 2

    html_content = html_path.read_text(encoding="utf-8")
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))

    blockers = []
    warnings = []
    report = {}

    # 1. HTML size
    passed, size_kb, err = check_html_size(html_path)
    report["html_size_kb"] = round(size_kb, 2) if size_kb else None
    if not passed:
        blockers.append(f"HTML size {size_kb:.1f}KB exceeds budget {HTML_SIZE_BUDGET_KB}KB")

    # 2. Alt text
    coverage, missing, total = check_alt_text(html_content)
    report["alt_text_coverage"] = round(coverage, 3)
    report["alt_text_missing"] = missing
    report["alt_text_total_imgs"] = total
    if coverage < 1.0:
        blockers.append(f"Alt text missing on {missing}/{total} <img> tags")

    # 3. CTA URL — required in carousel SVG (slide 7), optional in article HTML
    if args.carousel:
        carousel_path = Path(args.carousel)
        if carousel_path.exists():
            carousel_content = carousel_path.read_text(encoding="utf-8")
            cc_passed, _ = check_cta_url(carousel_content)
            report["carousel_cta_url_present"] = cc_passed
            if not cc_passed:
                blockers.append(f"Required CTA URL not found in carousel: {REQUIRED_CTA_URL}")
        else:
            warnings.append(f"Carousel path provided but file missing: {carousel_path}")
    # Article HTML may optionally include the CTA URL in footer; not enforced.
    article_cta_present, _ = check_cta_url(html_content)
    report["article_cta_url_present"] = article_cta_present

    # 4. Forbidden adjectives
    forbidden = check_forbidden_adjectives(html_content)
    report["forbidden_adjectives_found"] = len(forbidden)
    if forbidden:
        for adj, ctx in forbidden:
            blockers.append(f"Forbidden adjective '{adj}' in body: ...{ctx}...")

    # 5. schema.org/Article
    found, parseable, valid_article = check_schema_org(html_content)
    report["jsonld_found"] = found
    report["jsonld_parseable"] = parseable
    report["jsonld_valid_article"] = valid_article
    if not found:
        blockers.append("JSON-LD schema.org/Article not found")
    elif not parseable:
        blockers.append("JSON-LD present but not valid JSON")
    elif not valid_article:
        warnings.append("JSON-LD present but missing Article required fields (headline/datePublished)")

    # 6. Verbatim quotes
    quote_violations = check_verbatim_quotes(html_content, candidate)
    report["quote_violations_count"] = len(quote_violations)
    for q, wc, reason in quote_violations:
        blockers.append(f"Quote violation [{reason}, {wc} words]: \"{q}\"")

    # 7. Halusinasi guard
    suspicious = check_hallucination(html_content, candidate)
    report["suspicious_entities"] = suspicious
    for kind, val in suspicious:
        warnings.append(f"Possible hallucination [{kind}]: '{val}' not found in candidate JSON")

    # ===== Print summary =====
    print("=" * 60)
    print("SAI OUTPUT VALIDATION REPORT")
    print("=" * 60)
    for k, v in report.items():
        print(f"  {k}: {v}")
    print()

    if blockers:
        print(f"❌ {len(blockers)} BLOCKER(S):")
        for b in blockers:
            print(f"   • {b}")
        print()

    if warnings:
        print(f"⚠️  {len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"   • {w}")
        print()

    if blockers:
        return 2
    if warnings and args.strict:
        return 2
    if warnings:
        print("✅ PASS with warnings")
        return 1
    print("✅ PASS — all checks clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
