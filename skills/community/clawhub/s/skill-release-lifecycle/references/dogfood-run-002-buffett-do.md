# Dogfood Run 002 — buffett-do

## Date

2026-05-24

## Tested Skill

- Lifecycle under test: `skill-release-lifecycle`
- Case under test: `buffett-do`
- Skill type: user-facing research-prioritization skill
- Local skill path: `/root/.hermes/skills/wbwd/buffett-do/SKILL.md`
- ClawHub slug: `buffett-do`

## Input Used

Primary input was the local `buffett-do` SKILL.md content loaded via `skill_view`:

- name: `buffett-do`
- local version: `1.1.6`
- description: `Buffett-style Research Prioritization Assistant — decide whether a company deserves deeper research, what to check first, and get a copy-paste research prompt for your agent.`
- title: `# What Buffett Would Do`
- activation: `what Buffett would do with [company/ticker]`
- example: `what Buffett would do with Pop Mart`
- output contract: `Decision`, `Check First`, `Paste This to an Agent`
- anti-scope: standalone `## What This Will Not Do`
- feedback path: `DM me on X: @BeeGeeEth`

Additional direct verification:

```bash
clawhub inspect buffett-do
```

Observed:

- ClawHub latest version: `1.1.10`
- Local SKILL.md version: `1.1.6`

This means the local file inspected in this dogfood run may be stale relative to the current public release.

## A–E Gate Results

### A. Utility / Recurrence — PASS, with reference-derived evidence

**Evidence:**

- The workflow is recurring: deciding whether a company deserves deeper research is a repeated investment-research triage task.
- It applies to many company/ticker inputs, not a one-off task.
- The output was used to publish a public skill and define a reusable research prioritization format.
- Prior iteration records show multiple public-release revisions around migration, activation, feedback placement, and user-facing wording.

**Evidence source:**

- direct inspection: recurring workflow is visible from the skill description and activation pattern.
- reference-derived / historical claim: multi-run and version-iteration evidence comes from prior session history and `clawhub-auto-publish` references, not raw logs inspected in this run.

**Sufficiency:** sufficient for this dogfood run, but a future release gate report should cite raw session links or release metadata if available.

### B. Identity — PASS

**Evidence:**

- Narrow scope: research prioritization only — decide whether a company deserves deeper research and what to check first.
- Explicit anti-scope exists as a standalone section: `## What This Will Not Do`.
- Anti-scope includes:
  - not financial advice
  - no buy/sell/hold verdicts
  - no price targets or fair value estimates
  - no portfolio-weight guidance
  - no claim to know Buffett's private view
  - say NEEDS INFO when facts are insufficient
- Not a generic assistant: the skill is specifically a research-prioritization assistant, not a broad investing assistant.

**Evidence source:** direct inspection.

**Sufficiency:** sufficient.

### C. Safety — PASS

**Evidence:**

- Skill explicitly says it is not financial advice.
- It does not produce buy/sell/hold calls.
- It does not give price targets or portfolio allocation guidance.
- Output categories are research-priority labels, not trading instructions:
  - Research Now
  - Watch
  - Skip
  - NEEDS INFO
- The copy-paste prompt says: `Do not give buy/sell advice.`

**Evidence source:** direct inspection.

**Sufficiency:** sufficient.

### D. UX — PASS, with local/public version caveat

**Evidence:**

- Activation is clear: `what Buffett would do with [company/ticker]`.
- Example exists: `what Buffett would do with Pop Mart`.
- Output contract is clear and compact: Decision / Check First / Paste This to an Agent.
- User-facing wording is not harsh; it is direct and restrained.
- Feedback path is short and placed near the end.

**Potential UX issue:**

- The local SKILL.md has no explicit install command. For a public ClawHub skill, lifecycle UX normally expects a copy-paste install command.
- However, this run inspected the local runtime skill, not necessarily the current public page. `clawhub inspect` shows public latest is `1.1.10`, while local is `1.1.6`.

**Evidence source:**

- direct inspection: local SKILL.md content.
- direct CLI verification: ClawHub latest version differs from local version.

**Sufficiency:** partial. UX content itself passes, but install command clarity cannot be fully judged from the stale local file. Public page should be checked before any release decision.

### E. Maintenance — UNCLEAR / SOFT FIX CANDIDATE

**Evidence present:**

- Feedback path exists: `DM me on X: @BeeGeeEth`.
- ClawHub has a newer public version (`1.1.10`) than the local file (`1.1.6`), proving post-release updates happened.
- Prior references indicate iteration around migration, feedback placement, activation clarity, install command clarity, and wording.

**Evidence unclear:**

- Local SKILL.md does not include changelog.
- ClawHub inspect output did not show changelog details in the short command output captured.
- Local file appears stale relative to public latest, so local source is not enough to evaluate current release maintenance.

**Evidence source:**

- direct CLI verification: public latest `1.1.10`, local `1.1.6`.
- direct inspection: local feedback path exists.
- reference-derived: historical iteration reasoning.

**Sufficiency:** not fully sufficient. Maintenance should be UNCLEAR unless public release metadata or release report is inspected.

## Hard Gate Blockers

No hard gate blocker found.

- Identity: PASS — standalone anti-scope exists.
- Safety: PASS — no financial advice / no buy-sell / no price targets / no allocation advice.
- Utility: PASS — recurring research-prioritization workflow.

## Soft Gate Fixes

Potential soft issues:

1. **UX / Install clarity:** local SKILL.md lacks explicit install command. Because local version is stale relative to public version, this requires public-page or current source verification before declaring FAIL.
2. **Maintenance / Changelog evidence:** changelog evidence not found in local SKILL.md or short inspect output. Needs ClawHub release metadata, release report, or reference file citation.
3. **Source-of-truth mismatch:** local runtime skill version `1.1.6` differs from ClawHub latest `1.1.10`. Lifecycle should warn when local source and public release diverge.

## Release Verification Steps

This dogfood run did not publish or re-release anything.

If evaluating `buffett-do` for a new release, the lifecycle should require:

```bash
clawhub inspect buffett-do
openclaw skills search "buffett"
openclaw skills install buffett-do
openclaw skills list
openclaw skills info buffett-do
openclaw skills check
```

Also verify the public page if possible. Because local and public versions differ, public-page verification is especially important before judging install command clarity or current user-facing wording.

## Post-release Iteration Actions

No change was applied to `buffett-do`.

Recommended iteration actions if this were a real release review:

1. Verify current public page content for `buffett-do` v1.1.10.
2. Confirm whether the public page includes a clear install command.
3. Locate changelog evidence in ClawHub release metadata, release report, or reference file.
4. If no changelog evidence exists, classify Maintenance as SOFT FAIL and create release-report discipline before future version bumps.
5. Decide whether local runtime skill should be synced to public latest or whether public latest lives in another source path.

## Reference Usefulness

`references/buffett-do-mini-example.md` was useful because it correctly predicted the relevant evaluation dimensions for a user-facing research skill:

- feedback placement
- activation clarity
- install command clarity
- no harsh user-facing wording
- anti-scope

Additional useful finding:

- The lifecycle should explicitly include a **source-of-truth check** when local skill content and ClawHub public version diverge.

## Was Any Output Actually Useful?

Yes.

This dogfood run produced useful output because it tested the lifecycle on a different scenario from `waste-audit`:

- `waste-audit` = internal OpenClaw utility skill
- `buffett-do` = user-facing research-prioritization skill

It also revealed a new lifecycle issue not seen in Dogfood Run #1:

- local/public version divergence can make release-readiness evaluation misleading unless source-of-truth is identified first.

## What Should Be Changed in Skill Release Lifecycle

Recommended future patch after review:

1. Add source-of-truth check to Release Verification:

   > If local SKILL.md and `clawhub inspect <slug>` show different versions, identify which file/source is authoritative before judging current public release quality.

2. Add install command caveat to UX:

   > If evaluating a local/private skill, missing public install command may be acceptable. If evaluating a public release, clear install path is required either in public page body or release instructions.

3. Add maintenance evidence caveat:

   > A newer ClawHub version proves iteration happened, but does not by itself prove changelog quality. Changelog evidence must still be cited.

## Does This Count Toward the 3-Run Public Release Threshold?

Yes — this counts as dogfood run #2 for `skill-release-lifecycle`.

Reason:

- It used a real published skill (`buffett-do`).
- It tested a user-facing research-prioritization skill, distinct from the internal OpenClaw utility case in Dogfood Run #1.
- It applied the A–E gate criteria end-to-end.
- It labeled evidence source quality.
- It separated hard blockers, soft fixes, release verification needs, and post-release iteration actions.
- It produced a new lifecycle improvement candidate: source-of-truth / local-public version divergence check.

Current lifecycle maturity after this run:

- Dogfood runs completed: 2
- Distinct scenarios: 2
  1. internal OpenClaw utility skill (`waste-audit`)
  2. user-facing research-prioritization skill (`buffett-do`)
- Public Candidate threshold not yet reached: requires 3 non-trivial dogfood runs across at least 2 distinct scenarios.
