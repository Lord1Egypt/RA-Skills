# Audit report sample (output contract)

Use this as the template when running this skill in **audit mode** (read-only,
H1). It is the same shape as `skill-clean-audit`: a verdict, per-criterion
findings, hard-constraint checks, a change log, and next steps. Never modify the
target file from here.

Fill `<...>` placeholders; drop any section that has no findings.

---

```markdown
# SKILL.md audit report — <name>

- **Target:** <absolute path to SKILL.md>
- **Linter verdict:** <PASS / NEEDS_FIX / BLOCKED> (exit <0|2|1>), <platform>
- **Auditor:** skill-md-optimizer (audit mode, read-only)
- **Date:** <YYYY-MM-DD>
- **Language:** <auto|zh|en> (three-state pick, NL-Policy)

## Verdict

<One paragraph. State the mechanical verdict (from the linter), the count of
blocker / medium / low findings, and whether the file is publish-ready.
BLOCKER>0 → "not publishable until blockers clear". Medium/low only → "publishable
with N advisory fixes".>

## Mechanical findings (from scripts/check_skillmd.py)

| # | Rule | Severity | Message | Suggested fix |
|---|---|---|---|---|
| 1 | <FM-105 / NL-002 / RF-001 …> | <blocker|medium|low> | <msg> | <hint> |

> Reproduce with: `python scripts/check_skillmd.py <target> --platform <p> --json`.

## Criteria findings (judgment layer, T/L/C/B)

- **T · Trigger precision:** <did frontmatter hit real phrasing? missing NOT-for? mis-trigger risk vs sibling skills? cite line refs.>
- **L · Layering:** <hard constraints separated from single-run flow? marked "every turn"?>
- **C · Convergence:** <is the flow ≤5 steps? does each state input/output/fallback? one-turn closed?>
- **B · Budget:** <body lines / est tokens vs 3500 cap; core in first ~1500–2000?>

## Hard-constraint checks (H1–H9)

| # | Check | Status |
|---|---|---|
| H1 | No rule silently dropped | <ok / violated: …> |
| H2 | No overwrite | <n/a (read-only) / …> |
| H4 | No network / no secrets | <ok / …> |
| H6 | Mechanical items delegated to linter | <ok / …> |
| H9 | Output language not guessed | <ok / three-state honored> |

> List only the H constraints that actually bind this audit; omit the rest.

## NL-Policy check (§6.0)

- **Shape 1** (`language:` with no nearby justification): <hit / none>
- **Shape 2** (body locked to one language with no opt-in): <hit / none>
- **Verdict:** <compliant / needs a three-state picker or a stated locale reason>

## Change log (if refactor suggested, not applied)

| # | Old | New | Reason | Assumed? | P0? |
|---|---|---|---|---|---|
| 1 | <old wording/structure> | <new> | <why> | <yes: what was assumed / no> | <yes/no> |

> Audit mode does **not** write the target (H1). The log above is the *plan* a
> follow-up `refactor` run would apply; each "assumed" row must be confirmed.

## Next steps

1. <Clear every BLOCKER first.>
2. <Resolve the Medium advisory items (or mark them accepted with a reason).>
3. <Optional: run the publish gate (skill-publish-gate --platform <p>) before release.>
4. <Re-run the linter; target BLOCKER=0 AND MEDIUM=0 before declaring done.>
```

---

## Notes for the auditor

- **Read-only is the red line (H1).** Never edit the target; the "Change log"
  section is a *plan*, not a change.
- **Keep the mechanical layer mechanical (H6).** Cite linter rule IDs, don't
  re-derive them by hand.
- **Assumptions get flagged (H3).** Any row that relies on a default the user did
  not state must say "assumed" + what was assumed.
- **NL-Policy is human-callable.** The linter only *hints* at shapes 1/2 (NL-001/002);
  the final "compliant or not" is the auditor's judgment against §6.0.
