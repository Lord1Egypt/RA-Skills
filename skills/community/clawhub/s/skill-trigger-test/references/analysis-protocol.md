# Analysis Protocol — Trigger Test

The same 4-question analysis runs for every (test message × skill) pair. The agent answers each question with evidence quoted from the skill's `description`, then reaches one verdict.

## Setup

For the run, collect:
- The full `description` text of every installed skill (from SKILL.md frontmatter)
- The test suite: generated messages + user's real messages, each labeled `expect: TRIGGER <skill>` / `expect: SILENT` / `expect: CONTESTED`

## The 4 questions (answer in order, each with quoted evidence)

### Q1 — Intent match
What is the core intent of the test message? Which claimed scenario (if any) in this skill's description covers that intent?
- Quote the exact scenario phrase from the description that matches (or state "no scenario covers this")
- A partial match counts only if the intent, not just a keyword, matches

### Q2 — Keyword evidence
Which concrete words/phrases from the message appear in or clearly imply phrases in this skill's description?
- List each overlap as `message: "…" ↔ description: "…"`
- Keyword overlap WITHOUT intent match does not justify triggering (this is the #1 source of false alarms)

### Q3 — Competition
Do any OTHER installed skills also claim this scenario per their descriptions?
- List each competitor with its competing scenario phrase
- If none: answer "no competition"
- This question prevents double-counting: a skill only "wins" a contested message if its claim is more specific

### Q4 — Verdict
Combine Q1-Q3 into exactly one:
- **TRIGGER** — intent matches a claimed scenario, with evidence
- **SILENT** — no scenario covers the intent
- **CONTESTED** — this skill and ≥1 other both claim it with comparable specificity
- **LOST** — intent matches this skill AND a more specific competitor (points to the competitor)

Score against the expected label:
- expect TRIGGER + verdict TRIGGER = hit
- expect TRIGGER + verdict SILENT or LOST = miss
- expect SILENT + verdict TRIGGER = false-alarm
- expect CONTESTED + verdict CONTESTED = hit
- anything else = unexpected (investigate)

## Message generation rules (for the generated suite)

From a skill's description, derive positives, negatives, and ambiguous:

**Positives (3)** — rephrase each claimed scenario as a natural user message:
- One that quotes a trigger phrase almost verbatim (easy case)
- One that expresses the intent in completely different words (hard case — the one that catches vague descriptions)
- One real-world context message (e.g. for a PDF skill: "here's the landlord's contract, what am I signing?")

**Negatives (3)** — messages from neighboring intents that share keywords but differ in intent:
- Identify the 2-3 keywords most likely to over-attract (e.g. "file", "read", "code")
- Write messages containing those keywords whose actual intent belongs to a DIFFERENT skill or no skill
- Example: for a git skill, "read me the error in this log file" must NOT trigger it

**Ambiguous (1)** — a message where two installed skills' claims genuinely overlap; label expect CONTESTED

## Calibration rules

- Never let a verdict rest on the skill's NAME alone — names mislead; descriptions are what the host reads
- When truly torn between TRIGGER and SILENT, choose SILENT and mark the case "borderline" in the report — silent failures (misses) are the expensive failure mode, so borderline calls should surface, not hide
- A verdict with no quoted evidence is invalid; re-run that pair
