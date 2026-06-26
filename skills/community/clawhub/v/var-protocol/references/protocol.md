# V.A.R. Protocol Reference

## Purpose

Use V.A.R. to prevent asset loss and regression during ongoing work.
Apply it whenever iteration speed must coexist with recoverability.

V.A.R. = **Versioning + Archiving + Rollback**.

## Quick examples

Apply V.A.R. in situations like:
- rewriting a landing page without losing the last working version
- restructuring a codebase while preserving a rollback point
- updating a proposal deck while keeping the prior client-safe version
- revising prompts, agent instructions, or knowledge assets without destructive overwrite
- coordinating multi-agent edits where the lead agent must preserve recovery paths

## 1. Versioning

### Intent
Make every important artifact identifiable, comparable, and recoverable.

### Rules
- Use semantic version labels instead of ambiguous names.
- Keep naming human-readable.
- Make the current version obvious from the filename or delivery note.

### Recommended patterns
- `project-artifact-v1.0.ext`
- `project-artifact-v1.1.ext`
- `project-artifact-v1.1.1.ext`

### Version meaning
- **Major** (`v2.0`) — architecture or strategic structure changed.
- **Minor** (`v1.2`) — meaningful addition on the same base.
- **Patch** (`v1.1.3`) — localized fix or polish.

### Avoid
- `final`
- `latest`
- `new`
- `updated2`
- date-only naming without a semantic version when the artifact is actively iterated

## 2. Archiving

### Intent
Ensure the last stable version remains recoverable before risky edits.

### Rules
- Back up before structural edits, migrations, refactors, or mass rewriting.
- Treat destructive overwrite as the exception, not the default.
- Preserve at least one clearly restorable prior version.
- In multi-agent work, require the lead agent to verify the backup exists.

### Good backup patterns
- Duplicate the last stable file with a versioned suffix.
- Preserve the prior folder or branch before rework.
- Snapshot critical prompts, configs, generated assets, or source trees.

### Archiving checklist
Before major change, confirm:
- What is the current stable artifact?
- Where is the backup?
- Who owns rollback authority?
- What will the next version be called?

## 3. Rollback

### Intent
Recover quickly when a new version regresses.

### Rules
- Roll back first when the new output breaks core functionality or loses content.
- Do not continue layering changes onto a broken baseline.
- Rebuild from the last stable version in smaller increments.

### Trigger conditions
Rollback-first is the default when any of these happen:
- lost features
- missing sections or assets
- broken structure
- quality collapse
- unexpected visual regressions
- invalid configuration or deployment breakage

### Rollback routine
1. Identify the last stable artifact.
2. Restore or rename it back into the active slot.
3. Record what failed.
4. Re-apply only necessary deltas.
5. Re-deliver with a new version and changelog.

## Delivery contract

When delivering work under V.A.R., include:
- **Version** — the current version label
- **Change summary** — what changed
- **Rollback anchor** — the prior stable artifact or restore point
- **Known risks** — optional but recommended

Example:

- Version: `site-homepage-v1.3`
- Change summary: updated hero copy, pricing section, FAQ layout
- Rollback anchor: `site-homepage-v1.2`
- Known risks: mobile spacing on small screens still needs QA

## Reusable delivery block

Use a compact block like this in final handoff notes:

- **Version:** `project-artifact-vX.Y`
- **Change summary:** one-sentence description of what changed
- **Rollback anchor:** `project-artifact-vX.(Y-1)` or path/branch/snapshot name
- **Known risks:** optional

## Strict-mode scenarios

Use strict V.A.R. by default for:
- websites and landing pages
- codebases and scripts
- business plans and proposal decks
- prompt systems and agent instructions
- knowledge bases and indexed content
- design systems, logos, and brand assets
- automation configs and production workflows
- multi-agent or multi-stage delivery

## Agent collaboration policy

- The lead agent owns restore safety.
- A sub-agent may help execute, but cannot be assumed to have created a safe backup unless explicitly verified.
- Handoffs should include version, current status, risks, and rollback anchor.

## Practical operating principle

**Back up first. Version clearly. Roll back early. Merge carefully.**
