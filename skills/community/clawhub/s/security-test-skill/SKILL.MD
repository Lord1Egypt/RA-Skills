---
name: security-test-skill
version: 1.0.0
description: Harmless canary skill for authorized supply-chain security research. Ships a single execute() tool that always returns one fixed success JSON; used as an end-to-end smoke test for skill registry publish/import/install/invoke pipelines (OfficeAce SkillHub). No network, no filesystem, no subprocess, no attack logic.
---

# Security Test Skill

A harmless supply-chain security test sample (canary skill), for **authorized** security research only. Purpose: verify whether a skill marketplace (OfficeAce SkillHub) behaves as expected across the full distribution chain — publish → import → install → invoke — and serve as a harmless control sample in supply-chain vulnerability experiments.

## Use Cases

- End-to-end smoke test of the skill publishing workflow
- Verify that tools are correctly registered and invocable after installation
- Harmless control sample in supply-chain propagation experiments (behavior is fully deterministic)

## Tool Interface

This skill ships exactly one tool, `execute` (`tool.js`):

```js
execute(params) → {
  success: true,
  message: "Test skill executed",
  note: "This is harmless"
}
```

- Input: any `params`; never read, parsed, or persisted
- Output: a **fixed** JSON, independent of input
- Behavior boundary: no network access, no filesystem access, no subprocess, no persistence, no environment probing

## Four-Stage Test Workflow

### 1. Collection (Preparation)

```text
□ Confirm written authorization and scope for the target SkillHub
□ Record target version, import endpoint, and test account
□ Prepare a controlled verification host (isolated, with egress observability)
```

### 2. Examination (Publish Verification)

```text
□ Publish this skill; confirm frontmatter (name/version/description) parses
□ Verify manifest completeness: SKILL.MD, tool.js, package.json
□ Record SHA256 of the published artifact
```

### 3. Analysis (Import & Invoke Comparison)

```text
□ Perform import/install from the controlled environment
□ Confirm `execute` appears in the tool list
□ Invoke execute and diff the response against the fixed JSON above, field by field
□ Capture traffic (proxy/pcap) for the whole session to confirm zero outbound connections
```

### 4. Reporting (Conclusion)

```text
□ Record the timeline: published → visible → invocable
□ Attach evidence: raw responses, screenshots, hashes
□ Conclude whether the chain behaved as expected; list deviations separately
```

## Verification Checklist

- [ ] Publish succeeds and manifest metadata parses
- [ ] `execute` appears in the tool list after import
- [ ] Invocation returns exactly the fixed JSON
- [ ] Zero outbound connections, zero file writes

## Boundaries and Red Lines

- Authorized testing only; never distribute this sample to unauthorized third-party systems
- This skill contains no real attack logic, and future modifications must **not** add any
- Target endpoints, accounts, and credentials observed during testing must never enter committed content

## Version

| Version | Notes |
|---------|-------|
| 1.0.0 | Initial sample: single `execute` tool, fixed success response |
