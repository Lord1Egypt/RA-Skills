---
name: wip-repo-init
description: Scaffold the standard ai/ directory structure in any repo.
license: MIT
interface: [cli, skill]
metadata:
  display-name: "Repo Init"
  version: "1.0.0"
  homepage: "https://github.com/wipcomputer/wip-ai-devops-toolbox"
  author: "Parker Todd Brooks"
  category: repo-management
  capabilities:
    - scaffold-ai-dir
    - template-copy
  requires:
    bins: [node]
  openclaw:
    requires:
      bins: [node]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-repo-init"
        bins: [wip-repo-init]
        label: "Install via npm"
    emoji: "📁"
compatibility: Requires node. Node.js 18+.
---

# Repo Init

Scaffolds the standard `ai/` directory structure in any repo.

## Commands

```
wip-repo-init /path/to/repo              # scaffold ai/ in a repo
wip-repo-init /path/to/repo --dry-run    # preview without changes
wip-repo-init /path/to/repo --yes        # skip confirmation prompt
```

## What happens

**New repo (no ai/ folder):** Creates the full standard structure with all READMEs explaining what goes where.

**Existing repo (ai/ folder exists):** Shows you what will happen and asks for confirmation. If you say yes:
1. Moves your current `ai/` contents to `ai/_sort/ai_old/`
2. Scaffolds the new standard structure
3. You sort files from `ai_old/` into the new structure at your own pace

Nothing is deleted. Your old files are all in `ai/_sort/ai_old/`.

## The standard ai/ structure

```
ai/
  read-me-first.md          <- explains everything, links to all sections
  _sort/                    <- holding pen for files that need sorting
  _trash/                   <- archive (never delete, move here)
  dev-updates/              <- engineering changelog, auto-detected by wip-release
  product/
    readme-first-product.md <- the product bible
    notes/                  <- freeform notes, research
    plans-prds/             <- plans with lifecycle stages
      roadmap.md            <- prioritized roadmap
      current/              <- plans being built now
      upcoming/             <- plans that are next
      archive-complete/     <- plans that shipped
      todos/                <- per-agent todo files
    product-ideas/          <- ideas that aren't plans yet
```

Every folder has a `_trash/` subfolder. Every section has a README explaining what it is, what goes in it, and how to maintain it.

## Interfaces

CLI, Skill
