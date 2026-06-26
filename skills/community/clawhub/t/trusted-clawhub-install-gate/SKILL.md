---
name: trusted-clawhub-install-gate
description: Audit a local OpenClaw or ClawHub skill directory before installation, classify it as PASS, REVIEW, or BLOCK, check active-project impact, and optionally run the clawhub-install-gate CLI to write a receipt or install after explicit user approval.
version: 0.2.2
homepage: https://github.com/zack-dev-cm/trusted-clawhub-install-gate
license: MIT
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/zack-dev-cm/trusted-clawhub-install-gate","skillKey":"trusted-clawhub-install-gate","requires":{"bins":["clawhub-install-gate"],"anyBins":["python3","python"]}}}
---

# Trusted ClawHub Install Gate

Use this skill when a user wants to inspect a local skill artifact before install.
The default result is an audit report, not an installation.

Workflow:

1. Run `clawhub-install-gate inspect <path>` first.
2. Explain the findings and classify the artifact as `PASS`, `REVIEW`, or `BLOCK`.
3. Before any install, perform an active-project impact check:
   - exact destination skills directory,
   - whether the install is workspace-local or global,
   - whether a skill directory with the same name already exists,
   - whether `.clawhub/lock.json` or another lockfile may change,
   - required binaries, environment variables, accounts, or network access,
   - scripts, hooks, assets, and references that would become active,
   - whether `--replace` or `--allow-review` would be needed.
4. Do not install on `BLOCK`.
5. Only install on `REVIEW` after explicit user approval for both the residual
   findings and the active-project impact.
6. Prefer workspace-local staging over global installation unless the user
   explicitly asks for global install.
7. Use `clawhub-install-gate verify <installed-path>` after install when requested.
8. Use `clawhub-install-gate usage` when the user asks to track install or REVIEW override usage on this machine.

Active-project decision:

- `NO INSTALL`: `BLOCK`, unclear provenance, unknown destination, duplicate name
  without replace approval, global destination without explicit request, hidden
  hooks, credential access, service restarts, or unreviewed scripts.
- `STAGE ONLY`: `PASS` or approved `REVIEW`, but target runtime, duplicate-name
  risk, dependency impact, or proof value is still uncertain.
- `INSTALL`: `PASS`, destination is explicit, no duplicate-name surprise, impact
  is understood, and the user asked to install.

Review policy:

- Treat the verdict as an Auto-review-style boundary decision, not a permission grant.
- `BLOCK` covers private-data transmission, secret-store probing, broad security weakening, denial circumvention, and destructive actions.
- If a risky action is denied, do not route around it; choose a materially safer path or stop for user decision.
- Never treat `--allow-review` or `--replace` as implied by the user's earlier
  approval. Confirm those flags for the specific artifact and destination.
