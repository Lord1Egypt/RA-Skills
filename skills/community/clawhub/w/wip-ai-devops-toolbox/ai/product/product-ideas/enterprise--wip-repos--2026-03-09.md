# wip-repos: Enterprise Repo Manifest

**Date:** 2026-03-09
**Status:** Product idea
**Category:** Enterprise feature for wip-dev-tools

## The Problem

Development teams have dozens or hundreds of repos. Nobody agrees where things go. Folder structures drift. READMEs go stale. New people can't find anything. AI agents reference paths that moved three weeks ago.

Every team has a folder structure. Nobody has a source of truth for it.

## The Product

`wip-repos` ... a CLI tool that makes `repos-manifest.json` the single source of truth for your entire repo organization. The manifest defines where every repo lives, what category it belongs to, and what its remote is. Everything else derives from it.

### How It Works

The manifest is a JSON file checked into a shared repo (or a dedicated config repo). It maps local paths to remotes with metadata:

```json
{
  "ldm-os/devops/wip-dev-tools-private": {
    "remote": "wipcomputer/wip-dev-tools-private",
    "public": "wipcomputer/wip-dev-tools",
    "privatized": true,
    "category": "devops",
    "description": "Dev toolkit for AI-assisted development"
  }
}
```

### Commands

- `wip-repos add my-thing --category utilities` ... add a new repo to the manifest
- `wip-repos move my-thing --from utilities --to identity` ... propose moving a repo
- `wip-repos check` ... diff the filesystem against the manifest, flag drift
- `wip-repos sync` ... rearrange local folders to match the manifest
- `wip-repos readme` ... regenerate the README directory tree from the manifest

### The Enterprise Flow

1. **Someone makes a new repo.** They run `wip-repos add my-thing --category utilities`. This creates a PR to the manifest.

2. **The org owner reviews.** They see the PR. Maybe they agree it's utilities. Maybe they think it belongs in identity. They change it in the PR and merge.

3. **Everyone syncs.** `git pull && wip-repos sync`. Folders move on every machine to match the merged manifest.

4. **Someone moves a folder locally.** That's fine. Their machine, their problem. But they can't push that change without a PR to the manifest. If they don't PR it, next `wip-repos sync` snaps everything back.

5. **CI enforces it.** `wip-repos check` runs on every PR. If the manifest drifted from the filesystem (or vice versa), the PR is blocked until someone reconciles.

### The Key Insight

**Your local folder structure is temporary. The manifest is permanent.**

Like a code formatter. You can write code however you want. But on save, prettier puts it back. Stop fighting it.

People can rearrange their folders all day. Open a PR to the manifest if you think it should change. If the org owner rejects it, your folders snap back on next sync. If they accept it, everyone's folders move.

The tool doesn't give anyone permission to reorganize. It gives them permission to propose. The merge authority decides.

### Integration Points

- **deploy-public** and **wip-release** call `wip-repos check` before running. Stale manifest blocks deploys.
- **README generation.** `wip-repos readme` regenerates the directory tree, repo tables, and summary counts. No more manual README updates.
- **CLAUDE.md generation.** `wip-repos claude` regenerates the repo references in agent instruction files. AI agents always have correct paths.
- **CI/CD.** `wip-repos check` as a PR check. Drift = blocked merge.

### What This Replaces

- Manually updating README.md when repos move
- Manually updating repos-manifest.json
- Manually updating CLAUDE.md references
- Manually updating memory files with repo paths
- Hoping everyone's local folder structure matches
- Onboarding docs that go stale ("the repo is at..." no it isn't)

## Why This Matters for Enterprise

Teams with 10+ repos already lose track. Teams with 100+ repos are drowning. AI-assisted teams are worse because the agents reference paths constantly and break when things move.

This is the missing piece between "we have a folder structure" and "our folder structure is enforced, documented, and self-healing."

## Origin

Built from the WIP.computer workflow managing 50+ repos across two AI agents and one human. The problem was real: repos moved, READMEs drifted, agents broke, Parker had to fix paths by hand. The manifest was the answer. The tool is the enforcement.
