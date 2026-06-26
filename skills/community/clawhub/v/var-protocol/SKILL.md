---
name: var-protocol
description: Enforce Versioning, Archiving, and Rollback discipline for long-lived assets and multi-step delivery work. Use when editing codebases, websites, documents, decks, brand assets, prompts, configs, or any project artifact that needs safe iteration, backup-first handling, semantic version naming, changelogs, rollback anchors, or non-destructive updates. Trigger on requests about refactoring, major revisions, migration, redesign, rework, release packaging, version-control hygiene, or safe multi-agent collaboration. 中文简介：用于长期资产与多阶段交付的安全协作协议，核心是版本清晰、备份优先、遇错先回退，避免 destructive overwrite 导致资产丢失。
---

# V.A.R. Protocol

Apply V.A.R. whenever the cost of overwriting the wrong thing is higher than the cost of being slightly more disciplined.

## 中文简介

V.A.R. Protocol 是一个面向长期项目、重要资产和多阶段交付的协作规范。
它的核心原则是：**版本清晰（Versioning）、备份优先（Archiving）、遇错先回退（Rollback）**。
适用于网站改版、代码重构、文档/Deck 迭代、Prompt/Config 升级、多 Agent 协作等场景，目标是在推进迭代速度的同时，避免 destructive overwrite、内容丢失与不可逆回归。

V.A.R. stands for:
- **Versioning**
- **Archiving**
- **Rollback**

## What this skill is for

Use this skill to turn risky editing work into a safer delivery flow.
It is designed for code, content, design, and multi-agent execution where recoverability matters as much as speed.

Typical triggers:
- “Refactor this site without breaking the current version.”
- “Rewrite this proposal / deck, but keep a safe fallback.”
- “Migrate these prompts or configs and preserve rollback options.”
- “Have multiple agents work on the same long-lived asset safely.”
- “Package this release with a clear version, changelog, and rollback point.”

## Core operating sequence

Follow this order:
1. **Stabilize the baseline** — identify the current working version or last known good artifact.
2. **Back up before structural change** — create a restorable copy before large edits, refactors, migrations, or agent handoffs.
3. **Use explicit versions** — name outputs with clear semantic versions instead of vague labels like `final`, `latest`, or `new2`.
4. **Change incrementally** — prefer small, reversible modifications over full replacement.
5. **Attach a changelog** — state what changed, why, and what the rollback anchor is.
6. **Rollback first when broken** — if the new version regresses, restore the last stable version before attempting another merge.

## When to apply strict mode

Use the strictest form of V.A.R. when any of the following are true:
- The asset is long-lived or business-critical.
- Multiple agents or contributors are touching the same artifact.
- The task involves refactor, redesign, migration, or restructuring.
- The user may need to compare versions or recover prior work quickly.
- The output is a website, source tree, proposal, deck, prompt system, knowledge base, automation config, or brand asset set.

## Minimum operating requirements

Before making a high-impact change:
- Identify the artifact owner and the current stable version.
- Create a backup or duplicate that can be restored quickly.
- Decide the next semantic version.
- Preserve or document the rollback anchor.

During the change:
- Avoid destructive overwrite when a parallel version is feasible.
- Prefer additive or surgical edits over wholesale replacement.
- Keep filenames and folders readable and comparable.

At delivery:
- State the new version.
- Provide a concise change summary.
- Name the rollback anchor explicitly.
- Call out any known risks or incomplete areas.

## Default naming guidance

Prefer patterns like:
- `[project]-[artifact]-v1.0.ext`
- `[project]-[artifact]-v1.1.ext`
- `[project]-[artifact]-v1.1.1.ext`

Use version levels consistently:
- **Major**: architecture, structure, or strategy changed.
- **Minor**: meaningful feature/module expansion without core rewrite.
- **Patch**: small fixes, copy edits, image swaps, bug fixes.

## Delivery contract

When delivering work under V.A.R., include:
- **Version**
- **Change summary**
- **Rollback anchor**
- **Known risks** if any remain

## Failure handling

If the new version loses functionality, quality, or content:
1. Stop stacking more changes onto the broken version.
2. Restore or switch back to the last stable artifact.
3. Diagnose the failure from the stable baseline.
4. Re-apply only the needed changes in smaller slices.

## Multi-agent rule

The lead agent owns backup and rollback safety.
Do not assume a sub-agent already created a safe restore point unless it is explicitly confirmed.

## Read next

For the full protocol text, delivery checklist, and example delivery block, read `references/protocol.md`.
