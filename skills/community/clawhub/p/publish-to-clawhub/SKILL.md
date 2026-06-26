---
name: publish-to-clawhub
description: |
  Prepare and publish a local skill to ClawHub and GitHub using a workflow that keeps the local publish directory clean.

  Use this skill when the user wants to update an already published skill, release a local skill safely, improve the skill structure before publishing, or keep GitHub as a backup and showcase without leaving README files in the local publish folder.
---

# Publish To ClawHub

Use this skill when a local skill should be updated, published, and backed up with a clean repeatable workflow.

Typical requests:

- "Publish this skill to ClawHub."
- "Help me put this skill on GitHub and ClawHub."
- "Improve this skill, publish it, then sync GitHub."
- "Keep the local skill folder clean but still show a README on GitHub."

## Safety First

This workflow can involve:

- structural edits to the skill itself
- GitHub authentication
- git push to a public remote
- ClawHub CLI publishing

Rules:

- never ask the user to paste a long-lived token into chat unless there is no safer option
- prefer browser login, credential manager, or SSH when available
- never store credentials in files
- never force-push without explicit user confirmation
- prefer a temporary GitHub README over leaving `README.md` in the local publish directory

## Prerequisites

Confirm these before publishing:

- the skill exists locally
- `SKILL.md` is present
- GitHub repo target is known if backup/showcase sync is needed
- ClawHub CLI is installed and logged in if ClawHub publishing is required

Detailed checks are in [references/publish-checklist.md](./references/publish-checklist.md).

## Workflow

### 1. Inspect And Improve The Skill First

Review the skill folder for:

- non-English content that should be internationalized
- private or proprietary references
- user-specific file paths
- tokens, emails, or placeholders that should not be published
- unclear skill structure or stale instructions

Check `SKILL.md`, scripts, references, notebooks, and optional metadata.

If the skill itself needs cleanup, improve it before publishing. For substantial skill revisions, validate the structure first, then publish the revised skill rather than publishing a known rough draft.

### 2. Normalize The Publishable Skill Content

Before publishing:

- convert the skill description and instructions to clear English if the release is meant for a broader audience
- replace proprietary names with generic placeholders when needed
- remove secrets, personal addresses, and private identifiers
- make examples understandable to an outside user
- keep the local publish directory minimal and skill-focused

Keep `SKILL.md` focused on how the AI should use the skill, not on project history.

### 3. Publish To ClawHub First

When the user's priority is the actual skill update, publish the local skill to ClawHub before creating or restoring a GitHub README.

Before publishing:

- verify `clawhub whoami`
- choose the next semantic version
- write a short changelog that reflects the real skill update
- publish from the local skill folder

After publishing:

- confirm the returned version or package identifier
- verify the updated listing if needed

### 4. Add A Temporary GitHub README

If GitHub backup or showcase is desired:

- create a concise `README.md` that explains what the skill does for human readers
- keep `SKILL.md` as the AI-facing file and `README.md` as the GitHub-facing file
- treat the README as temporary in the local publish directory if the user wants a pure local skill folder

### 5. Sync To GitHub

Use SSH or a local credential helper when possible.

Recommended flow:

- clone or update a clean GitHub working copy
- copy in the latest skill files plus the temporary README
- review what will be committed
- commit with a clear message
- push to the intended repository

This keeps the local publish folder and the GitHub sync folder serving different purposes.

### 6. Remove The Local README If The User Wants A Pure Skill Folder

After the GitHub push succeeds:

- delete the local `README.md` from the publish directory if the user's preferred workflow is "clean local skill, richer GitHub repo"
- keep the GitHub version with README intact

### 7. Report What Happened

Summarize clearly:

- what files were cleaned or changed
- whether ClawHub publish succeeded
- whether GitHub push succeeded
- whether the local README was removed afterward
- any follow-up steps still needed from the user

## Decision Rules

- If the skill is still private or contains sensitive material, stop before publishing.
- If the user only wants GitHub backup, skip ClawHub publishing.
- If the user wants the clean-local-folder workflow, publish to ClawHub before adding README.
- If ClawHub CLI is missing, explain the blocker and continue with GitHub prep only if that still helps.
- If the remote repo already contains conflicting starter files, resolve carefully rather than overwriting blindly.
- If renaming the repo, slug, or published skill would break existing links, pause and confirm before changing names.

## Common Failure Modes

Use [references/publish-checklist.md](./references/publish-checklist.md) for:

- pre-publish checklist
- common errors
- safe credential guidance
- suggested commands
- the clean local / GitHub showcase workflow
