---
name: openclaw-skills-doctor
description: Audit the skills OpenClaw loads and get a measured plan to cut their per-step token cost.
metadata:
  openclaw:
    emoji: 🩺
    requires:
      bins:
        - npx
    homepage: https://github.com/wangyuchen5110/openclaw-skills-doctor
---

# openclaw-skills-doctor

Every eligible skill costs the prompt ~97 characters plus its name, description
and location - **on every step**. Audit that cost before adding more skills.

## When to use

- The user asks why a skill is missing, duplicated, or not the one they expect.
- The skill catalog feels large, or the context window is under pressure.
- A `SKILL.md` references files that may have moved.
- Before/after installing skills from ClawHub or a Git repo.

## Run it

```bash
npx -y openclaw-skills-doctor doctor      # paths, roots, MCP + skill install state
npx -y openclaw-skills-doctor check       # findings + per-step token cost
npx -y openclaw-skills-doctor plan        # what to trim / hide, in tokens
npx -y openclaw-skills-doctor scan        # every skill: source, precedence, cost
```

`check` is read-only. Add `--json` for structured output, `--html report.html`
for a shareable report, `--budget <n>` to change the 1200-token/step target.

## Reading the result

- **token-budget** - descriptions cost more than the budget every step. Run
  `plan`; prefer trimming descriptions (keeps discoverability) over hiding.
- **shadowed / near-duplicate** - the same name loads from several roots and only
  the highest-precedence one wins. `fix --dry-run` then `fix` archives the losers
  into `.skills-doctor-archive/` (reversible).
- **broken-reference** - a `references/`, `scripts/` or `assets/` path does not
  resolve next to the `SKILL.md`. Fix the path; the file may live one level up.
- **large-body** - paid only when the skill is invoked; move detail into
  `references/`.

## Fixing

```bash
npx -y openclaw-skills-doctor fix --dry-run   # what would be archived/hidden
npx -y openclaw-skills-doctor fix             # archive shadowed duplicates (reversible)
npx -y openclaw-skills-doctor fix --hide old-skill   # autoinvoke: false, still loadable via @id
```

Never edit the top-level `openclaw.json` by hand from here - `install`/`uninstall`
own the `mcp.servers.skills-doctor` entry.

## As an MCP tool

When the MCP server is registered (`npx -y openclaw-skills-doctor install`), call
the tool `skills-doctor__skills_doctor` instead of shelling out. It returns the
same markdown report and accepts `directory`, `budget`, `lang` and `html`.
