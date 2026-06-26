---
name: safe-install
description: Install OpenClaw skills through policy validation, ClawShield scanning, snapshot storage, and rollback controls.
homepage: https://github.com/mike007jd/openclaw-skills/tree/main/safe-install
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["node"]}}}
---

# Safe Install

Add a local security review layer in front of skill installation.

## When to use

- You want policy-driven review before activating a local skill.
- You need ClawShield scanning and human approval for medium or high risk findings.
- You want rollback-ready snapshots and install history for locally managed skills.

## Commands

```bash
node {baseDir}/bin/safe-install.js /path/to/skill --config ./policy.json --store ./.openclaw-tools/safe-install
node {baseDir}/bin/safe-install.js /path/to/skill --yes
node {baseDir}/bin/safe-install.js /path/to/skill --force
node {baseDir}/bin/safe-install.js history --format table
node {baseDir}/bin/safe-install.js rollback my-skill
node {baseDir}/bin/safe-install.js policy validate --file ./policy.json
```

## Review flow

1. **Source validation**: check the candidate against `allowedSources`.
2. **Pattern blocking**: reject candidates that match a blocked regular expression.
3. **ClawShield scan**: scan before install.
4. **Risk review**:
   - `Safe`: install directly
   - `Caution`: require `--yes` or interactive approval
   - `Avoid`: require `--force`
5. **Snapshot storage**: save a hashed snapshot for rollback.

## Policy file

`.openclaw-tools/safe-install.json`:

```json
{
  "defaultAction": "prompt",
  "blockedPatterns": ["curl\\s*\\|\\s*sh"],
  "allowedSources": ["clawhub.com", "/local/skills"],
  "forceRequiredForAvoid": true
}
```

- `defaultAction`: allow/prompt/block
- `blockedPatterns`: regular expressions that reject installation
- `allowedSources`: source allowlist
- `forceRequiredForAvoid`: whether `Avoid` requires `--force`

## Storage

```
.openclaw-tools/safe-install/
├── snapshots/{skill}/{version}/{hash}/  # stored snapshots
├── active/{skill}/                       # current active version
├── state.json                           # active state
└── history.json                         # install history
```

## Limits

- Maximum file size: 100MB
- Maximum files per skill: 10,000
- Maximum total skill size: 500MB
- Path traversal protection is enforced

## Boundaries

- Safe Install currently resolves local directories or registry aliases defined in policy. It is not a full remote ClawHub client.
- This tool adds a local control layer; it does not replace OpenClaw's native `skills install` flow.
