---
name: puter-deployer
description: Deploy or update Puter-hosted web apps/sites with a CLI-first, verify-first workflow. Use when user asks to publish to Puter, update an existing Puter app/site, create a new Puter app from a build directory, troubleshoot failed Puter deployment, or prepare rollback. Trigger on phrases like "deploy to Puter", "publish Puter app", "update Puter site", "Puter deployment failed", or "rollback Puter deploy".
---

# Puter Deployer

Use a strict flow: preflight → build/stage → deploy path selection → verify → rollback note.

## 1) Preflight (always)

Run:

```bash
bash skills/puter-deployer/scripts/preflight.sh <project_dir> <build_dir>
```

This checks:
- `puter` CLI exists
- `puter whoami` works
- build directory exists and is non-empty
- `index.html` exists

If any check fails, stop and report exact fix commands.

## 2) Deployment path selection

Choose one path explicitly:

1. **Create new Puter app entry (CLI-supported):**
   - `puter app:create <name> <remoteDir> --description "..." --url "..."`
2. **Update/publish build content:**
   - Use Puter API fallback guidance in `references/api-fallback.md`.
   - If API details are unclear for this host/version, inspect active `puter-cli` source behavior before pushing.

Important: current public `puter-cli` command surface is limited. Do not invent non-existent commands.

## 3) Verify deployment (always)

Run:

```bash
bash skills/puter-deployer/scripts/verify_url.sh <url> [expected_snippet]
```

Require:
- HTTP 200
- expected snippet present (if provided)

If verification fails, mark deployment unsuccessful.

## 4) Rollback note (always)

Return these fields in final report:
- source commit
- previous known-good artifact path
- previous known-good URL
- exact rollback command/runbook

Use `scripts/deploy_report_template.md` as output skeleton.

## Guardrails

- Never print auth tokens.
- Never delete remote app/site without explicit user request.
- Require explicit confirmation before overwriting production targets.
- On failure, classify into one bucket:
  1) auth/session
  2) missing build artifact
  3) wrong app/site target
  4) platform/API error

## References

- `references/deploy-checklist.md` — end-to-end checklist
- `references/api-fallback.md` — API-first fallback logic when CLI is insufficient
- `references/failure-playbook.md` — common failure signatures + fixes
