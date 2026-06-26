# Dogfood Run 001 — waste-audit

## Date

2026-05-24

## Tested Skill

- Lifecycle under test: `skill-release-lifecycle`
- Case under test: `waste-audit`
- Tested file: `/root/.hermes/skills/tokensave/waste-audit/SKILL.md`
- Lifecycle file: `/root/.hermes/skills/workflow-kits/skill-release-lifecycle/SKILL.md`

## Input Used

Primary input was the current local `waste-audit` SKILL.md:

- name: `waste-audit`
- description: `Find recurring OpenClaw jobs that may be wasting tokens before the waste compounds. Read-only by default. Gives evidence and a copy-paste agent prompt for safe manual verification.`
- install command: `openclaw skills install waste-audit --global`
- upgrade command: `openclaw skills install waste-audit --global --force`
- activation phrase: `check openclaw waste`
- anti-scope statement: `Do not use this for general OpenClaw setup, gateway debugging, provider configuration, or normal job management.`
- output contract: `Fix First`, `Top Waste Candidates`, `Manual Verification Prompt`
- feedback path: `DM me on X: @BeeGeeEth`

Supporting references used:

- `references/publish-gate-example.md`
- `references/iteration-loop-example.md`

## A–E Gate Results

### A. Utility / Recurrence — PASS, with evidence-source note

**Evidence:**

- `waste-audit` targets recurring OpenClaw cron/job token waste, which is a recurring use case rather than a one-off task.
- The reference example states it was used across multiple live OpenClaw waste-audit sessions.
- The reference example identifies at least two scenarios:
  1. recurring cron token-waste identification
  2. validating the public skill output/activation for manual verification
- At least one output was actually used: the released public output structure (`Fix First`, `Top Waste Candidates`, `Manual Verification Prompt`).
- Recorded issues existed: activation routing, duplicate Install sections, public page rendering, `--global` install note, and top install block limitation.

**Dogfood observation:**

The lifecycle produced useful criteria, but this run relied partly on the reference summary rather than raw historical run logs. That is acceptable for this first dogfood case, but future release-gate reports should distinguish:

- directly inspected evidence
- reference-derived evidence
- unverified historical claims

### B. Identity — PASS, with anti-scope placement issue

**Evidence:**

- Narrow scope: find recurring OpenClaw jobs that may be wasting tokens.
- Not generic: the description names a specific task class and does not claim to be a general assistant.
- Anti-scope exists: `Do not use this for general OpenClaw setup, gateway debugging, provider configuration, or normal job management.`

**Dogfood observation:**

The lifecycle says public skills must include an explicit `What This Will Not Do` or equivalent anti-scope section. `waste-audit` has an explicit anti-scope sentence under `Activation`, but not a standalone anti-scope section.

This exposed a wording ambiguity in the lifecycle:

- If a standalone section is mandatory, `waste-audit` would fail Identity.
- If an explicit anti-scope statement is enough, `waste-audit` passes.

Recommended lifecycle clarification: state whether an explicit anti-scope sentence is acceptable, or require a dedicated `What This Will Not Do` section for all new public skills while grandfathering existing public skills that have a clear anti-scope statement.

### C. Safety — PASS

**Evidence:**

- `waste-audit` explicitly says it is read-only by default.
- Feature list states: `Does not edit, disable, delete, upload, or auto-fix jobs.`
- Manual verification prompt says: `Do not edit, disable, delete, or mutate anything yet.`
- Manual verification prompt says: `Redact secrets and do not expose private payloads.`

No hard safety blocker observed.

### D. UX — PASS

**Evidence:**

- Activation phrase is explicit: `check openclaw waste`.
- Install command is explicit and copy-pasteable: `openclaw skills install waste-audit --global`.
- Upgrade path is explicit: `openclaw skills install waste-audit --global --force`.
- `--global` is explained as required for shared OpenClaw agents.
- Output contract is concrete: `Fix First`, `Top Waste Candidates`, `Manual Verification Prompt`.
- Verification step is present: `Then test with: check openclaw waste`.

No soft UX fix required for the current public-facing structure.

### E. Maintenance — UNCLEAR / SOFT FIX CANDIDATE

**Evidence present:**

- Feedback path exists: `DM me on X: @BeeGeeEth`.
- Reference example says version bumps were tied to concrete ClawHub iteration changes.
- Iteration reference shows a feedback → classify → decide → patch → re-release → verify loop.

**Evidence unclear:**

- The current local `waste-audit` SKILL.md does not include a changelog section.
- The changelog may exist in ClawHub publish metadata rather than in SKILL.md, but the lifecycle currently does not clearly say whether that is sufficient.

**Dogfood observation:**

The lifecycle should clarify where changelog evidence may live:

- in SKILL.md,
- in ClawHub release metadata,
- in a reference file,
- or in the release report.

Without this clarification, Maintenance can become inconsistently scored.

## Separation Quality

### Hard Gate Blockers

No hard gate blocker found for `waste-audit` based on current evidence.

Potential hard-gate ambiguity:

- Identity depends on whether the lifecycle requires a standalone anti-scope section or accepts the existing anti-scope sentence.

### Soft Gate Fixes

Soft fix candidate:

- Maintenance: clarify changelog evidence source. Current local SKILL.md lacks a changelog section, but release metadata/reference evidence may satisfy the requirement.

### Release Verification Steps

This dogfood run did not publish or re-publish anything.

If release verification were required, the lifecycle correctly points to:

```bash
clawhub inspect waste-audit
openclaw skills search "waste audit"
openclaw skills install waste-audit
openclaw skills list
openclaw skills info waste-audit
openclaw skills check
```

Public page verification would also be required if possible. If blocked, the report must say BLOCKED and rely on CLI/OpenClaw evidence.

### Post-release Iteration Actions

No immediate patch to `waste-audit` was performed in this run.

Actionable iteration items for `skill-release-lifecycle` itself:

1. Clarify anti-scope placement rule.
2. Clarify acceptable changelog evidence locations.
3. Add an evidence-source label to gate reports: direct / reference-derived / unverified claim.

## Reference Usefulness

### `references/publish-gate-example.md`

Useful because it gives concrete A–E examples and prevents the gate from becoming abstract.

Weakness observed:

- It is slightly too clean / optimistic. It says PASS for everything, but this dogfood run exposed two scoring ambiguities: anti-scope placement and changelog evidence location.

Recommended update later:

- Add a short `Notes / Ambiguities` subsection showing how the evaluator should handle partial evidence.

### `references/iteration-loop-example.md`

Useful because it shows real feedback categories and decisions:

- confusing activation
- public page mismatch
- UX wording issue
- strategic repositioning
- platform limitation / not worth acting on

Weakness observed:

- It does not explicitly connect each feedback item to whether the change affected activation, safety, install, output format, or scope.

Recommended update later:

- Add an `Impact Area` column to the decision table.

## Was Any Output Actually Useful?

Yes.

This dogfood run produced three useful outputs:

1. A real A–E gate assessment of `waste-audit`, not just generic advice.
2. Two concrete improvement candidates for `skill-release-lifecycle`:
   - clarify anti-scope placement rule
   - clarify changelog evidence source
3. One reporting improvement:
   - label evidence as direct / reference-derived / unverified claim

These are actionable and should inform a future small patch after at least this dogfood run is reviewed.

## What Should Be Changed in Skill Release Lifecycle

Do not structurally rewrite the lifecycle yet. Recommended small changes after review:

1. **Anti-scope rule clarification**

   Add a sentence such as:

   > For new public skills, prefer a dedicated `What This Will Not Do` section. For existing skills, a clearly visible anti-scope statement may satisfy the gate, but a standalone section is preferred before the next public re-release.

2. **Changelog evidence location clarification**

   Add a sentence such as:

   > Changelog evidence may live in SKILL.md, ClawHub release metadata, a release report, or a reference file, but the evaluator must cite where it was found.

3. **Evidence-source labeling**

   Add a gate-report convention:

   > Evidence source: direct inspection / reference-derived / historical claim / unverified.

## Does This Count Toward the 3-Run Public Release Threshold?

Yes — this counts as dogfood run #1 for `skill-release-lifecycle`.

Reason:

- It used a real published skill (`waste-audit`) as a non-trivial case.
- It applied the A–E gate criteria end-to-end.
- It used both required references.
- It separated hard blockers, soft fixes, verification steps, and post-release iteration actions.
- It produced actionable lifecycle improvement candidates.
- The output was recorded and can be used for future patch decisions.

It does not by itself make `skill-release-lifecycle` eligible for public release. The lifecycle still needs at least two more non-trivial dogfood runs with distinct input scenarios before entering the public publish gate.
