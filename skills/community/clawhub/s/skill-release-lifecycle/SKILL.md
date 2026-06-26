---
name: skill-release-lifecycle
description: "A lightweight release-quality workflow for OpenClaw / ClawHub skills. Use when deciding whether a skill is ready to publish, verifying a release, and turning post-release feedback into actionable updates."
version: 0.1.3
status: public-experimental
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [workflow-kit, release-lifecycle, skill-quality, openclaw, clawhub, feedback-loop]
    related_skills: [hermes-agent-skill-authoring, clawhub-auto-publish, waste-audit]
---

# Skill Release Lifecycle

A lightweight release-quality workflow for OpenClaw / ClawHub skills.

## Install

```
openclaw skills install skill-release-lifecycle --global
```

## Features

🚦 **Release Readiness Gate**: decide whether a skill is ready to publish or should stay private.

🔍 **Release Verification**: check install path, activation, safety, metadata, and public-page status after release.

🔁 **Feedback → Iteration Loop**: turn feedback into ignore / patch / version bump / reposition / deprecate decisions.

🧩 **Prompt for Agent**: generate a copy-paste prompt you can give to your agent for further release improvement.

## What This Will Not Do

* It does not write SKILL.md from scratch.
* It does not run ClawHub publish commands directly.
* It does not replace clawhub-auto-publish.
* It does not optimize ClawHub ranking, downloads, stars, or homepage placement.
* It does not certify a skill as stable or fully validated.

## How It Works

### 1. Release Readiness Gate

Check five things before release: utility, identity, safety, UX, and maintenance.

**Hard fail:**
* no recurring use case
* no anti-scope
* unsafe default behavior
* secret exposure
* destructive behavior without explicit protection

**Soft fix:**
* unclear install command
* unclear activation
* unclear output format
* missing feedback path
* weak version/update explanation

### 2. Release Verification

**Before publishing**, check local SKILL.md, title, summary, install command, activation, anti-scope, safety, and release status.

**After publishing**, verify with ClawHub / OpenClaw evidence where available:
```
clawhub inspect <slug>
openclaw skills search "<keyword>"
openclaw skills install <slug>
openclaw skills info <slug>
openclaw skills check
```

Public page check if accessible.

If the public page is blocked, report BLOCKED, not PASS.

### 3. Feedback → Iteration Loop

Classify feedback as:
* bug
* confusing activation
* missing install path
* scope too broad
* missing anti-scope
* safety concern
* output mismatch
* UX wording issue
* strategic repositioning
* not worth acting on

Then choose:
* ignore / log only
* docs patch
* minor wording patch
* version bump
* major repositioning
* deprecate / merge
* keep private

## Prompt for Agent

Copy this prompt into your agent:

```
Run the skill-release-lifecycle gate on <skill-name/slug>.

Inspect the current SKILL.md. For each gate (Utility, Identity, Safety, UX, Maintenance), write Pass / Fail / Unclear with a one-line reason and label your evidence source (direct inspection / reference-derived / historical claim / unverified).

If any hard gate fails, do not publish. If soft gates fail, patch within the same session before publishing.

After patching, run:
- clawhub inspect <slug>
- openclaw skills search "<keyword>"
- openclaw skills install <slug>
- openclaw skills info <slug>

Report exact evidence: commands run, observed output, files changed, version bumped, and unresolved blockers.

Do not claim public page verification if it was blocked.
```

## Related Skills

* `hermes-agent-skill-authoring` — SKILL.md authoring, frontmatter, validator rules
* `clawhub-auto-publish` — detailed ClawHub publish mechanics and CLI flow
* `waste-audit` — reference implementation used in examples

## Feedback

Found an issue or have feedback?
DM me on X: @BeeGeeEth