---
name: core-workflow
description: The standard GitHub workflow from task to PR.
---

# Core Workflow

Standard flow from "task link" to "create PR" (no merge).

## Prerequisites
- **GitHub Skill** or **`gh` CLI** installed and authenticated (`gh auth login`).
- **Security**: Only use trusted skills and tools. For `gh` extensions or related skills, verify the provider and repository integrity.
- Check at workflow start; prompt if missing.

## Workflow Steps

### Step 1: Get Task
Use [Task Retrieval](feature-task-retrieval.md) to fetch details.

### Step 2: Prepare Environment
1. **Base Branch**: Use `dev` if exists (local/origin), else `main` (or repo default).
2. **Create Branch**:
   - Update base: `git checkout <base> && git pull origin <base>`
   - Create new: `git checkout -b fix/<kebab-case-desc>` (or `feature/...`).
3. **Create Spec**: Write `TODO.md` (see [TODO Spec](feature-todo-spec.md)).

### Step 3: Implement & Verify
Delegate to SubAgent using `TODO.md` (see [TODO Spec](feature-todo-spec.md)).
- Wait for completion/confirmation.
- Get user confirmation.
- Delete `TODO.md`.
- Create Commit.

### Step 4: Create PR
**Target**: `origin` only.
1. **Push**: `git push -u origin <branch>`
2. **Create**:
   ```bash
   gh pr create --base <base-branch> --head <branch> --title "<title>" --body "<body_with_link>"
   ```
   - Do NOT use `--repo`.

## Edge Cases

| Case | Handling |
|------|----------|
| `git pull` fails | Suggest checking network/origin; or branch from local and note "latest not pulled". |
| Branch exists | Ask to use existing or new name (e.g. `-v2`). |
| Origin Read-only | Report error; suggest UI creation. |
| User asks for PR early | If commits exist and user insists, proceed to Step 4. |

## Key Points
- **Origin Only**: Do not interact with other remotes.
- **No Merge**: The workflow ends at PR creation.
- **Safety**: Verify env/auth before starting dependent steps.
