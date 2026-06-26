---
name: wip-repos
description: Repo manifest reconciler. Makes repos-manifest.json the single source of truth for repo organization.
license: MIT
interface: [cli, module, mcp]
metadata:
  display-name: "Repo Manifest Reconciler"
  version: "0.1.0"
  homepage: "https://github.com/wipcomputer/wip-ai-devops-toolbox"
  author: "Parker Todd Brooks"
  category: dev-tools
  capabilities:
    - manifest-check
    - filesystem-sync
    - repo-add
    - repo-move
    - tree-generation
  requires:
    bins: [node, git]
  openclaw:
    requires:
      bins: [node, git]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-repos"
        bins: [wip-repos]
        label: "Install via npm"
    emoji: "📂"
compatibility: Requires git, node. Node.js 18+.
---

# wip-repos

Repo manifest reconciler. Like prettier for folder structure. Move folders around all day; on sync, everything snaps back to where the manifest says.

## When to Use This Skill

**Use wip-repos for:**
- Checking if the filesystem matches the manifest (`check`)
- Moving repos to match the manifest (`sync`)
- Adding a new repo to the manifest (`add`)
- Moving a repo in the manifest (`move`)
- Generating a directory tree from the manifest (`tree`)

**Use after:**
- Cloning a new repo
- Moving repos between categories
- Adding new repos to the org

### Do NOT Use For

- Git operations (use git directly)
- Repo creation on GitHub (use gh)

## API Reference

### CLI

```bash
wip-repos check                              # diff filesystem vs manifest
wip-repos sync --dry-run                     # preview moves
wip-repos sync                               # execute moves
wip-repos add ldm-os/utilities/new-tool --remote wipcomputer/new-tool
wip-repos move ldm-os/utilities/tool --to ldm-os/devops/tool
wip-repos tree                               # generate directory tree
```

### Module

```javascript
import { check, planSync, addRepo, moveRepo, generateReadmeTree } from '@wipcomputer/wip-repos';

const result = check('/path/to/manifest.json', '/path/to/repos/');
const moves = planSync('/path/to/manifest.json', '/path/to/repos/');
```

### MCP

Tools: `repos_check`, `repos_sync_plan`, `repos_add`, `repos_move`, `repos_tree`
