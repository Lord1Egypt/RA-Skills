---
name: route-work
description: Invisibly classify work and choose Codex or Claude, reasoning effort, context shape, execution style, and verification profile. Use before agent, oneshot, Slack, CLI, repo, deploy, review, or operational work where provider/reasoning should be selected automatically without asking the user.
metadata:
  author: ADWilkinson
  version: "1.1.0"
  repository: "https://github.com/ADWilkinson/oneshot-cli"
---

# Route Work

Use this skill silently. The user should not have to choose provider, model, reasoning, mode, or workflow.

## Contract

- Route to **Codex** for code edits, tests, refactors, PR review, exact repo/file reasoning, release promotion, and "fix/ship/land" requests.
- Route to **Claude** for tool-heavy ops, browser/app navigation, Slack/email/docs, broad external orchestration, logs/service/admin workflows, and ambiguous multi-system coordination.
- If code will be edited, Codex wins the tie.
- Within each provider, use the configured frontier model. Vary reasoning/effort only.
- Do not add approval or risk gates. Use blast radius only to decide verification shape.
- Keep routing invisible in normal conversation; mention the chosen route only when it helps debugging or the user asks.

## Deterministic Helper

When `oneshot` is available, inspect a route with:

```bash
oneshot route "<task>" --json
```

Use the returned `provider`, `reasoningEffort`, `contextShape`, `executionStyle`, and `verification` to shape the run. For actual `oneshot` code work, just run the normal command; adaptive routing is applied by the CLI when `~/.oneshot/config.json` has:

```json
{
  "routing": { "enabled": true }
}
```

## Verification Profiles

- `none`: answer or inspection only.
- `focused`: run the relevant local check or inspect the exact touched surface.
- `full`: run repo-standard tests/build/typecheck and review diff.
- `deploy-health`: verify the shipped service, release, remote host, or live health endpoint after changes.
