---
name: deploy-public
version: 1.3.0
description: Private-to-public repo sync. Copies everything except ai/ to the public mirror. Creates PR, merges, syncs releases.
author: Parker Todd Brooks
interface: [cli]
metadata:
  category: dev-tools
  capabilities:
    - repo-sync
    - release-sync
---

# deploy-public

Private-to-public repo sync. One script for all repos. Copies code, creates a PR on the public repo, merges it, and syncs GitHub releases.

## When to Use This Skill

**Use deploy-public for:**
- Publishing a private repo's code to its public counterpart
- After running `wip-release` on the private repo (release must exist first)
- Syncing release notes from private to public

**CRITICAL: Release order matters.**
1. Merge PR to private repo's main
2. Run `wip-release` (creates GitHub release with notes on private repo)
3. THEN run `deploy-public.sh` (pulls notes from private release)

If you skip step 2, the public release gets empty notes.

### Do NOT Use For

- Repos without a `-private` counterpart
- First-time repo setup (create the public repo on GitHub first)

## API Reference

### CLI

```bash
bash scripts/deploy-public.sh /path/to/private-repo org/public-repo
```

### Examples

```bash
# Deploy memory-crystal
bash scripts/deploy-public.sh /path/to/memory-crystal-private wipcomputer/memory-crystal

# Deploy wip-dev-tools
bash scripts/deploy-public.sh /path/to/wip-ai-devops-toolbox-private wipcomputer/wip-ai-devops-toolbox
```

## What It Does

1. Clones the public repo to a temp directory
2. Copies all files from private repo (excluding `ai/`, `.git/`)
3. Creates a branch, commits, pushes, creates PR
4. Merges the PR (regular merge, never squash)
5. Syncs GitHub releases (pulls notes from private repo's releases)
