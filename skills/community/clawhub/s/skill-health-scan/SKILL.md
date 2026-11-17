---
name: skill-health-scan
version: 1.1.2
description: Use when two skills fire for the same request, or a skill never fires at all scans every installed skill, maps trigger overlaps and blind spots, delivers one health report with fixes. skillsskillsscanAllinstalled skills, map trigger overlaps and blind spots, deliver acheckupreport
---

# Skill Health Checkup

Your skills fight each other for attention — or never get any. This skill runs a full physical exam on every installed skill and ships one report: who overlaps whom, who is dead weight, who has a broken description.


## Onboarding (First Use)

When the user first triggers this skill and `memory/skill_health_scan_state.json` doesn't exist, run a one-time setup:

1. **Introduce capability** (one sentence): _I can give all yourAllskillscheckup, report_

2. **Quick configuration:**

1. **Report language**(Default: Follow user input language)
   - Chinese / English / Follow user input
2. **Fix suggestion mode**(Default: report + )
   - Report only (find issues, no file changes)
   - Report + suggest fixes (show diff, execute after user confirmation)

3. **Write initial state file** `memory/skill_health_scan_state.json`(JSON format, with `onboarded: true` and timestamp)

4. **Confirm completion**: _"Setup done! Just use it from now on. Say 'reset settings' anytime to reconfigure."

**Onboarding runs exactly once.** Subsequent activations read the state file directly. When the user says "reset settings", delete the state file and re-run setup.

---

## Startup

1. Locate the skills directory (try in order: `~/.openclaw/skills/`, `<project>/.claude/skills/`, `~/.claude/skills/`; if none exists, ask the user where skills live)
2. Run the deterministic scan:
   ```bash
   python3 scripts/scan_skills.py --dir <skills-dir> --json
   ```
3. Python unavailable → read each `SKILL.md` frontmatter manually (name + description only)
4. Report language: match the user's language

## The Exam — 5 checks

### 1. Trigger Overlap (the headline check)
For every pair of skills, compare their `description` trigger phrases:
- **RED** — two skills explicitly claim the same scenario (e.g. both say "Use when the user asks to optimize a prompt")
- **YELLOW** — partial overlap: same verbs, different objects ("write a report" vs "write documentation")
- **GREEN** — no conflict
Verdict rule: for every RED pair, name the exact sentence a user could type that would wake both skills. No hypotheticals — the sentence must be plausible.

### 2. Dead Zones
Ask the user for their 5 most frequent task types (or infer from conversation). Check which tasks have **no skill covering them**. A dead zone is not an error — it is expansion space. List top 3 with a one-line skill idea for each.

### 3. Description Fitness
For each installed skill:
- description shorter than 60 chars → trigger accuracy at risk (**RED**)
- no "Use when"-style trigger phrase → the model must guess when to fire (**YELLOW**)
- describes features ("generates reports") instead of scenarios ("use when memory contains stale numbers") → propose a rewrite (**YELLOW**)

### 4. Duplicates
Same core function installed twice — detect by name similarity plus description similarity (≥60% keyword overlap in the trigger phrase). **RED**. Ask before suggesting removal.

### 5. Bloat
Skills that are large (many reference files) AND plausibly never triggered = dead weight loading cost. **YELLOW**, suggest review — never delete without asking.

## Report

Follow `references/report-template.md`. Rules:
- Overlaps: one line per skill pair, with the wake-both sentence quoted
- Fitness: one line per skill with the verdict and the fix
- End with **Top 3 fixes by impact** — the three edits that most improve trigger accuracy

## Fix Protocol

- For RED overlaps: propose a boundary sentence for each skill ("You handle X; the other handles Y"), then edit both descriptions
- For fitness issues: offer a rewritten description, show the exact before/after
- Never modify a skill without showing the user the precise diff first
- Re-run check 1 after any description edit to confirm the conflict is gone
