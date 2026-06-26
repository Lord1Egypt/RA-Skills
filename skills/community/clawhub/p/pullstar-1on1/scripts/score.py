"""
score.py — Deterministic scoring engine for PullStar 1-on-1

Usage:
    python scripts/score.py --login jsmith
    python scripts/score.py --login jsmith --input-dir .pullstar --output-dir .pullstar

Phase 2: All 5 dimensions. No AI calls. Pure computation. Max score = 100.
"""

import argparse
import json
import math
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fail(msg: str) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def as_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def parse_dt(iso: str) -> datetime:
    return as_utc(datetime.fromisoformat(iso))


def clamp(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def pr_confidence(n: int) -> str:
    """Confidence tier based on number of data points."""
    if n >= 8:
        return "high"
    if n >= 4:
        return "medium"
    return "low"


def _merge_time_phrase(avg_days: float) -> str:
    """Human-readable merge time. Avoids raw decimals like '0.1 days'."""
    if avg_days < 1:
        return "Typically merged same day"
    if avg_days < 2:
        return "Typically merged within a day or two"
    return f"Avg {avg_days:.0f} days from open to merge"


def _insights_summary(prs_with_insights: list) -> dict:
    """
    Aggregate PR insight detail (embedded in prs_authored entries) into scoring stats.
    Expects entries that have discussion_summary_stats and reviews_received_detail.
    Returns empty dict when list is empty.

    Fields returned:
      n                  — number of PRs with insights
      revised_count      — PRs where an approval followed a changes_requested
      cr_count           — PRs that received at least one changes_requested review
      avg_review_comments — avg review objects received per PR
      avg_reviewers      — avg unique reviewer count per PR
      prs_with_any_review — count of PRs that received at least one review
      prs_with_approved  — count of PRs that received at least one approval
      prs_with_discussion — count of PRs with at least one substantive body (>50 chars)
                            in reviews or issue comments
    """
    if not prs_with_insights:
        return {}
    n = len(prs_with_insights)
    revised_count       = 0
    cr_count            = 0
    total_rev_comments  = 0
    total_reviewers     = 0
    prs_with_any_review = 0
    prs_with_approved   = 0
    prs_with_discussion = 0

    for p in prs_with_insights:
        stats    = p.get("discussion_summary_stats", {})
        detail   = p.get("reviews_received_detail", [])
        comments = p.get("comments_detail", [])

        if stats.get("changes_requested_count", 0) > 0:
            cr_count += 1
        if stats.get("review_count", 0) > 0:
            prs_with_any_review += 1
        if stats.get("approved_count", 0) > 0:
            prs_with_approved += 1

        total_rev_comments += stats.get("review_count", 0)

        reviewer_logins = {r["reviewer_login"] for r in detail if r.get("reviewer_login")}
        total_reviewers += len(reviewer_logins)

        # Substantive discussion: any review or comment body longer than 50 chars
        has_discussion = (
            any(r.get("body_length", 0) > 50 for r in detail)
            or any(c.get("body_length", 0) > 50 for c in comments)
        )
        if has_discussion:
            prs_with_discussion += 1

        # was_revised: approved follows changes_requested in submission order
        pending_cr = False
        for r in detail:
            if r["state"] == "changes_requested":
                pending_cr = True
            elif r["state"] == "approved" and pending_cr:
                revised_count += 1
                break

    return {
        "n":                   n,
        "revised_count":       revised_count,
        "cr_count":            cr_count,
        "avg_review_comments": total_rev_comments / n,
        "avg_reviewers":       total_reviewers / n,
        "prs_with_any_review": prs_with_any_review,
        "prs_with_approved":   prs_with_approved,
        "prs_with_discussion": prs_with_discussion,
    }


# ---------------------------------------------------------------------------
# Dimension 1: Velocity (max 20)
# ---------------------------------------------------------------------------
# Base:    >=4 merged -> 12 | 2-3 -> 8 | 1 -> 4 | 0 -> 0
# Bonus:   avg merge time < 3 days -> +4
# Bonus:   PRs across >=2 repos -> +4
# Penalty: >3 open PRs stale >7 days -> -4
# Cap:     0-20
#
# Signals answer: How much shipped? How fast did things move?
# Flags:   stale open PRs only (gaps are handled by consistency)

def score_velocity(prs: list, lookback_days: int, ingested_at: datetime) -> tuple[dict, list]:
    merged = [p for p in prs if p["status"] == "merged"]
    n_merged = len(merged)
    n_total = len(prs)

    if n_merged >= 4:
        score = 12
    elif n_merged >= 2:
        score = 8
    elif n_merged == 1:
        score = 4
    else:
        score = 0

    # Signal 1: volume, with rate context when window is long enough
    if n_merged >= 4 and lookback_days >= 14:
        rate = lookback_days / n_merged
        day_word = "day" if round(rate) == 1 else "days"
        signals = [f"{n_merged} PRs merged — one every {rate:.0f} {day_word} on average"]
    else:
        signals = [f"{n_merged} PR{'s' if n_merged != 1 else ''} merged in {lookback_days} days"]

    dim_flags = []
    top_flags = []

    # Bonus + signal 2: merge speed
    merge_times = []
    for pr in merged:
        if pr["created_at"] and pr["merged_at"]:
            delta = (parse_dt(pr["merged_at"]) - parse_dt(pr["created_at"])).total_seconds() / 86400
            merge_times.append(delta)

    if merge_times:
        avg_merge = sum(merge_times) / len(merge_times)
        if avg_merge < 3:
            score += 4
        signals.append(_merge_time_phrase(avg_merge))

    # Bonus + signal 3: cross-repo work
    repos = {p["repository"] for p in prs}
    if len(repos) >= 2:
        score += 4
        if len(signals) < 3:
            signals.append(f"Work spans {len(repos)} repos")

    # Penalty + flag: stale open PRs
    stale = sum(
        1 for p in prs
        if p["status"] == "open"
        and (ingested_at - parse_dt(p["created_at"])).total_seconds() / 86400 > 7
    )
    if stale > 3:
        score -= 4
        msg = f"{stale} PRs have been open for over a week with no merge"
        dim_flags.append(msg)
        top_flags.append({"severity": "caution", "dimension": "velocity", "message": msg})

    return {
        "score": clamp(score, 0, 20),
        "max": 20,
        "confidence": pr_confidence(n_total),
        "signals": signals[:3],
        "flags": dim_flags[:2],
    }, top_flags


# ---------------------------------------------------------------------------
# Dimension 2: PR Quality (max 20)
# ---------------------------------------------------------------------------
# Size:        avg <=200 lines -> 8 | 201-500 -> 5 | >500 -> 2
# Description: >=70% have >50 chars -> 6 | 30-69% -> 3 | <30% -> 0
# Labels:      >=50% have labels -> 3
# Commits:     avg <=5 commits/PR -> 3
# Cap:         0-20
#
# Signals answer: Are PRs well-scoped? Well-documented?
# Signal order: size -> descriptions -> labels or commits (whichever is more notable)

def score_pr_quality(prs: list, insights_summary: dict | None = None) -> tuple[dict, list]:
    if not prs:
        return {
            "score": 0,
            "max": 20,
            "confidence": "low",
            "signals": ["No PRs in window"],
            "flags": [],
        }, []

    n = len(prs)
    score = 0
    signals = []
    dim_flags = []
    top_flags = []

    # Signal 1: size with plain-language label
    sizes = [p["lines_added"] + p["lines_deleted"] for p in prs]
    avg_size = sum(sizes) / n
    if avg_size <= 200:
        score += 8
        signals.append(f"Focused PRs — avg {avg_size:.0f} lines changed")
    elif avg_size <= 500:
        score += 5
        signals.append(f"Mid-sized PRs — avg {avg_size:.0f} lines changed")
    else:
        score += 2
        signals.append(f"Large PRs on average — {avg_size:.0f} lines changed")

    # Flag: large PRs — count them, don't just say "one or more"
    large_prs = [s for s in sizes if s > 1000]
    if large_prs:
        count = len(large_prs)
        msg = (
            f"{count} PR{'s' if count > 1 else ''} exceeded 1000 lines "
            f"— worth discussing scope or decomposition"
        )
        dim_flags.append(msg)
        top_flags.append({"severity": "caution", "dimension": "pr_quality", "message": msg})

    # Signal 2: descriptions — use count, not just percent
    with_desc = sum(1 for p in prs if p["description_length"] > 50)
    desc_pct = with_desc / n
    if desc_pct >= 0.70:
        score += 6
        signals.append(f"Descriptions on {with_desc} of {n} PRs — good context for reviewers")
    elif desc_pct >= 0.30:
        score += 3
        signals.append(f"Descriptions on {with_desc} of {n} PRs — inconsistent coverage")
    else:
        signals.append(f"Only {with_desc} of {n} PRs include a description")

    # Labels points
    with_labels = sum(1 for p in prs if p["label_names"])
    if with_labels / n >= 0.50:
        score += 3

    # Commit focus points
    avg_commits = sum(p["commit_count"] for p in prs) / n
    if avg_commits <= 5:
        score += 3

    # Signal 3: pick the most notable of labels or commits
    if avg_commits > 8:
        signals.append(f"High commit count — avg {avg_commits:.0f} commits per PR")
    elif with_labels / n >= 0.50 and len(signals) < 3:
        signals.append(f"{with_labels} of {n} PRs are labeled")

    # Flag: most PRs target non-default branches
    non_main = sum(1 for p in prs if p["base_branch"] not in ("main", "master", "trunk", "develop"))
    if non_main / n > 0.50:
        msg = "Most PRs target feature branches rather than main — check if this is intentional"
        dim_flags.append(msg)
        top_flags.append({"severity": "info", "dimension": "pr_quality", "message": msg})

    # Insights enrichment (additive — only when --pr_insights data is present)
    ins = insights_summary or {}
    if ins:
        n_ins         = ins["n"]
        revised       = ins["revised_count"]
        cr            = ins["cr_count"]
        prs_with_disc = ins.get("prs_with_discussion", 0)

        # Score boost: modest reward for responsive revision pattern.
        # Only applies when >=1 PR was revised and the majority of CRed PRs got revised.
        if revised >= 1 and cr >= 1 and (revised / cr) >= 0.5:
            score += 2

        # Signal (slot 3 if free): revision pattern or discussion presence
        if len(signals) < 3:
            if revised > 0:
                signals.append(
                    f"{revised} of {n_ins} PR{'s' if n_ins != 1 else ''} iterated after "
                    f"review feedback — responsive to changes requested"
                )
            elif prs_with_disc > 0:
                signals.append(
                    f"Reviewer discussion present on {prs_with_disc} of {n_ins} PRs"
                )

        # Flag: clear pattern of CRs with no observed revision.
        # Threshold >=3 avoids flagging on a single borderline case.
        if cr >= 3 and revised == 0 and len(dim_flags) < 2:
            msg = (
                f"Changes requested on {cr} of {n_ins} PRs "
                f"with no observed revision cycle — worth discussing"
            )
            dim_flags.append(msg)
            top_flags.append({"severity": "caution", "dimension": "pr_quality", "message": msg})

    return {
        "score": clamp(score, 0, 20),
        "max": 20,
        "confidence": pr_confidence(n),
        "signals": signals[:3],
        "flags": dim_flags[:2],
    }, top_flags


# ---------------------------------------------------------------------------
# Dimension 3: Review Participation (max 20)
# ---------------------------------------------------------------------------
# Base:  >=10 reviews -> 12 | 5-9 -> 8 | 2-4 -> 5 | 1 -> 2 | 0 -> 0
# Bonus: >=50% of reviews are substantive (body_length > 50) -> +4
# Bonus: reviewed in >=2 distinct repos -> +4
# Cap:   0-20
#
# Signals answer: Do they review? How engaged are those reviews?
# Flag only fires when n >= 5 and zero written feedback (likely approval-only pattern)

def score_review_participation(reviews: list, insights_summary: dict | None = None) -> tuple[dict, list]:
    n = len(reviews)

    if n == 0:
        return {
            "score": 0,
            "max": 20,
            "confidence": "low",
            "signals": ["No reviews given in this window"],
            "flags": [],
        }, []

    score = 0
    signals = []
    dim_flags = []
    top_flags = []

    # Base score by volume
    if n >= 10:
        score = 12
    elif n >= 5:
        score = 8
    elif n >= 2:
        score = 5
    else:
        score = 2

    # Signal 1: volume with weekly rate
    weeks_approx = max(1, round(n / max(1, n)))  # placeholder; rate computed below
    signals.append(f"{n} review{'s' if n != 1 else ''} given")  # overwritten below with rate

    # Substantive feedback
    substantive = sum(1 for r in reviews if r["body_length"] > 50)
    subst_pct = substantive / n
    if subst_pct >= 0.50:
        score += 4

    # Cross-repo bonus
    review_repos = {r["repository"] for r in reviews}
    if len(review_repos) >= 2:
        score += 4

    # Build human-readable signals now that we have all the data
    signals = []

    # Signal 1: volume (rate will be added by caller if lookback_days is passed;
    # for now, just volume — the manager sees the lookback context from the header)
    signals.append(f"{n} review{'s' if n != 1 else ''} given")

    # Signal 2: written feedback — use count, not percent
    if substantive == n:
        signals.append(f"Written comments on all {n} reviews")
    elif substantive > 0:
        signals.append(f"Written comments on {substantive} of {n} reviews")
    else:
        signals.append("No written comments left — all reviews appear to be approvals")

    # Signal 3: breadth
    if len(review_repos) >= 2:
        signals.append(f"Reviewed PRs across {len(review_repos)} repos")
    elif len(review_repos) == 1:
        if len(signals) < 3:
            signals.append(f"All reviews in {list(review_repos)[0]}")

    # Flag: no written feedback across a meaningful number of reviews
    if n >= 5 and substantive == 0:
        msg = f"No written feedback across {n} reviews — may be approving without engaging"
        dim_flags.append(msg)
        top_flags.append({"severity": "caution", "dimension": "review_participation", "message": msg})

    # Insights enrichment: how the engineer's own PRs engage with review cycles.
    # Completes the review picture — not just how they review others, but how they
    # respond when others review them.
    ins = insights_summary or {}
    if ins and len(signals) < 3:
        n_ins   = ins["n"]
        revised = ins["revised_count"]
        cr      = ins["cr_count"]
        if revised > 0:
            signals.append(
                f"Responds to review feedback — {revised} of {n_ins} own "
                f"PR{'s' if n_ins != 1 else ''} revised before approval"
            )
        elif cr > 0:
            signals.append(
                f"{cr} of {n_ins} own PR{'s' if n_ins != 1 else ''} received change requests"
            )

    # Confidence: based on review count
    if n >= 10:
        confidence = "high"
    elif n >= 5:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "score": clamp(score, 0, 20),
        "max": 20,
        "confidence": confidence,
        "signals": signals[:3],
        "flags": dim_flags[:2],
    }, top_flags


# ---------------------------------------------------------------------------
# Dimension 4: Collaboration (max 20)
# ---------------------------------------------------------------------------
# Cross-repo PR authorship:  >=4 repos -> 8 | 2-3 -> 5 | 1 -> 2
# Reviews received on PRs:   avg >=1.5 -> 8 | >=0.5 -> 4 | >0 -> 2 | all-zero -> 0
# PR description quality:    >=70% with description -> +4
# Cap:                        0-20
#
# Signals answer: Are they integrated with the team? Bidirectional?
# Note: reviews_received_count may be 0 if the token lacks review metadata scope.
#       We do not penalize for missing data; confidence is set to low.
# Flag only fires when many PRs authored but 0 reviews given (one-directional).

def score_collaboration(prs: list, reviews: list, insights_summary: dict | None = None) -> tuple[dict, list]:
    if not prs:
        return {
            "score": 0,
            "max": 20,
            "confidence": "low",
            "signals": ["No PRs in window"],
            "flags": [],
        }, []

    n_prs = len(prs)
    n_reviews_given = len(reviews)
    score = 0
    signals = []
    dim_flags = []
    top_flags = []

    # Cross-repo contributions
    authored_repos = {p["repository"] for p in prs}
    n_repos = len(authored_repos)
    if n_repos >= 4:
        score += 8
    elif n_repos >= 2:
        score += 5
    else:
        score += 2

    # Signal 1: contribution breadth
    if n_repos == 1:
        signals.append(f"All {n_prs} PRs in one repository")
    else:
        signals.append(f"PRs across {n_repos} repos")

    # Reviews received
    total_received = sum(p["reviews_received_count"] for p in prs)
    reviews_data_missing = total_received == 0

    if not reviews_data_missing:
        avg_received = total_received / n_prs
        if avg_received >= 1.5:
            score += 8
        elif avg_received >= 0.5:
            score += 4
        else:
            score += 2
        # Signal 2: team engagement with their work
        signals.append(
            f"Avg {avg_received:.1f} review{'s' if avg_received != 1 else ''} received per PR"
        )
    # If reviews_data_missing: skip signal slot 2 — no useful info to surface

    # PR description quality
    with_desc = sum(1 for p in prs if p["description_length"] > 50)
    desc_pct = with_desc / n_prs
    if desc_pct >= 0.70:
        score += 4

    # Signal 2 or 3: bidirectional engagement
    if n_reviews_given > 0 and len(signals) < 3:
        signals.append(
            f"Authored {n_prs} PRs and gave {n_reviews_given} reviews — active in both directions"
        )
    elif desc_pct >= 0.70 and len(signals) < 3:
        signals.append(f"PRs are well-documented — makes code review easier for the team")
    elif desc_pct < 0.30 and len(signals) < 3:
        signals.append(f"Most PRs lack descriptions — reviewers may lack context")

    # Flag: active shipper but no reviews given (one-directional contribution)
    if n_prs >= 5 and n_reviews_given == 0:
        msg = f"Authored {n_prs} PRs but gave no reviews — consider engaging with the team's work"
        dim_flags.append(msg)
        top_flags.append({"severity": "info", "dimension": "collaboration", "message": msg})

    # Insights enrichment: reviewer engagement depth and breadth (additive)
    ins = insights_summary or {}
    if ins:
        n_ins         = ins["n"]
        avg_rev       = ins["avg_reviewers"]
        prs_with_disc = ins.get("prs_with_discussion", 0)

        # Signal: reviewer breadth or discussion presence (fills next free slot)
        if len(signals) < 3:
            if avg_rev >= 2.0:
                signals.append(f"Avg {avg_rev:.1f} reviewers per PR — broad team engagement")
            elif prs_with_disc >= max(2, round(0.5 * n_ins)):
                signals.append(
                    f"Active reviewer discussion on {prs_with_disc} of {n_ins} PRs"
                )

        # Flag: very low reviewer engagement across a meaningful sample
        if avg_rev < 0.5 and n_ins >= 5 and len(dim_flags) < 2:
            msg = f"Fewer than 1 reviewer per PR on average across {n_ins} PRs"
            dim_flags.append(msg)
            top_flags.append({"severity": "caution", "dimension": "collaboration", "message": msg})

    # Confidence: lower if review data is missing (partial picture)
    confidence = "low" if reviews_data_missing else pr_confidence(n_prs)

    return {
        "score": clamp(score, 0, 20),
        "max": 20,
        "confidence": confidence,
        "signals": signals[:3],
        "flags": dim_flags[:2],
    }, top_flags


# ---------------------------------------------------------------------------
# Dimension 5: Consistency (max 20)
# ---------------------------------------------------------------------------
# Active weeks ratio (PRs authored + reviews given, matching ingest.py):
#   >=75% -> 12 | >=50% -> 8 | >=25% -> 4 | <25% -> 2
# Max consecutive inactive weeks:
#   0 -> +4 | 1 -> +2 | >=2 -> 0
# Cadence evenness (no single week holds >50% of all PRs):
#   Pass -> +4
# Cap: 0-20
#
# Signals answer: Is contribution regular? Any patterns worth noting?
# Flags: gap >= 3 consecutive weeks only
# Gap detection uses active_week_set (PRs + reviews) — same definition as ingest.py.
# Velocity no longer flags gaps; this dimension owns that signal.

def score_consistency(prs: list, reviews: list, lookback_days: int, ingested_at: datetime) -> tuple[dict, list]:
    total_weeks = math.ceil(lookback_days / 7)
    since_dt = ingested_at - timedelta(days=lookback_days)
    n_total = len(prs)

    score = 0
    signals = []
    dim_flags = []
    top_flags = []

    # Build per-week PR histogram (for cadence evenness check)
    weeks_hist: dict[int, int] = {w: 0 for w in range(total_weeks)}
    for pr in prs:
        w = int((parse_dt(pr["created_at"]) - since_dt).total_seconds() // (7 * 86400))
        if 0 <= w < total_weeks:
            weeks_hist[w] = weeks_hist.get(w, 0) + 1

    # Active weeks = weeks with any PR authored OR review given (matches ingest.py)
    active_week_set: set[int] = set()
    for pr in prs:
        w = int((parse_dt(pr["created_at"]) - since_dt).total_seconds() // (7 * 86400))
        if 0 <= w < total_weeks:
            active_week_set.add(w)
    for review in reviews:
        w = int((parse_dt(review["submitted_at"]) - since_dt).total_seconds() // (7 * 86400))
        if 0 <= w < total_weeks:
            active_week_set.add(w)
    active_weeks_count = len(active_week_set)

    # Active weeks ratio
    ratio = active_weeks_count / total_weeks if total_weeks > 0 else 0
    if ratio >= 0.75:
        score += 12
    elif ratio >= 0.50:
        score += 8
    elif ratio >= 0.25:
        score += 4
    else:
        score += 2

    # Signal 1: active weeks ratio
    signals.append(
        f"Active in {active_weeks_count} of {total_weeks} weeks ({round(ratio * 100)}%)"
    )

    # Max consecutive inactive weeks
    max_gap = 0
    current_gap = 0
    for w in range(total_weeks):
        if w not in active_week_set:
            current_gap += 1
            max_gap = max(max_gap, current_gap)
        else:
            current_gap = 0

    if max_gap == 0:
        score += 4
    elif max_gap == 1:
        score += 2
    # >=2 weeks gap: no bonus

    # Signal 2: gap pattern
    if max_gap == 0:
        signals.append("No inactive weeks — consistent presence throughout")
    elif max_gap == 1:
        signals.append("One quiet week, otherwise consistent week-over-week")
    elif max_gap == 2:
        signals.append("Longest gap was 2 weeks")
    # >=3: flag fires below; skip this signal slot to avoid repetition

    # Flag: meaningful gap (>=3 weeks)
    if max_gap >= 3:
        msg = f"{max_gap}-week gap in activity — worth exploring what was happening"
        dim_flags.append(msg)
        top_flags.append({"severity": "info", "dimension": "consistency", "message": msg})

    # Cadence evenness: no single week holds >50% of all PRs
    if n_total > 0:
        max_week_count = max(weeks_hist.values()) if weeks_hist else 0
        if n_total >= 2 and max_week_count / n_total <= 0.50:
            score += 4
            if len(signals) < 3:
                signals.append("Work distributed across weeks — no major bursts")
        else:
            if len(signals) < 3 and n_total >= 2:
                # Find how concentrated: how many weeks hold 80% of PRs
                sorted_counts = sorted(weeks_hist.values(), reverse=True)
                cumulative = 0
                burst_weeks = 0
                for c in sorted_counts:
                    cumulative += c
                    burst_weeks += 1
                    if cumulative >= n_total * 0.8:
                        break
                signals.append(
                    f"Most activity concentrated in {burst_weeks} week{'s' if burst_weeks > 1 else ''}"
                )

    # Confidence: meaningful only with enough weeks of data
    if total_weeks >= 4 and active_weeks_count >= 3:
        confidence = "high"
    elif total_weeks >= 2 and active_weeks_count >= 2:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "score": clamp(score, 0, 20),
        "max": 20,
        "confidence": confidence,
        "signals": signals[:3],
        "flags": dim_flags[:2],
    }, top_flags


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score a PullStar ingest profile (all 5 dimensions, max 100)."
    )
    parser.add_argument("--login", required=True)
    parser.add_argument("--input-dir", default=".pullstar")
    parser.add_argument("--output-dir", default=".pullstar")
    args = parser.parse_args()

    input_path = Path(args.input_dir) / f"ingest_{args.login}.json"
    if not input_path.exists():
        fail(f"Ingest file not found: {input_path}\n  Run ingest.py first.")

    profile = json.loads(input_path.read_text(encoding="utf-8"))
    prs     = profile["prs_authored"]
    reviews = profile["reviews_given"]
    stats   = profile["summary_stats"]
    lookback_days = profile["lookback_days"]
    ingested_at   = parse_dt(profile["ingested_at"])

    # PR insights enrichment: detect PRs that were enriched by --pr_insights
    prs_with_insights = [p for p in prs if "discussion_summary_stats" in p]
    ins_summary       = _insights_summary(prs_with_insights) if prs_with_insights else {}

    # Score all 5 dimensions
    velocity,             vel_flags    = score_velocity(prs, lookback_days, ingested_at)
    pr_quality,           qual_flags   = score_pr_quality(prs, ins_summary)
    review_participation, rev_flags    = score_review_participation(reviews, ins_summary)
    collaboration,        collab_flags = score_collaboration(prs, reviews, ins_summary)
    consistency,          cons_flags   = score_consistency(prs, reviews, lookback_days, ingested_at)

    all_dims    = [velocity, pr_quality, review_participation, collaboration, consistency]
    total_score = sum(d["score"] for d in all_dims)

    # Deduplicate top-level flags by message; sort notable > caution > info
    raw_flags = vel_flags + qual_flags + rev_flags + collab_flags + cons_flags
    severity_rank = {"notable": 2, "caution": 1, "info": 0}
    seen: set[str] = set()
    deduped_flags: list[dict] = []
    for flag in sorted(raw_flags, key=lambda f: severity_rank.get(f["severity"], 0), reverse=True):
        if flag["message"] not in seen:
            seen.add(flag["message"])
            deduped_flags.append(flag)

    # Overall confidence + data volume note
    n_prs = stats["total_prs_authored"]
    if n_prs < 5:
        overall_confidence = "low"
        for d in all_dims:
            d["confidence"] = "low"
        data_volume_note = (
            f"Only {n_prs} PR{'s' if n_prs != 1 else ''} in the {lookback_days}-day window "
            f"— scores may not be representative."
        )
    else:
        low_count    = sum(1 for d in all_dims if d["confidence"] == "low")
        medium_count = sum(1 for d in all_dims if d["confidence"] == "medium")
        if low_count >= 2:
            overall_confidence = "low"
        elif low_count == 1:
            overall_confidence = "medium"
        elif medium_count >= 2:
            overall_confidence = "medium"
        else:
            overall_confidence = "high"
        data_volume_note = None

    scored = {
        "engineer_login": profile["engineer_login"],
        "scored_at": datetime.now(timezone.utc).isoformat(),
        "lookback_days": lookback_days,
        "dimensions": {
            "velocity":             velocity,
            "pr_quality":           pr_quality,
            "review_participation": review_participation,
            "collaboration":        collaboration,
            "consistency":          consistency,
        },
        "total_score": total_score,
        "confidence": overall_confidence,
        "data_volume_note": data_volume_note,
        "flags": deduped_flags,
    }

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"score_{args.login}.json"
    tmp_path = output_path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(scored, indent=2), encoding="utf-8")
    tmp_path.replace(output_path)

    dim_labels = [
        ("Velocity",             velocity),
        ("PR Quality",           pr_quality),
        ("Review Participation", review_participation),
        ("Collaboration",        collaboration),
        ("Consistency",          consistency),
    ]
    print(f"> Scored {args.login}: {total_score}/100 ({overall_confidence} confidence)")
    for label, dim in dim_labels:
        top_signal = dim["signals"][0] if dim["signals"] else "-"
        print(f"  {label:<22} {dim['score']:>2}/20  - {top_signal}")
    if data_volume_note:
        print(f"  Note: {data_volume_note}")
    if deduped_flags:
        print(f"  Flags: {[f['message'] for f in deduped_flags]}")
    print(f"> Written to {output_path}")


if __name__ == "__main__":
    main()
