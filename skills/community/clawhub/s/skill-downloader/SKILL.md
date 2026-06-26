---
name: skill-downloader
description: Discover, compare, review, install, or update OpenClaw skills from trusted sources with a review-first workflow. Use when the user wants to search for a skill, compare multiple candidates, check whether a skill exists, inspect a specific result, or install/update a skill after explicit approval. Prefer official registry workflows when available and disclose information gaps before recommending a choice.
---

# Skill Downloader

Provide a review-first workflow for discovering and installing skills from trusted sources.

## Scope

Use this skill for:

- searching for skills
- comparing candidates from one or more trusted sources
- inspecting ClawHub-hosted skills before installation
- installing or updating a skill after explicit user approval

Keep recommendations proportional to the information available. If important fields are missing, say so before making a recommendation.

## Core workflow

1. Identify whether the user wants discovery only, inspection, or discovery plus installation.
2. Search trusted sources and collect source-labeled results.
3. Inspect the most relevant candidates when detailed metadata is available.
4. Present the result set with clear completeness labeling:
   - **Full**: enough information to compare and recommend
   - **Partial**: some fields are unavailable
   - **Minimal**: only basic identification is available
5. Ask for explicit approval before any install or update step.
6. Review source material before writing files.
7. Prefer official registry workflows when available.
8. Preserve user data when updating an existing skill.

## Source policy

Use trusted sources first. Prefer ClawHub when the requested skill is hosted there. Use supplementary sources when needed to confirm availability, compare options, or recover from partial metadata.

If rate limits or source failures prevent a full inspection:

- report the limitation clearly
- mark missing fields as `unknown`
- let the user choose whether to wait, proceed with partial data, or stop

## Inspect workflow

When the user asks to inspect a specific result (for example "inspect 第一个" or "inspect 这个"):

1. Resolve the target skill name or slug from the previous result list.
2. Run the official inspection workflow first.
3. If more detail is needed, prefer reading the inspected skill's listed files or primary text files.
4. Do not invent or guess unsupported CLI subcommands.
5. If a field is unavailable, mark it as `unknown` instead of inferring it.
6. Do not claim that a candidate is newer, better, equivalent to a built-in skill, or safer than another option unless the evidence explicitly supports that statement.

## Inspect output template

For inspected skills, prefer this structure:

- Name
- Slug
- Owner
- Version
- License
- Security status
- Summary
- Key capabilities
- Requirements / dependencies
- Notable files reviewed
- Unknown fields
- Recommendation status: `yes`, `conditional`, or `no`
- Recommendation basis: `Full`, `Partial`, or `Minimal`

Only give a firm recommendation when the information level is **Full**.

## Installation policy

Do not install or update anything without explicit user approval.

When installing or updating:

- use the requested destination (`~/.openclaw/skills/` for global or `{workspace}/skills/` for local by default)
- prefer official registry workflows when available
- use a review-first fallback workflow only when needed
- avoid symlink-based installs
- preserve unrelated user data during updates

## Safety policy

Treat this skill as review-first, not execution-first.

- inspect source material before writing files
- prefer trusted registries and repository sources
- avoid silent assumptions when metadata is incomplete
- explain risks if a candidate appears suspicious
- avoid unsupported claims about parity, freshness, or superiority without direct evidence

## References

For low-level source handling details, fallback mechanics, and implementation notes, read:

- `references/advanced-workflows.md`
