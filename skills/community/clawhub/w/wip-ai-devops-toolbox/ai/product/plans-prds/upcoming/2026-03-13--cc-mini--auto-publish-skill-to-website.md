# Plan: Auto-Publish SKILL.md to Website on Deploy

**Date:** 2026-03-13
**Author:** CC-Mini + Parker
**Priority:** High (blocks agent.txt rollout)
**Related:** Universal Installer, deploy-public.sh, wip-release

---

## The Problem

SKILL.md files live in GitHub repos. When you paste a GitHub URL into Claude or another AI, it often has trouble parsing the page (GitHub wraps everything in HTML). The SKILL.md should also be served as clean plain text from your own website so any AI can read it instantly.

Right now this is manual. After every release, someone would have to copy the SKILL.md and deploy it. Nobody does that.

## What This Does

After `wip-release` publishes a new version, automatically:
1. Copy the SKILL.md from the repo to the website as a `.txt` file
2. Deploy to the website

The result: `yoursite.com/install/your-tool.txt` always matches the latest released SKILL.md.

## How It Works (For Us)

```
wip-release patch --notes="whatever"
  -> version bump, npm publish, GitHub release (existing)
  -> deploy-public.sh (existing)
  -> NEW: publish-skill.sh
     -> copies skills/*/SKILL.md to wip-websites-private/wip.computer/install/{name}.txt
     -> runs deploy.sh to rsync to VPS
```

After release, `wip.computer/install/memory-crystal.txt` is the latest SKILL.md. The install prompt points here instead of GitHub.

## How It Works (For Anyone)

A developer using the DevOps Toolbox configures a `publish.json` (or section in their repo config):

```json
{
  "skill_publish": {
    "source": "skills/memory/SKILL.md",
    "target_name": "memory-crystal",
    "website_repo": "/path/to/my-website-repo",
    "website_dir": "install",
    "deploy_command": "bash deploy.sh"
  }
}
```

Or simpler, in the SKILL.md frontmatter:

```yaml
publish:
  url: wip.computer/install/memory-crystal.txt
```

The tool reads the config, copies the file, runs the deploy command. Same pattern for any website, any hosting, any deploy method.

## The Convention

```
yoursite.com/install/{tool-name}.txt
```

Plain text. No HTML. No rendering. Just the SKILL.md content served as `text/plain`. Any AI can `fetch()` this URL and get clean, parseable content.

This is like `robots.txt` (tells crawlers what to do) and `agent.txt` (tells agents what's available). `/install/*.txt` tells agents how to install things.

## Setup Flow

When a developer first configures this:

```bash
wip-release setup-publish
```

Asks:
1. Where is your website repo? (path)
2. What directory should install files go in? (default: `install/`)
3. What's your deploy command? (e.g., `bash deploy.sh`, `rsync ...`, `vercel deploy`)
4. Where are your SKILL.md files? (auto-detected from `skills/*/SKILL.md`)

Saves config to `.wip-release.json` or similar. From then on, every `wip-release` includes the publish step.

## Implementation

### New script: `scripts/publish-skill.sh`

```bash
#!/bin/bash
# Publish SKILL.md to website as plain text
# Usage: publish-skill.sh <repo-path> <website-path> <install-dir> <name>

REPO="$1"
WEBSITE="$2"
INSTALL_DIR="${3:-install}"
NAME="$4"

# Find SKILL.md
SKILL=$(find "$REPO/skills" -name "SKILL.md" -maxdepth 2 | head -1)
if [ -z "$SKILL" ]; then
  echo "No SKILL.md found in $REPO/skills/"
  exit 1
fi

# Copy as .txt
mkdir -p "$WEBSITE/$INSTALL_DIR"
cp "$SKILL" "$WEBSITE/$INSTALL_DIR/$NAME.txt"
echo "Published: $INSTALL_DIR/$NAME.txt"
```

### Integration into wip-release

After `deploy-public.sh` succeeds, check if `skill_publish` config exists. If so, run `publish-skill.sh`.

### For our repos

| Repo | SKILL.md | Published to |
|------|----------|-------------|
| memory-crystal | `skills/memory/SKILL.md` | `wip.computer/install/memory-crystal.txt` |
| wip-agent-pay | `skills/agent-pay/SKILL.md` | `wip.computer/install/agent-pay.txt` |
| wip-ldm-os | `SKILL.md` | `wip.computer/install/ldm-os.txt` |
| wip-ai-devops-toolbox | `SKILL.md` | `wip.computer/install/devops-toolbox.txt` |

## Files to Create/Modify

| File | Change |
|------|--------|
| `scripts/publish-skill.sh` (NEW) | Copy SKILL.md to website as .txt |
| `tools/wip-release/core.mjs` | Add publish-skill step after deploy-public |
| `tools/wip-release/cli.js` | Add `setup-publish` command |
| `tools/wip-release/SKILL.md` | Document the new feature |

## Verification

1. `wip-release patch --dry-run` shows the publish step
2. After release, `curl wip.computer/install/memory-crystal.txt` returns the SKILL.md content
3. An AI can `Read wip.computer/install/memory-crystal.txt` and get clean text
