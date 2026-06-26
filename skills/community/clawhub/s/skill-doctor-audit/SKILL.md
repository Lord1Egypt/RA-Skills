---
name: skill-doctor
version: "1.0.0"
description: "Audit, debug, and clean up the OpenClaw skills you already have installed. Use this skill whenever the user asks to check, audit, review, clean up, or debug their installed skills, or says things like 'why did the wrong skill fire,' 'which skill handles X,' 'do any of my skills conflict,' 'are my skills safe,' 'scan my skills for security issues,' 'are any of my skills out of date,' 'which skills overlap,' 'why isn't my skill triggering,' 'audit my skill library,' or 'is this skill safe to keep.' Detects duplicate and conflicting triggers (skills that fight over the same prompts), inline security red flags (credential exfiltration, remote code execution, hard-coded secrets), and out-of-date versions, and predicts which installed skill will fire for any given prompt. The missing health check for a growing skill collection."
metadata:
  openclaw:
    emoji: 🩺
---

# Skill Doctor

Most OpenClaw guidance is about *finding and installing* new skills. Almost nothing helps once you have twenty of them and two quietly fight over the same prompts, one is three versions behind, and one you installed last month does something to your environment you never noticed. Skill Doctor is the checkup for the skills you already have.

It does four things, all offline and with no API key:

1. **Conflict detection** - finds skills whose triggers overlap, so you know why the agent sometimes fires the wrong one.
2. **Security scan** - flags inline red flags in skill files (remote code execution, credential exfiltration, hard-coded secrets, destructive commands).
3. **Version check** - reports which skills are behind their latest ClawHub release (when the `clawhub` CLI is available).
4. **"Which fires?" prediction** - given any prompt, ranks which installed skill is most likely to handle it, and warns when the choice is ambiguous.

## When to use this

Reach for Skill Doctor whenever the user is reasoning about their *installed* collection rather than looking for something new. Triggers include "audit my skills," "why did the wrong skill fire," "which skill handles X," "are my skills safe," "scan for security issues," "anything out of date," or "clean up my skills." If they want to *discover* a new skill, that is a different job - this is the doctor, not the directory.

## The tool

Everything runs through `skill_doctor.py` (pure Python 3, standard library only; it will use PyYAML if installed but does not require it). All commands auto-detect the installed-skills directory; pass `--skills-dir` to point at a specific one.

```bash
python skill_doctor.py audit       # full health report (run this first)
python skill_doctor.py conflicts   # just the trigger overlaps
python skill_doctor.py security    # just the red-flag scan
python skill_doctor.py stale       # installed vs latest ClawHub version
python skill_doctor.py which "the prompt to test"
```

Add `--json` to any command except plain `conflicts`/`security` text mode when you need structured output to reason over.

### Finding the skills directory

`audit` auto-detects by checking, in order: `$OPENCLAW_SKILLS_DIR`, `~/.openclaw/skills`, `~/.openclaw/extensions`, `/data/.openclaw/skills`, `/data/.openclaw/extensions`, `/usr/local/lib/node_modules/openclaw/extensions`, and `~/.claude/skills`. The first directory that actually contains skill folders wins. If the user runs a non-standard layout, ask for the path and pass `--skills-dir`.

## How to run an audit

1. Run `python skill_doctor.py audit`. If it cannot find the skills directory, ask the user where their skills live and re-run with `--skills-dir`.
2. Read the Markdown report back to the user, but **lead with what matters**: high-severity security flags first, then conflicts, then stale versions. Do not just dump the raw report - interpret it.
3. For each finding, give a concrete next step (see below). The value is in the recommendation, not the list.

## Interpreting the results

**Security flags.** Severity is the guide. A `high` flag (curl-piped-to-bash, environment variables posted to a URL, hard-coded `ghp_`/`sk-`/`AKIA` tokens, reads of `~/.ssh`/`.aws/credentials`, reverse-shell patterns, `rm -rf /`) deserves a clear, calm warning and a recommendation to review the exact file and line before trusting the skill. A `medium` flag (`shell=True`, `eval`/`exec`, `chmod 777`) is worth a look but often legitimate. Always cite the file and line and show the snippet so the user can judge for themselves - your job is to surface, not to accuse. A flag is a reason to look, not proof of malice.

**Conflicts.** When two skills share an explicit trigger phrase or have high keyword overlap, the agent can fire the wrong one. The fix is almost always to tighten one skill's `description` so the two stop competing - narrow the broader skill, or add distinguishing context ("for *church* events" vs "for *corporate* events"). Offer to edit the description if the user wants.

**Versions.** `behind` means a newer ClawHub release exists - offer to update it. `missing-version` means the skill has no `version` field in its frontmatter, which breaks update tracking - offer to add one. `no-clawhub-cli` just means the `clawhub` command is not installed, so remote version checking was skipped (everything else still ran).

**"Which fires?"** Use this to debug triggering. If the user complains the wrong skill ran, run `which "<their prompt>"`. A clear single winner means triggering is working; a `WARNING: ambiguous` with close scores explains the misfire and points at exactly which descriptions to disambiguate. If nothing scores, the agent would handle the prompt with base tools and no skill fires - which is sometimes the real reason "my skill didn't trigger."

## Example

**Input:** "can you check my installed skills - something keeps answering event questions wrong and I want to make sure none of them are sketchy"

**Approach:**
1. Run `audit` for the full picture.
2. Run `which "plan our fall event"` (or the user's actual phrasing) to pin down the event-triggering ambiguity.
3. Report: lead with any security flags, then explain the event-skill conflict and which two descriptions overlap, then offer to tighten the broader skill's description so the right one wins.

## Notes for honest output

- Never imply a skill is malicious just because it tripped a flag. Show the evidence and let the user decide.
- If the scan comes back clean, say so plainly - a clean bill of health is a useful result, not a failure to find something.
- Keep the recommendations concrete and few. A short list of "here's the one thing worth fixing" beats an exhaustive dump.
