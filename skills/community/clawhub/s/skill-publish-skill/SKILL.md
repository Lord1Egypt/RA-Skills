---
name: skill-publish
description: Publish AI agent skills to GitHub and multiple skill registries (skills.sh, clawhub.ai) in one workflow. Use this skill whenever the user wants to publish, upload, or push a skill to GitHub, skills.sh, clawhub.ai, or says things like "publish skill", "推送skill", "发布skill", "上传skill到平台", "publish to marketplace", "多平台发布". Also trigger when the user wants to update an already-published skill across platforms. This skill handles git push, registry publishing, and version management.
---

# Skill Publish

Publish an AI agent skill to GitHub and multiple skill registries in one workflow.

The overall flow is: GitHub first, then skills.sh and clawhub.ai, with skillsmp.com auto-syncing from GitHub. Skill name and description on all platforms come from the SKILL.md frontmatter, keeping everything consistent with the GitHub repo.

## Prerequisites

Before running this skill, check that the required CLI tools are available. If any are missing, guide the user through installation.

1. **git** — required. Check with `git --version`.
2. **gh** (GitHub CLI) — required for skills.sh publishing. Check with `gh --version`.
3. **gh skill publish extension** — required for skills.sh. Check with `gh extension list | grep skill`.
   - Install: `gh extension install skills-sh/skill-publish`
4. **clawhub CLI** — required for clawhub.ai publishing. Check with `which clawhub`.
   - Install: `npm i -g clawhub`
   - Login: `clawhub login` (GitHub OAuth)
   - Verify: `clawhub whoami`

If a tool is missing, ask the user whether to install it or skip that platform.

## Workflow

Follow these steps in order.

### Step 1: Resolve the remote URL

1. Read `references/repo-map.json` (relative to this skill's directory). This file maps local project paths to their GitHub URLs.
2. Compare the current working directory against the keys in the mapping.
3. **If a mapping is found:** Use the stored URL. Tell the user: "Detected repo: <URL>"
4. **If no mapping is found:** Ask the user to provide the GitHub repository URL. Accept formats like:
   - `https://github.com/user/repo.git`
   - `git@github.com:user/repo.git`
   - `https://github.com/user/repo`

### Step 2: Check and initialize Git if needed

Run `git status` to check if the current directory is a Git repository.

**If NOT a Git repository:**
1. Run `git init`
2. Run `git add .` to stage all files
3. Run `git commit -m "Initial commit"`
4. Run `git remote add origin <URL>`
5. Run `git branch -M main`

**If already a Git repository:**
1. Check if remote `origin` exists: `git remote get-url origin`
   - If the URL differs from what was resolved, ask the user whether to update it
   - If no remote `origin` exists, run `git remote add origin <URL>`

### Step 3: Handle uncommitted changes

Check for uncommitted changes with `git status --porcelain`.

**If there are uncommitted changes:**
1. Run `git diff --cached` to see staged changes
2. Run `git diff` to see unstaged changes
3. Stage all changes: `git add .`
4. Analyze the staged changes and generate a commit message:
   - Follow conventional commit format: `type(scope): brief summary`
   - Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `style`, `test`
   - Title no more than 50 characters
   - Body lists the affected files and what changed
5. Run `git commit -m "<generated message>"`

**If no uncommitted changes:** Proceed to push.

### Step 4: Push to GitHub

1. Detect the current branch: `git branch --show-current`
2. Try normal push: `git push -u origin <branch>`
3. **If the push fails with a connection error** (e.g., "Could not connect to server", "Failed to connect", timeout, network unreachable):
   - Run `git remote get-url origin` to inspect the current URL.
   - If the URL starts with `https://`, retry up to **3 times**.
   - If all 3 HTTPS retries fail, **automatically switch to SSH**:
     - Convert: `https://github.com/user/repo.git` → `git@github.com:user/repo.git`
     - Run `git remote set-url origin <ssh-url>`
     - Try pushing again.
   - If the remote is already SSH and fails, retry up to 3 times, then report the error.
4. **If the push fails for other reasons** (e.g., divergent histories):
   - Ask the user: "Push failed. Force push? This may overwrite remote history. (y/n)"
   - If yes: `git push -u origin <branch> --force`
   - If no: stop and report.

### Step 5: Save the GitHub mapping

Update `references/repo-map.json` with the current project path and its GitHub URL so future publishes skip the URL prompt.

### Step 6: Publish to skills.sh

skills.sh is a skill registry that auto-discovers skills from GitHub. The `gh skill publish` extension validates the skill and creates a GitHub release.

1. Check if `gh skill publish` extension is installed.
   - If not, offer to install: `gh extension install skills-sh/skill-publish`
2. Read the SKILL.md frontmatter from the current skill directory to get the skill name and description.
3. Run: `gh skill publish --slug <skill-name>`
   - The `--slug` should match the `name` field in SKILL.md frontmatter.
   - If `gh skill publish` is not available, skip and tell the user: "skills.sh will auto-discover your skill from the GitHub repo. For faster indexing, install the extension with `gh extension install skills-sh/skill-publish`."
4. If publishing succeeds, report: "Published to skills.sh: https://skills.sh/<owner>/<repo>/<skill-name>"

### Step 7: Publish to clawhub.ai

ClawHub is a skill marketplace with CLI-based publishing. It requires authentication via GitHub OAuth.

1. Check if `clawhub` CLI is installed.
   - If not, offer to install: `npm i -g clawhub`
2. Check if the user is logged in: `clawhub whoami`
   - If not logged in, guide the user: `clawhub login`
3. Read the SKILL.md frontmatter to get the skill name and description.
4. Derive the version from `git describe --tags --always` or use "1.0.0" for first publish.
5. Run: `clawhub skill publish . --slug <skill-name> --name "<skill-name>" --version <version> --changelog "<commit-message>"`
   - The `--name` and description come from SKILL.md frontmatter to stay consistent.
6. If publishing succeeds, report: "Published to clawhub.ai: https://clawhub.ai/skills/<skill-name>"

### Step 8: Note about skillsmp.com

skillsmp.com automatically scrapes GitHub for public repos with SKILL.md files. No manual action is needed. Tell the user: "skillsmp.com will auto-sync from the GitHub repo (may take a few hours)."

### Step 9: Confirm success

Report the final status of all platforms:

```
Publish complete!
  GitHub:   <url> (branch: <branch>, commit: <message>)
  skills.sh: Published / auto-discoverable
  clawhub.ai: Published / skipped
  skillsmp.com: Auto-sync from GitHub
```

If any platform failed, clearly state which ones succeeded and which need manual follow-up.

## Update flow

When the user wants to update an already-published skill, the workflow is the same — GitHub push first, then re-publish to each platform:

- **skills.sh**: Re-run `gh skill publish` to create a new release.
- **clawhub.ai**: Run `clawhub skill publish` with an incremented version number. Use `git log --oneline <last-tag>..HEAD` to generate a changelog from recent commits.
- **skillsmp.com**: Auto-syncs, no action needed.

## Self-Evolution Mechanism

After each execution of this Skill:

1. Evaluate whether the output achieved the intended goal: **pass / fail**.
2. If it fails, reflect on the cause of failure and append a "failure case + improvement suggestion" to `diary/YYYY-MM-DD.md`.
3. If a certain improvement suggestion is repeatedly mentioned in the most recent three executions, refine it into a formal rule and submit a PR to modify this `SKILL.md`.

## Reference files

- `references/repo-map.json` — Local path to GitHub URL mappings. Read this first to resolve the remote URL; update it after each successful push.
