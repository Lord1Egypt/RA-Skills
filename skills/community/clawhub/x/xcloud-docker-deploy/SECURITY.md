# Security Policy — xCloud Docker Deploy Skill

## Overview

This ClawHub skill is a documentation, template, and deployment-preparation package. It helps an AI agent analyze a user-approved project and prepare xCloud-ready deployment files such as Dockerfiles, `docker-compose.yml`, GitHub Actions workflow templates, and `.env.example` files.

The package itself does not run code automatically. Some templates it helps generate, such as GitHub Actions workflows or deployment webhooks, can perform real network and deployment actions after a user installs them in a repository. Those steps require explicit user confirmation.

## Why ClawHub May Flag This Skill

ClawHub's scanner may flag this package because:

1. It contains Dockerfiles and Docker Compose templates.
2. It contains GitHub Actions workflow templates that can build and push images to GHCR.
3. It discusses deployment webhooks and live xCloud API skills.
4. It documents private API token handling for `XCLOUD_API_TOKEN`.
5. It helps agents create or modify deployment files after user approval.

**Verdict: expected deployment-skill behavior, with explicit safety gates. This package contains no malware, no real credentials, and no executable installer.**

## File-by-File Analysis

| File/Folder | Type | Risk Notes | Safety Boundary |
|---|---|---|---|
| `SKILL.md` | Agent instructions | Guides project inspection and file generation | Requires user confirmation before inspection, edits, token handling, or live API routing |
| `README.md` | Human documentation | Documents deployment flows | Includes confirmation, backup, staging, and token safety guidance |
| `DETECT.md` | Stack detection reference | Read-only fingerprint rules | No execution |
| `references/*.md` | Scenario/reference docs | May show deploy commands or webhook patterns | Examples only; user must approve before use |
| `dockerfiles/*.Dockerfile` | Dockerfile templates | Build instructions for generated images | Templates only; not executed by install |
| `compose-templates/*.yml` | Compose templates | Deployment configuration templates | Templates only; users review before applying |
| `assets/github-actions-build.yml` | GitHub Actions template | Can build/push to GHCR if copied into a repository | Requires repository owner approval; uses GitHub-provided `GITHUB_TOKEN` |
| `examples/*.md` | Example walkthroughs | May include git push or deployment steps | Examples only; production safety gate applies |
| `skill.json` | Machine-readable metadata | Describes capabilities and safety boundaries | No secrets |
| `.clawhubsafe` | Checksum attestation | Integrity manifest | Verifiable with `sha256sum -c .clawhubsafe` |

## Consent Gates

Agents using this skill must separate read-only analysis from change-making actions.

Before project inspection:

- Confirm that the user wants the agent to inspect the project files.

Before file generation or modification:

- Confirm the exact files to create or edit.
- Prefer a feature branch or pull request.
- Show the generated Dockerfile, compose file, workflow, and `.env.example` before the user applies them.

Before production-impacting actions:

- Confirm whether the target is staging or production.
- Ask whether a backup exists for production sites/databases.
- Do not trigger deployment webhooks, migrations, DNS changes, SSL changes, cache clears, or live API mutations without a separate final confirmation.

Before token collection or live xCloud API routing:

- State the exact live operation.
- Prefer least-privilege and short-lived tokens where possible.
- Ask for the token only after the user approves that exact operation.
- Never print, store, log, reuse, or commit the token.

## What This Skill Does NOT Do

- Does not include real API keys, tokens, passwords, or private URLs.
- Does not include binaries, installers, or background services.
- Does not execute Docker, GitHub Actions, webhooks, or xCloud API calls by itself.
- Does not collect telemetry.
- Does not persist credentials.
- Does not automatically modify user files.

## Generated Output Security

The skill may guide agents to generate:

1. **Modified `docker-compose.yml`** — removes unsupported `build:` directives, proxy services, or unsafe host port bindings for xCloud.
2. **GitHub Actions workflow** — uses GitHub's repository-scoped `GITHUB_TOKEN` for GHCR pushes. `packages: write` is required only when the user approves image publishing.
3. **`.env.example`** — lists variable names only. It must never contain real values.
4. **Optional webhook step** — only when the user explicitly configures a deployment webhook secret and confirms the action.

## Verification Instructions

```bash
# Verify checksums:
sha256sum -c .clawhubsafe

# Verify no common secret patterns:
grep -rE "(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{20,}|BEGIN (RSA|OPENSSH|PRIVATE) KEY)" . --exclude-dir=.git
# Expected: no output
```

## Reporting Vulnerabilities

If you find a security issue with this skill or its generated output, open an issue at:
https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill/issues

## Provenance

- Source: https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill
- ClawHub: https://clawhub.ai/Asif2BD/xcloud-docker-deploy
- Author: M Asif Rahman / Asif2BD
- Security review updated by: Oracle (Matrix Zion) — 2026-06-23
