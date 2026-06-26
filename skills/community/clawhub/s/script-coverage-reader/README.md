# Script Coverage Reader

**Platforms:** Claude · Openclaw · Codex
**Domain:** Film & TV — Development

## Purpose

A script-coverage reader for development teams. Reads a feature screenplay or TV pilot and produces industry-standard coverage: logline, one-page synopsis, character breakdown, craft grid (Excellent / Good / Fair / Poor across Premise, Story, Structure, Character, Dialogue, Setting), comments tied to specific pages and beats, producibility notes, comps, and a separate script verdict and writer verdict (Pass / Consider / Recommend).

## When to Use

- Reading a script submission (agency, manager, query, contest, OWA, internal)
- Producing coverage for a development meeting or weekend read
- Standardizing how a small development team rates scripts across readers
- Generating a comp pass and producibility check at a defined budget tier
- Generating a separate writer verdict to track a writer the team should meet regardless of this draft

## What It Does

**Phase 1: Intake**
1. Captures title, writer, format (feature / pilot / short), pages, draft, genre, submission source, budget tier, platform, and coverage type
2. Confirms whether a TV submission also includes a series document

**Phase 2: Read pass**
3. Reads the script in full while tracking beats by act, protagonist agency, opposing force, stakes, world, dialogue distinctiveness, voice, producibility, and representation

**Phase 3: Coverage draft**
4. Drafts a 25–40-word, spoiler-free logline
5. Drafts a ~1-page synopsis (summary, not opinion; spoilers OK)
6. Builds a character breakdown table
7. Rates the script on the craft grid using fixed scale anchors
8. Writes 1–1.5 pages of comments anchored to specific pages and beats
9. Adds producibility notes (locations, cast, VFX / period / IP, budget-tier fit)
10. Names 2–3 real released comparable projects

**Phase 4: Verdicts**
11. Gives a script verdict and a separate writer verdict (Pass / Consider / Recommend), each with a one-sentence rationale tied to the craft grid

## Output

A coverage document with:

- Submission metadata header
- Logline, synopsis, character breakdown
- Craft grid (Excellent / Good / Fair / Poor)
- Comments by craft category with page references
- Producibility notes and budget-tier fit
- Comps (real released projects only)
- Separate script and writer verdicts with rationale
- Optional next-steps and open-question flags

## Safety

The skill labels every output **COVERAGE — DEVELOPMENT TEAM USE ONLY** with reader name and date. It treats the script as confidential, paraphrases instead of quoting (no more than ~25 verbatim words), never invents beats or characters, never invents comps, and surfaces sensitivity flags professionally for the development team to handle.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
