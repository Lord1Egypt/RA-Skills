---
name: repo-setup
description: "Fork, clone, and set up a GitHub repository for development or contribution. Handles fork creation, clone with authentication, upstream remote configuration, branch creation from upstream, and dependency installation. Use when starting work on a new open-source project, setting up a multi-repo development environment, or onboarding to a new codebase."
---

# Repo Setup — Fork, Clone & Branch Setup

## Overview

Automate the setup of a local development environment for contributing to or working on GitHub repositories. Handles the full fork → clone → branch → dependencies pipeline.

**Use cases**: Open-source contribution, multi-repo development, new project onboarding, codebase exploration.

## Prerequisites

```bash
gh auth status   # Must show "Logged in"
git --version    # Git installed
```

If not configured, ask the user to provide:
1. **GitHub username** — used for fork URLs and clone paths
2. **GitHub token** — run `gh auth login` or set `export GH_TOKEN=<token>`

Token is required for: forking repos, cloning private forks, pushing code. Without it, `git push` and `gh repo fork` will fail.

## Workflow

### Step 1: Get Parameters

| Parameter | Required | Default | Example |
|-----------|----------|---------|---------|
| Repository | ✅ | — | `owner/repo` |
| GitHub username | ✅ | — | `myusername` |
| Branch name | ❌ | *(stay on default)* | `fix/bug-description` |
| Working directory | ❌ | `~/prs/{repo}` | `~/dev/{repo}` |
| Auth method | ❌ | `GH_TOKEN` env var | Token in URL, SSH |

### Step 2: Fork

```bash
gh repo fork {owner}/{repo} --clone=false
```

If fork already exists, this is a no-op. If the user already owns the repo, skip forking.

### Step 3: Clone

```bash
WORKDIR="${WORK_BASE:-$HOME/prs}/{repo_name}"

if [ -d "$WORKDIR" ]; then
    cd "$WORKDIR"
    git fetch --all
else
    mkdir -p "$(dirname "$WORKDIR")"

    # With token auth
    git clone "https://${GH_TOKEN}@github.com/${username}/${repo_name}.git" "$WORKDIR"

    # Or with SSH
    # git clone "git@github.com:${username}/${repo_name}.git" "$WORKDIR"

    cd "$WORKDIR"
fi
```

### Step 4: Configure Upstream Remote

```bash
if ! git remote get-url upstream &>/dev/null; then
    git remote add upstream "https://github.com/${owner}/${repo_name}.git"
fi
git fetch upstream
```

### Step 5: Create Feature Branch

```bash
# Detect default branch
DEFAULT_BRANCH=$(git remote show upstream 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}')
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"

# Create branch from latest upstream
git checkout -b {branch_name} upstream/$DEFAULT_BRANCH
```

### Branch Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Bug fix | `fix/{short-description}` | `fix/null-pointer-on-empty-list` |
| Feature | `feat/{short-description}` | `feat/add-retry-logic` |
| Refactor | `refactor/{short-description}` | `refactor/extract-auth-module` |
| Review iteration | `fix/{description}-v2` | `fix/tool-guards-v2` |

### Step 6: Install Dependencies

Detect the project type and install accordingly:

| Indicator | Language | Install Command |
|-----------|----------|----------------|
| `pyproject.toml` / `setup.py` | Python | `pip install -e ".[dev]"` or `pip install -e .` |
| `requirements.txt` | Python | `pip install -r requirements.txt` |
| `package.json` | Node.js | `npm install` |
| `go.mod` | Go | `go mod download` |
| `Cargo.toml` | Rust | `cargo build` |
| `pom.xml` | Java | `mvn install -DskipTests` |
| `build.gradle` | Java/Kotlin | `./gradlew build -x test` |

**If full dev install fails** (common with native dependencies):
1. Install core deps individually
2. Skip optional native/GPU deps
3. Ensure test framework is installed at minimum

### Step 7: Verify

```bash
# Check setup
echo "Directory: $(pwd)"
echo "Branch: $(git branch --show-current)"
echo "Upstream: $(git remote get-url upstream)"
echo "Fork: $(git remote get-url origin)"

# Quick build/import test
# Python: python -c "import {package}"
# Node: npm run build (if applicable)
# Go: go build ./...
```

## Automation Script

A helper script is available if this Skill is installed alongside **oss-pr-campaign**:

```bash
# One-liner setup
scripts/setup_repo.sh owner/repo username fix/branch-name
```

Or implement the same logic step-by-step using the SOP above.

## Output

- Local repo at `~/prs/{repo}/` (or custom directory) on feature branch
- Upstream remote configured
- Dependencies installed
- Ready for development

## Tips

- When used as part of a development pipeline, this follows **issue-hunter** and feeds into **dev-test**.
- For exploring a codebase without contributing, skip the fork step and clone the original directly.
- Store GH_TOKEN in your shell profile for persistent auth across sessions.
- If working on multiple repos, keep them all under `~/prs/` for easy navigation.
