# Validator Agent

Multi-round automated validation pipeline for TypeScript/Solidity projects. Runs 8 rounds of checks before any publish or deploy: compile gate, lint, test suite, security audit, type coverage, docs, changelog, and final review.

**The gold standard** — catches what manual review misses. Originally built to validate the agent-wallet-sdk before every npm publish. Now available as a reusable skill for any project.

## When to Use

- Before `npm publish` — run the full 8-round validation
- Before merging a PR — run as a quality gate
- After a dependency update — verify nothing regressed
- On any TypeScript or Solidity project in the workspace

## Quick Start

```
Run the Validator Agent on skills/agent-nexus-2/agent-wallet-sdk
```

Or trigger specific rounds:

```
Run Validator Agent round 0 (compile gate) on projects/mastra-plugin
```

## The 8 Rounds

### Round 0 — Compile Gate (BLOCKING)
```bash
cd <project> && npx tsc --noEmit 2>&1
```
**If this fails, ALL subsequent rounds are BLOCKED.** Nothing proceeds until compile is clean. This was added after a Feb 20 incident where broken types were published to npm.

### Round 1 — Lint
```bash
cd <project> && npm run lint 2>&1 | tail -20
```
Check for lint errors. Warnings are noted but don't block. Errors block.

### Round 2 — Test Suite
```bash
cd <project> && npm test 2>&1
```
Capture: total tests, passing, failing, skipped. Compare against baseline in `ops/test-baselines.md` if it exists. **Any test count drop = regression = BLOCK.**

### Round 3 — Security Audit
```bash
cd <project> && npm audit 2>&1 | tail -15
```
- 0 vulnerabilities → ✅ PASS
- Moderate only (transitive) → ⚠️ WARN (note but don't block)
- HIGH or CRITICAL → 🚨 BLOCK

### Round 4 — Type Coverage
```bash
cd <project> && npx type-coverage 2>&1 || echo "type-coverage not installed — skip"
```
If available, report percentage. Target: >95%. Below 90% = WARN.

### Round 5 — Documentation Check
- Does `README.md` exist and reference current version?
- Does `CHANGELOG.md` have an entry for the version being published?
- Are all exported functions documented?

### Round 6 — Changelog Verification
- Read `package.json` version field
- Read `CHANGELOG.md` — does it have an entry matching that version?
- If no changelog entry for current version → BLOCK publish

### Round 7 — Final Review Summary
Aggregate all rounds into a single verdict:

```
# Validator Agent Report — [project] — [timestamp]

## Verdict: [✅ PASS / ⚠️ WARN / 🚨 BLOCK]

| Round | Check | Result |
|-------|-------|--------|
| 0 | Compile | ✅/❌ |
| 1 | Lint | ✅/⚠️/❌ |
| 2 | Tests | ✅ X/X passing / ❌ regression |
| 3 | Security | ✅/⚠️/🚨 |
| 4 | Type Coverage | ✅ X% / ⚠️ / skipped |
| 5 | Docs | ✅/⚠️ |
| 6 | Changelog | ✅/❌ |
| 7 | Summary | [verdict] |

## Blocking Issues
[list or "None"]

## Warnings
[list or "None"]

## Recommendation
[PUBLISH / FIX FIRST / DO NOT PUBLISH]
```

Save report to: `ops/reports/validator-YYYY-MM-DD-HH-[project].md`

## Configuration

The skill auto-detects project type from:
- `package.json` → TypeScript/Node project
- `foundry.toml` → Solidity/Forge project

For Solidity projects, Round 0 uses `forge build` instead of `tsc`, Round 2 uses `forge test`, and Round 3 uses `forge audit` (if slither is available).

## Authority
- This skill is **read-only** — it checks and reports, never modifies code
- It produces a recommendation, never auto-publishes
- Max or Bill must approve the publish after reviewing the report
