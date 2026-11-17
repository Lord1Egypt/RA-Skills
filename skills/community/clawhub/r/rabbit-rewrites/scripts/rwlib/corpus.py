#!/usr/bin/env python3
"""
The README corpus figures readme_check.py compares against.

readme_check.py used to carry these as a literal dict with a comment promising
it mirrored docs/readme-analysis/03_aggregate_summary.json. Nothing checked the
promise, so regenerating the corpus silently orphaned the checker's thresholds:
the script kept quoting "corpus median 5" at a corpus whose median had moved.

Now there is a committed extract, skills/rabbit-readme-improver/scripts/corpus_summary.json,
which is what ships and what the checker reads. It is small enough that shipping
it costs nothing, and it keeps the skill working when installed without the
research data. `derive` is the function that produces it from the aggregate, so
the exporter and validate.py's drift check run the same code over the same
input and cannot disagree about what "mirrors" means.

Regenerate with:

    cd scripts/readme-research
    python3 03_analyze_readme.py --batch && python3 04_aggregate.py
    python3 05_export_corpus_summary.py

Stdlib only, 3.9+.
"""

import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# rwlib -> scripts -> rabbit-writes -> skills -> the plugin root. Walked rather
# than hardcoded, so the skill directory can be renamed without editing this.
PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
SUMMARY_PATH = os.path.join(PLUGIN_ROOT, "skills", "rabbit-readme-improver", "scripts",
                            "corpus_summary.json")
AGGREGATE_PATH = os.path.join(PLUGIN_ROOT, "docs", "readme-analysis",
                              "03_aggregate_summary.json")
REPOS_DIR = os.path.join(PLUGIN_ROOT, "docs", "readme-analysis", "repos")

# Bumped when `derive` changes which keys it emits or how it rounds them, so a
# committed extract from an older shape fails the drift check loudly instead of
# comparing unequal for a reason nobody can see.
#
# 2 adds measured_at.
SCHEMA_VERSION = 2

_CACHE = {}


def readme_paths(repos_dir=REPOS_DIR):
    """[(slug, path)] for the committed 100-README snapshot, or [] when it is
    not in this checkout.

    Here rather than in a test helper because both test suites need it now: the
    README suite has always used it, and the engine suite reaches for it the
    moment a detector has to be calibrated against real third-party documents,
    which `CLAUDE.md` requires of every new one. Two copies of the glob is how
    two halves of one plugin end up disagreeing about what the corpus is.

    Returns empty rather than raising. The snapshot is committed today and a
    consumer that hard-failed without it would make the corpus a build
    dependency, which it is not.
    """
    cache_key = ("readme_paths", repos_dir)
    if cache_key not in _CACHE:
        found = []
        if os.path.isdir(repos_dir):
            for slug in sorted(os.listdir(repos_dir)):
                hits = sorted(glob.glob(os.path.join(repos_dir, slug, "README.*")))
                preferred = [h for h in hits if h.lower().endswith(".md")]
                if preferred or hits:
                    found.append((slug, (preferred or hits)[0]))
        _CACHE[cache_key] = found
    return _CACHE[cache_key]


def derive(aggregate):
    """The subset of the aggregate that readme_check.py actually uses.

    Rounded here rather than at the point of use, because these numbers are
    quoted verbatim in findings ("Corpus median is 5") and a number that renders
    differently in two findings reads as two different measurements.
    """
    pos = aggregate["section_avg_relative_position"]
    lic = aggregate.get("section_median_word_count", {}).get("license", {})
    return {
        "schema_version": SCHEMA_VERSION,
        "n_repos": aggregate["n_repos"],
        # Carried through so the checker's report can date its own comparison.
        # These are a frozen snapshot skewed toward what was trending the week it
        # was taken, which the writeup says and the report did not: it just said
        # "100 trending repos", and a reader two years out had no way to tell.
        # None on an aggregate produced before the key existed, and the reporter
        # drops the clause rather than inventing a date.
        "measured_at": aggregate.get("measured_at"),
        "word_count_percentiles": dict(aggregate["readme_word_count_percentiles"]),
        "avg_paragraph_words": round(aggregate["avg_paragraph_words"], 1),
        "sentence_mix_pct": {
            "short": round(aggregate["avg_short_sentence_pct"], 1),
            "medium": round(aggregate["avg_medium_sentence_pct"], 1),
            "long": round(aggregate["avg_long_sentence_pct"], 1),
        },
        "median_badge_count": int(aggregate["median_badge_count"]),
        "link_style_pct": {
            "inline": aggregate["link_style_corpus_totals"]["pct_inline"],
            "bare": aggregate["link_style_corpus_totals"]["pct_bare_url"],
            "reference": aggregate["link_style_corpus_totals"]["pct_reference_style"],
        },
        "avg_link_text_words": round(aggregate["avg_link_text_words"], 1),
        "median_license_words": int(lic.get("median_words", 13)),
        "pct_has_installation_section": aggregate["pct_has_installation_section"],
        "pct_has_code_blocks": aggregate["pct_has_code_blocks"],
        "pct_has_license_section_or_badge": aggregate["pct_has_license_section_or_badge"],
        "pct_has_toc": aggregate["pct_has_toc"],
        "pct_has_toc_heading": aggregate.get("section_category_presence_pct", {}).get("toc", 12.0),
        "section_avg_position": {
            cat: v["avg_relative_position"] for cat, v in pos.items()
        },
    }


def load(path=SUMMARY_PATH):
    if path not in _CACHE:
        with open(path, encoding="utf-8") as fh:
            _CACHE[path] = json.load(fh)
    return _CACHE[path]


def load_aggregate(path=AGGREGATE_PATH):
    """The full research aggregate, or None when the study data is not installed."""
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def drift(summary_path=SUMMARY_PATH, aggregate_path=AGGREGATE_PATH):
    """[(key, shipped, derived)] where the committed extract has fallen behind.

    Empty when the research data is absent: an installed skill has no aggregate
    to compare against, and refusing to run would punish the common case for a
    check that only means something in this repo.
    """
    aggregate = load_aggregate(aggregate_path)
    if aggregate is None or not os.path.exists(summary_path):
        return []
    shipped = load(summary_path)
    derived = derive(aggregate)
    out = []
    for key in sorted(set(shipped) | set(derived)):
        if shipped.get(key) != derived.get(key):
            out.append((key, shipped.get(key), derived.get(key)))
    return out
