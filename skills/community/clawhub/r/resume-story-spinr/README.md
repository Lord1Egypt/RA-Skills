# Resume Story Spinr

**Turn duty-listed resumes into quantified achievement narratives that survive ATS filters, 6-second skims, and interview follow-ups.**

## The Problem

A resume passes through two killers before a human says "interesting":

1. **The ATS parser** — if the posting says "PostgreSQL" and your resume
   says "relational databases", searchable keyword match fails and you're
   invisible. Fancy two-column layouts get linearized into gibberish.
2. **The 6-second skim** — recruiters scan for strong verbs and numbers.
   "Responsible for the payments API" has neither, and gets skimmed past
   with prejudice.

And even a great bullet creates a debt: "cut p99 latency 38%" means the
interviewer WILL ask "how did you measure that?" — a question most
candidates haven't prepared for.

## What It Does

`scripts/resume_spinr.py` (offline, Python stdlib only):

| Command | What it does |
|---|---|
| `transform` | "Responsible for X" → "Owned X"; gerund fixes; Action–Result splitting; quantification detection + metric hints for what to measure |
| `ats` | Keyword coverage of resume vs job posting (stop-word-filtered), missing-term list, weak-opener counts, filler/format hazard flags |
| `interview` | Expands each bullet into STAR story scaffolding + the likely follow-up questions it invites |
| `demo` | All three on sample data |

It's the deterministic structure engine — an agent (or you) supplies final
wording using its skeletons and your real numbers.

## Quick Start

```bash
# Transform weak bullets
python3 scripts/resume_spinr.py transform --bullets "Responsible for the payments API
Worked on improving test coverage"
# → Owned the payments API.  /  Improved test coverage.
#   ⚠ No metric — add: requests/sec served, p95/p99 latency change...

# Tailor to a posting
python3 scripts/resume_spinr.py ats --resume resume.txt --job posting.txt
# → Keyword coverage: 44% (4/9 terms); missing: grpc, observability...

# Prep the interview story behind a bullet
python3 scripts/resume_spinr.py interview --bullet \
  "Led migration of 14 services; cut deploy time from 40min to 6min"

# Tests
python3 scripts/test_resume_spinr.py   # → "35 passed, 0 failed"
```

## Who Needs This

- Job seekers updating a resume that isn't getting callbacks
- Career changers whose bullets describe duties, not outcomes
- Anyone tailoring a resume to a specific posting (10 min, highest ROI in
  the search)
- Interview preppers: every resume bullet should have a rehearsed STAR
  story behind it

Full ATS mechanics (parser behavior, formatting rules, keyword strategy,
finding your numbers) in
[`references/ats-guide.md`](references/ats-guide.md).

## Honesty Rule

The tool flags missing metrics and generates interview questions on
purpose: **never write a number you can't defend for two minutes out
loud.** Estimates fine; fabrication career-limiting.

## License

MIT © Denis Voronin
