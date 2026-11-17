# ATS Guide — How Resume Robots Actually Read Your Resume

## What an ATS Does (and Doesn't)

Applicant Tracking Systems (Workday, Greenhouse, Lever, Taleo, iCIMS) are
**not AI judges**. They are parsers + databases:

1. **Parse** your document into structured fields (name, contact, roles,
   dates, skills).
2. **Index** the text for recruiter keyword searches and auto-matches.
3. **Rank** (some systems) candidates by keyword overlap with the posting.

A resume fails the ATS when *parsing* scrambles it (formatting hazards) or
when *matching* can't find the posting's terms (wording hazards). No parser
reads your beautiful two-column layout — it reads a content-extracted
soup, and your job is to keep that soup clean.

## The Two Filters

| Filter | Reader | Time | What kills you |
|---|---|---|---|
| ATS match | Parser + recruiter search | seconds | missing keywords, scrambled format |
| Human skim | Recruiter/hiring manager | 6–10 seconds | weak verbs, no numbers, wall of text |

You must survive both. Keywords get you found; quantified achievements get
you read.

## Keyword Strategy

**Mirror the posting's core terms exactly.** If the posting says
"PostgreSQL", don't only write "Postgres" or "relational databases" —
older matchers are literal. Legit synonyms can appear once, but the exact
term must appear in a *true* statement:

- Posting: "CI/CD" → bullet: "Built CI/CD pipeline (GitHub Actions) cutting
  release cycle from 2 weeks to 2 days"
- Posting: "stakeholder management" → bullet: "Ran stakeholder reviews for
  4 product lines; shipped 100% of committed Q3 scope"

**Where keywords count most** (parser weighting, roughly): skills section,
job-title line, bullets within the 3 most recent roles, summary. Don't
waste the prime real estate on "team player".

**Coverage targets:** 60–75% of the posting's distinctive terms means a
genuine match. 100% coverage means you stuffed (or you're the perfect
candidate, in which case, apply now). Below 40% means you'll never surface
in searches — either tailor the resume or don't apply.

## Formatting That Survives Parsing

### Do
- Single column, top-to-bottom
- Standard headers: "Experience", "Education", "Skills" (not "Where I've
  Made Magic")
- Hyphen (`-`) bullets, left-aligned
- .docx or text-based PDF (vector, not scanned)
- Dates as `MM/YYYY – MM/YYYY` on one line
- Job titles next to dates, company on its own line

### Don't
- Tables, text boxes, sidebars — parsers linearize them into gibberish
- Headers/footers for critical info (some parsers skip them entirely —
  your phone number lives there and vanishes)
- Graphics, icons, emoji, skill-bar charts (unparseable noise)
- Multi-column layouts (reading order scrambles chronology)
- Creative section names (the parser's section-mapping fails)
- .pages, .odt, image-PDFs

## The Weak-Verb Problem

The most common resume failure at the human filter:

| Duty voice (invisible) | Achievement voice (interviewable) |
|---|---|
| Responsible for the payments API | Owned payments API serving 2.1M req/day |
| Helped with Kubernetes migration | Drove migration of 14 services to K8s — deploy time 40min → 6min |
| Worked on improving test coverage | Raised test coverage 41% → 78%; escaped bugs down 60% |
| Was part of the design team | Designed checkout flow; task completion +23%, support tickets −31% |
| Duties included on-call | Ran on-call for 99.99%-uptime tier-1 service; MTTR 45min → 12min |

The pattern: **strong past-tense verb + specific object + measured result.**
The tool's `transform` enforces the first two mechanically and nags until
the third exists.

## Finding Your Numbers (When You Think You Have None)

Everyone has numbers; most people haven't dug for them:

- **Scale**: users, requests/day, records, transactions, team size, budget
- **Change**: % faster/slower, before→after times, error rates, costs
- **Counts**: projects shipped per quarter, incidents handled, tickets
  resolved, reports/builds/deployments per week
- **Money**: revenue influenced, cost saved, contract values, headcount
  avoided
- **Time**: how long the old way took vs your way, MTTR, cycle time

Estimates are fine if honest and defensible ("~2M req/day", "reduced
roughly 40%"): you will be asked how you know, and "we watched the Grafana
dashboard for a month" is a great answer. Fabrication is not fine.

## Bullet Transformation Worked Example

**Before (duty):**
> Responsible for monitoring and alerting infrastructure, was part of the
> SRE on-call rotation, and helped various teams with reliability issues.

**After (achievements):**
> - Owned monitoring stack (Prometheus + Grafana) across 30+ services;
>   alert precision 45% → 82%, pages per night down 60%
> - Ran tier-1 on-call rotation (4 engineers); drove MTTR from 45min to
>   12min via runbook automation
> - Partnered with 6 product teams on SLOs; error-budget reviews adopted
>   org-wide

Same person, same work — one version gets skimmed past, the other gets
interviews.

## The Interview Consistency Check

Every quantified bullet generates interviewer questions:
- "How did you measure that?"
- "What was your specific contribution?"
- "What went wrong / would you do differently?"

Rule: **if you can't tell the 2-minute story behind a bullet, don't put
the bullet on the resume.** Run `interview` on each final bullet and
rehearse out loud. The resume and the interview must tell the same story —
discrepancies read as fabrication even when they're just forgetting.

## Posting Red Flags (When NOT to Tailor)

- "Rockstar/ninja/guru" culture-speak with no concrete requirements
- 4+ years required for 12 technologies simultaneously
- Salary below market for the listed requirements
- Same posting reposted monthly (revolving door or ghost req)

Tailoring costs 10–15 minutes. Spend it on postings that pass the smell
test.
