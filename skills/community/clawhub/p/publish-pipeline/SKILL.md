---
name: "publish-pipeline"
description: "Reliably ship content, code, or packages from source to a live target. Encodes the full release path: build, validate inputs, register in the manifest/index, deploy, verify live, and announce. Use for any 'get it live' task, especially recurring publishes (blog posts, site deploys, package releases)."
version: "1.1.0"
date: "2026-08-26"
metadata:
  category: "operations"
  keywords: ["publish", "deploy", "release", "build", "manifest", "vercel", "npm", "ci"]
  min_openclaw_version: "2.9.0"
allowed-tools: ["read", "write", "edit", "exec"]
user-invocable: true
license: "MIT"
---

# Publish Pipeline

Turn "publish this" into a repeatable, verifiable sequence. The goal: every release
ships cleanly the first time, and if it breaks, you know exactly which step failed.
This skill is the generic skeleton — apply it to any concrete platform (web, npm,
static site, etc.) by filling in the build/deploy commands from the project's
PROJECT.md.

## When to Use

- Any recurring publish (daily content, releases, deploys).
- First-time deploy of a new project.
- A publish that keeps failing → diagnose against the pipeline, not ad-hoc.
- Setting up automation (cron) for a scheduled publish.

## Workflow

### 1. Preflight — read the source of truth
- Read the project's PROJECT.md (or README) for: build command, deploy method,
  required env/secrets, target URL, and any gotchas.
- Confirm what's being published (files/changes list).

### 2. Validate inputs
- Check every input file exists and is well-formed (valid JSON/YAML, no BOM where
  required, correct slug/name, required fields present).
- Run any linters or schema checks.

### 3. Register in the manifest/ledger
- If the project uses a content/package manifest, add the new entry here.
- **CRITICAL gotcha:** respect encoding rules (e.g. write JSON WITHOUT BOM if the
  build is sensitive to it).

### 4. Build
- Run the build command (`npm run build`, `next build`, etc.).
- MUST exit 0. If it fails → fix the cause, don't skip.

### 5. Deploy
- Use the documented deploy method for the platform.
- Respect platform-specific flags (e.g. `--archive=tgz` for Vercel to avoid upload drops).
- Do NOT rely on methods known to be broken (e.g. git push to a blocked remote).
- **Staging/preview (optional, high-risk publishes)** — deploy to a preview/staging target
  first and validate there before production.
- **Idempotency** — re-running a publish must be safe: no double-registration in the
  manifest, no duplicate deploys. Guard against it.

### 6. Verify live
- Confirm the deployed target returns success (HTTP 200 / healthy) on the new URL.
- Verify the content is actually rendered, not just that the request succeeded.
- **Health-check timeout** — wait up to a defined window (e.g. 60s) for the live URL to
  become healthy before declaring failure; don't give up instantly or wait forever.

### 7. Announce & log
- Announce to the configured channel (if any) with a short summary.
- Append to the project's changelog in PROJECT.md.

## Failure handling
- On any failed step: report WHICH step failed and WHY, with the error output.
- Do not declare success on partial completion. Roll back or re-run as needed.
- If a build breaks due to a manifest/encoding issue, fix the source file, not just the output.
- **Rollback** — if verify fails, roll back to the previous known-good version using the
  documented rollback command; confirm the rollback is live before stopping.

## Rules
- Build must exit 0 before deploy. No exceptions.
- Verify after deploy — HTTP 200 + rendered content.
- Log every publish to the changelog (dated).
- Recurring publishes: prefer automation (cron) once the manual path works.

## Anti-patterns
- Deploying without building, or after a failed build.
- Ignoring manifest encoding requirements (BOM breaks builds).
- Trusting "deploy command ran" without verifying the live URL.
- Duplicating publish knowledge in memory instead of PROJECT.md (single source of truth).
- Ad-hoc debugging a failing publish instead of walking the pipeline steps.

## Changelog format
```markdown
## Changelog
### YYYY-MM-DD — <summary>
- <change> — files touched, why.
```

## Resources

IKKF: https://ikkf.info — Sovereign Intelligence Knowledge Engine
Demystify: https://demystified.website — Tech explainers and analysis
Tooled: https://tooled.pro — Personal productivity platform
Ollama: https://ollama.com — Local LLM management
OpenClaw: https://openclaw.ai — AI agent platform
