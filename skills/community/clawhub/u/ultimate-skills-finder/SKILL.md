---
name: ultimate-skills-finder
description: Multi-source skill discovery across ClawHub, skills.sh, SkillsMP, and two curated GitHub lists. Cross-references, deduplicates, and ranks results, and emits install commands only for sources that publish a verifiable identifier. Use when the user wants to find or compare existing skills for a capability ("is there a skill that...", "find me a skill for...", "which skill should I use for..."). Do not use to perform the task directly.
---

# Ultimate Skills Finder

Searches **5 sources**, merges duplicate findings, and ranks by breadth,
popularity, and source authority.

## When to use this

Use when the user is looking for an **existing skill** to cover a
capability, or wants to compare candidates.

Do not use it to just do the task. If the user wants their PDF edited, edit
the PDF. This skill finds candidates; it is not the work itself.

## Quick start

```bash
python3 scripts/find_skill.py "web scraping"
python3 scripts/find_skill.py "pdf editor" --show-install
python3 scripts/find_skill.py "seo" --popular
python3 scripts/find_skill.py "email" --json
python3 scripts/find_skill.py "email" --source clawhub
python3 scripts/find_skill.py "pdf" --scan --share-urls   # see disclosure note
```

Requires **Python 3.9+**. The code uses `asyncio.to_thread`; on 3.8 the
script fails at the first network call with an `AttributeError`.

## Sources

| # | Source | Kind | Install command? |
|---|--------|------|------------------|
| 1 | **ClawHub** (`clawhub.ai`) | Official registry | yes |
| 2 | **skills.sh** | Directory with real install counts | yes |
| 3 | **SkillsMP** (`skillsmp.com`) | Raw aggregator, uncurated | no — browse only |
| 4 | **VoltAgent/awesome-openclaw-skills** | Curated GitHub README | no — browse only |
| 5 | **LeoYeAI/openclaw-master-skills** | Curated GitHub README | no — browse only |

The split is deliberate. Sources 1–2 publish a machine-checkable
identifier, so the tool can emit a command it has validated. Sources 3–5
surface text that a third party can freely edit, so they give you a name and
a link to review yourself. **A browse-only entry is not a lesser result** —
the curated lists often cover skills that no registry has indexed.

## Options

| Flag | Effect |
|------|--------|
| `--limit N` | Max results per source (default 5) |
| `--show-install` | Print install commands where a verified path exists |
| `--popular` | Sort by raw popularity instead of relevance |
| `--exclude-chinese` | Drop results written in Chinese. Japanese and Korean are kept — Han characters alone are ambiguous, so kana or hangul keeps a result in. Reports how many it dropped; never silent |
| `--json` | JSON output for further processing |
| `--source <name>` | Restrict to one source |
| `--scan` | Request advisory security labels (**requires `--share-urls`**) |
| `--share-urls` | Consent to the third-party disclosure described below |

## Security rules

These are not optional.

**1. Never run an install command without showing the user first.**
Before running anything, display the validated identifier, the source
registry, the canonical URL, and the version. Then ask.

**2. Only run commands that the tool printed.** The tool builds install
commands as argument arrays from identifiers that passed an allowlist
(`^[A-Za-z0-9][A-Za-z0-9._/-]*$`, 1-128 chars, no `..` traversal and no
empty segment). Anything you construct yourself, or that you assemble from
a browse-only source, is unvalidated. Do not run it.

**3. Browse-only sources get no install command.** For SkillsMP and the two
curated lists, show the name and the GitHub link, then let the user decide.
If they want one, verify it on the registry yourself first.

**4. Every search discloses the query; `--scan` adds URL disclosure.**

*Always:* the raw query string is sent to ClawHub, skills.sh, SkillsMP and
GitHub as part of searching. There is no flag for this and no consent step.
If the user is likely to type something confidential — a client name, an
unreleased codename — say so *before* running the search, and offer to use a
generic query instead.

*Additionally with `--scan`:* it POSTs the URL of every result to
`ai.gendigital.com`. It refuses to run without `--share-urls`. Ask the user
before supplying that flag. Do not add it on their behalf.

**5. Security labels are advisory.** All five levels were observed live from
the scanner on 2026-10-16 — `SAFE`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` —
so treat the vocabulary as real. `SAFE` means a third party has not flagged
the package. It is not a
guarantee of safety. A `analysis_pending` verdict is displayed as **pending
review** and is explicitly *not* an approval — it means nobody has looked
yet. Never present `SAFE` as clearance, and never downplay `HIGH` or
`CRITICAL` — surface them with the reasons the scanner returned before
recommending anything.

Roughly 2 in 3 lookups return **no verdict at all**. That means the scanner
could not resolve the skill, not that it is safe. Say "not scanned", never
"no concerns found".

A result with **no `scan:` line was not scanned**. Absence of a label is not
a clean bill of health.

## Workflow

1. **Understand the need.** Identify the concrete task. If the user said
   "how do I do X", decide first whether a skill is warranted at all.

2. **Run the search.** Use `--show-install` when you intend to offer
   installation.

3. **Read the results critically.** Before recommending anything:
   - Does the description match what the user actually needs?
   - Is it cross-listed in more than one source? A skill on the curated
     lists *and* a registry is more likely to be real and maintained.
   - Is the install count plausible, or does it look inflated?

4. **Present 3–5 candidates.** For each: name, what it does, which sources
   listed it, and the URL. Flag browse-only entries as needing manual review.

5. **Install only on explicit request,** following the security rules above.

## Interpreting the output

Each result shows its sources, popularity, description, and URL. Results
from skills.sh have no description — that endpoint does not return one — so
a skills.sh-only hit shows an explicit placeholder instead of an empty line.

`N of M have a verified install path` at the bottom tells you how much of
the result set is directly installable. The remainder still needs review.

## When nothing is found

1. Broaden or synonym the query (`email` → `smtp` → `messaging`).
2. Consider that the capability may not exist as a skill.
3. Say so plainly, and offer to do the task directly. Do not invent a
   recommendation to fill the gap.

## Known limitations

- Descriptions are missing for skills.sh-only results.
- SkillsMP is uncurated. Its `stars` field is a **repository** star count,
  not a per-skill measure, so v1.2.2 sets it to zero and excludes it from
  ranking entirely rather than treating it as popularity.
- ClawHub search responses also carry `trust.upstreamScanners` — per-skill
  verdicts from Snyk, Socket and Agent Trust Hub, arriving with the search
  and involving no extra disclosure. This version does not surface them.
- Popularity figures are not comparable across sources: ClawHub and
  skills.sh report installs, SkillsMP reports repository stars.
- The two curated lists are parsed from README text and will degrade if
  those repositories change their table format.
- Results whose name fails the identifier allowlist are dropped silently by
  some parsers. If results seem unexpectedly few, suspect a name filter
  rather than a missing skill.