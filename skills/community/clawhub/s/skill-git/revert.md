---
name: skill-git:revert
description: Roll back one or more skills to a previous version. Use when the user wants to undo skill changes, discard uncommitted edits, restore an older version, or recover from a bad commit. Triggers on "revert my skill", "roll back skill", "restore skill to v1.0.0", "undo my skill changes", or similar.
---

You are running `/skill-git:revert`. Follow these steps exactly.

## Step 1 — Init Check

Read `~/.skill-git/config.json`.

If the file does not exist, or if it exists but has no `skills` field under the current agent, tell the user:

> skill-git is not initialized. Please run `/skill-git:init` first.

Then stop.

Otherwise, extract the skills registry for the current agent (default: `claude`):
- `global_base` — the agent's base directory
- `skills` — map of skill name → `{ path, version }`

## Step 2 — Select Skill(s)

Parse `$ARGUMENTS` for any skill name(s) or version hints expressed in natural language. Accepted forms:
- No argument → list all registered skills and ask the user which one(s) to revert
- One or more skill names → proceed with those skills
- A version tag (e.g. `v1.0.1`) → use as the target version (resolve skill interactively if ambiguous)

If no skill is specified, list all registered skills and prompt:

```
Registered skills:

  1. <skill-name>    current: <version>
  2. <skill-name>    current: <version>
  ...

Which skill(s) do you want to revert? (enter number(s), name(s), or "all")
```

Wait for the user's response. Resolve to one or more skill names and paths. Validate each name exists in the `skills` map; if not, tell the user and stop.

## Step 3 — Detect Scenario and Determine Target Version

For each selected skill, run:

```bash
git -C <path> status --porcelain
```

Then determine the scenario and target version:

**Scenario A — Dirty working tree (uncommitted changes exist):**
- If the user did NOT specify a version → target = current tag (discard uncommitted changes only, stay at current version)
- If the user specified an older version → target = that version (discard uncommitted changes AND hard-reset to the specified version)

**Scenario B — Clean working tree (no uncommitted changes):**
- If the user did NOT specify a version → target = the tag immediately before the current one (default back one version)
  - Retrieve the previous tag: `git -C <path> tag -l "v*" --sort=-version:refname | sed -n '2p'`
  - If no previous tag exists, tell the user there is no earlier version to revert to, and stop.
  - Display: `[note] No version specified — defaulting to the previous tag <previous-tag>.`
- If the user specified a version → target = that version

For each skill, check that the target tag exists:

```bash
git -C <path> tag -l "<target-tag>"
```

If not found, tell the user the tag does not exist and stop.

## Step 4 — Analyze Changes

For each skill, collect the information needed to describe what will be undone. Do NOT execute any changes yet.

**For Scenario A (discard uncommitted changes only):**

```bash
git -C <path> diff HEAD
git -C <path> status --short
```

**For Scenario A with older version target OR Scenario B:**

```bash
git -C <path> diff <target-tag> HEAD
git -C <path> log --oneline <target-tag>..HEAD
```

Also list all version tags that will be permanently deleted (tags newer than the target):

```bash
git -C <path> tag -l "v*" --sort=version:refname | awk -v target="<target-tag>" 'found {print} $0==target{found=1}'
```

Read each diff and write a **2–3 sentence natural language summary** of what will be undone — describe the rules removed, behaviors restored, or edits discarded. Do not mention git commands or commit hashes.

## Step 5 — Show Confirmation Prompt

Display a confirmation for all selected skills in a single message. Choose the warning level based on the scenario:

---

**Scenario A — Discard uncommitted changes only:**

```
⚠️  The following uncommitted changes will be permanently discarded:

  <skill-name>    staying at <current-version>
  <2-3 sentence description of what will be lost>

This cannot be undone.

Proceed? (y/n)
```

---

**Scenario A with older version target — Discard uncommitted AND hard-reset:**

```
🚨  WARNING: Two destructive operations will be performed on <skill-name>:

  1. All uncommitted changes will be permanently discarded.
  2. The following committed versions will be permanently deleted:
       <version-1>, <version-2>, ...

  Reverting to: <target-version>

  What will be removed:
  <2-3 sentence description of what will be undone>

This cannot be undone. These versions will be gone forever.

Type "yes" to confirm, or "n" to cancel:
```

---

**Scenario B — Single version back (default):**

```
The following changes will be permanently removed from <skill-name>:

  <current-version> → <target-version>
  Deleting tag: <current-version>

  What will be removed:
  <2-3 sentence description of what will be undone>

This cannot be undone.

Proceed? (y/n)
```

---

**Scenario B — Multi-version jump:**

```
🚨  WARNING: Multiple committed versions of <skill-name> will be permanently deleted:

  Reverting: <current-version> → <target-version>
  Versions to be deleted: <v-1>, <v-2>, <v-3>, ...

  What will be removed:
  <2-3 sentence description of what will be undone across all deleted versions>

This cannot be undone. All listed versions will be gone forever.

Type "yes" to confirm, or "n" to cancel:
```

---

Wait for the user's response.
- Single-version / Scenario A (uncommitted only): accept `y` or `n`.
- Multi-version / combined operations: require `yes` (full word) to proceed.

If the user does not confirm, tell them nothing was changed and stop.

## Step 6 — Execute

Process each confirmed skill in order.

### 6a — Backup

Before touching anything, create a timestamped backup:

```bash
cp -r <path> /tmp/skill-git-backup-<skill-name>-$(date +%s)
```

### 6b — Reset

**Scenario A — Discard uncommitted changes only:**

```bash
git -C <path> reset --hard HEAD
```

**All other cases (hard-reset to target tag):**

```bash
git -C <path> reset --hard <target-tag>
```

If the reset command fails, print the error message in plain language (no raw git output), restore from the backup, and stop. Do not proceed to tag deletion.

### 6c — Delete Newer Tags

For every version tag newer than the target (collected in Step 4), delete it:

```bash
git -C <path> tag -d <tag>
```

If any tag deletion fails, note it in the final report but continue with the remaining deletions.

### 6d — Update config.json

Update the version for each successfully reverted skill:

```bash
jq --arg agent "claude" --arg name "<skill_name>" --arg ver "<target-version>" \
  '.agents[$agent].skills[$name].version = $ver' \
  ~/.skill-git/config.json > /tmp/sg-cfg.json \
  && mv /tmp/sg-cfg.json ~/.skill-git/config.json
```

Skip this update if the reset failed for that skill.

## Step 7 — Report

```
✅ <skill-name>    reverted to <target-version>
✅ <skill-name>    reverted to <target-version>
❌ <skill-name>    failed — <plain-language reason>

[skill-git] Done. Run /skill-git:commit to record new changes going forward.
```
