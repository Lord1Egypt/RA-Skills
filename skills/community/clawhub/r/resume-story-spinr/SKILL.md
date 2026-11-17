---
name: resume-story-spinr
description: "Turn flat resume bullets ('Responsible for X') into quantified STAR-method achievement narratives, score resumes against job descriptions for ATS keyword coverage and weak-phrase hazards, and expand each bullet into interview-ready stories with likely follow-up questions. Use when the user is writing or updating a resume/CV, preparing bullets for a job application, tailoring a resume to a specific job posting, or preparing interview stories from their experience."
version: 1.0.2
author: Denis Voronin
license: MIT
tags: [resume, cv, career, job-search, ats, star-method, interviews]
---

# Resume Story Spinr

Resumes fail two filters: the ATS robot (keyword match) and the 6-second human skim (weak verbs, no numbers). Then whatever survives gets interrogated in the interview — and "Responsible for the payments API" has no story behind it. This skill transforms duty-bullets into quantified achievements, scores the resume against the target job description, and pre-builds the STAR stories an interviewer will dig for.

## Overview

`scripts/resume_spinr.py` (offline, stdlib-only):

- **`transform`** — weak → strong verb rewrites ("Responsible for" → "Owned", "Worked on improving" → "Improved"), Action–Result splitting on semicolons/dashes, quantification detection, and metric hints for every unquantified bullet (what to measure for APIs, migrations, leadership, support…)
- **`ats`** — keyword coverage of resume vs job description with stop-word filtering, missing-term list, weak-opener counts, filler-phrase and formatting hazard detection
- **`interview`** — expands each bullet into S/T/A/R story scaffolding plus likely follow-up questions ("How did you measure that number?", "What was YOUR contribution vs the team's?")
- **`demo`** — all three on sample data

This is the *structure engine* — it fixes grammar, verbs, metrics detection, and scoring deterministically. The agent (you) uses its skeletons to draft final wording with the user's real numbers.

## When to Use

- Writing/updating a resume or CV, or preparing bullet points
- Tailoring a resume to a specific job posting (run `ats` before and after)
- Converting a duties-listed resume into an achievements resume
- Preparing interview stories from resume bullets (STAR practice)
- Reviewing someone else's resume (structured critique with specifics)

**Don't use for:** cover letters (different document, different job), LinkedIn profile summaries (though bullets transfer), or academic CVs where duties-listing is the convention.

## How It Works

1. **Weak-opener library**: 17 weak phrases mapped to strong verbs ("responsible for"→"Owned", "helped with"→"Drove", "tasked with"→"Led").
2. **Gerund normalization**: "Worked on improving test coverage" → "Improved test coverage".
3. **Action/Result split**: bullets are split on `;`, `—`, "which resulted in", "reducing" — the first half is the Action, the rest becomes the Result clause, joined with " — ".
4. **Quantification regex**: detects %, currency, min/sec/ms, hours/days/weeks/months/years, user/customer/request counts, team sizes, 2.1M-style scales, req/s.
5. **ATS scoring**: tokenizes JD minus stop-words (no "looking", "experience", "team" noise), computes coverage, flags missing core terms, counts weak openers and filler phrases.
6. **Follow-up generation**: quantified bullets get "how did you measure it"; leadership bullets get conflict questions; migrations get "what went wrong".

## Quick Start

```bash
# Transform weak bullets
python3 scripts/resume_spinr.py transform --bullets "Responsible for the payments API
Helped with migration of legacy services to Kubernetes
Worked on improving test coverage"

# Same, from a file (one bullet per line)
python3 scripts/resume_spinr.py transform --file bullets.txt

# Score against a job description
python3 scripts/resume_spinr.py ats --resume resume.txt --job posting.txt

# Build the interview story behind a bullet
python3 scripts/resume_spinr.py interview --bullet \
  "Led migration of 14 services; cut deploy time from 40min to 6min"

python3 scripts/resume_spinr.py demo
```

## Steps (Agent Workflow)

1. Collect the user's current bullets (paste, file, or read from their resume text).
2. Run `transform`. For each ⚠-flagged bullet, ask the user for the real number using the printed metric hints ("What was the request volume? latency before/after?").
3. Re-run `transform --metrics "serving 2.1M req/day"` or rewrite with user-supplied figures.
4. Get the target job description; run `ats`. Add *true* statements covering missing core terms (never stuff keywords — 100% coverage is a red flag, 60–75% is strong).
5. For the 3–5 strongest bullets, run `interview` and have the user answer the follow-up questions out loud — the resume now makes promises the interview must keep.
6. Final human pass: tense consistency, no first person, one page per decade of experience.

## Output Shape

```
[1] BEFORE: Responsible for the payments API
    AFTER:  Owned the payments API.
    ⚠ No metric — add: requests/sec served, p95/p99 latency change, error-rate delta
    Interview follow-up: What was YOUR specific contribution vs the team's?

[2] BEFORE: Led migration of 14 services; cut deploy time from 40min to 6min
    AFTER:  Led migration of 14 services — cut deploy time from 40min to 6min.

ATS MATCH REPORT
  Keyword coverage: 44%  (4/9 job terms found)
  [████████░░░░░░░░░░░░]
  Missing from resume (5):
    - grpc
    - observability
    ...
```

## Common Pitfalls

1. **Inventing metrics.** The tool flags missing numbers; the *user* must supply real ones. A fabricated "38% latency cut" collapses in the interview when asked "how did you measure it?" — which the tool deliberately also generates.
2. **Keyword stuffing to 100%.** ATS coverage above ~75% with terms not backed by real experience gets flagged by recruiters and destroyed in screening calls. Mirror only true statements.
3. **Keeping "Responsible for".** It's the single most common resume verb and says nothing about impact. Every weak opener has a stronger replacement in the library.
4. **One-line wonders with no Result.** "Owned the payments API" is still a duty without an outcome. Every bullet needs Action — Result; the split heuristics show where the result should go.
5. **Resume promises the interview can't keep.** Every quantified bullet invites "walk me through it". Run `interview` on each final bullet; if the user can't tell the story, soften the bullet or practice the story.
6. **Fancy formatting.** Tables, text boxes, multi-column layouts, and non-standard bullets silently scramble ATS parsers. Plain single-column, standard headers, hyphen bullets.
7. **Sending the same resume everywhere.** Run `ats` per posting; 10 minutes of tailoring (core terms + reorder bullets) is the highest-ROI time in a job search.

## Verification Checklist

- [ ] No weak openers remain (`transform` summary shows 0 unfixed)
- [ ] Every bullet quantified or consciously excepted (rare, e.g. people management)
- [ ] Every bullet reads Action — Result
- [ ] ATS coverage 60–75%+ on core terms for the target posting
- [ ] No filler phrases ("team player", "hard worker") detected
- [ ] Interview stories rehearsed for the top bullets
- [ ] Final format: single column, standard section headers, .docx or clean PDF

## One-Shot Recipes

**"Fix my resume for this posting"**
```bash
python3 scripts/resume_spinr.py ats --resume resume.txt --job posting.txt
python3 scripts/resume_spinr.py transform --file resume_bullets.txt
# add true statements for missing core terms, re-run ats → 60-75%+
```

**"I have a list of duties, need achievements"**
```bash
python3 scripts/resume_spinr.py transform --file duties.txt
# for each ⚠ bullet, extract the real number from the user, rewrite
```

**"Interview is tomorrow, stories from my resume"**
```bash
python3 scripts/resume_spinr.py interview --file resume_bullets.txt
# user answers each follow-up out loud; fix bullets they can't defend
```

## References

- [`references/ats-guide.md`](references/ats-guide.md) — how ATS parsers actually work, keyword strategy, formatting rules that survive parsing, before/after examples
