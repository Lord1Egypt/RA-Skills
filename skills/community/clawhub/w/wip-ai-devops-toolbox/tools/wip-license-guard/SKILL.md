---
name: wip-license-guard
description: License compliance for your own repos. Ensures correct copyright headers, dual-license blocks, and LICENSE files across all source files.
license: MIT
interface: [cli, skill]
metadata:
  display-name: "License Guard"
  version: "1.0.0"
  homepage: "https://github.com/wipcomputer/wip-ai-devops-toolbox"
  author: "Parker Todd Brooks"
  category: dev-tools
  capabilities:
    - copyright-enforcement
    - license-compliance
    - license-file-check
  requires:
    bins: [node, git]
  openclaw:
    requires:
      bins: [node, git]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-license-guard"
        bins: [wip-license-guard]
        label: "Install via npm"
    emoji: "📜"
---

# wip-license-guard

License compliance for your own repos. Ensures correct copyright, dual-license blocks, LICENSE files, and README license sections.

## When to Use This Skill

- Before a release, to verify all files have correct license headers
- After adding new source files to a repo
- To enforce the MIT/AGPL dual-license pattern
- To standardize README license sections across all your repos

## CLI

```bash
wip-license-guard check [path]                  # audit repo against config
wip-license-guard check --fix [path]             # auto-fix LICENSE, CLA, copyright issues
wip-license-guard init [path]                    # interactive setup
wip-license-guard init --from-standard           # apply WIP Computer defaults (no prompts)
wip-license-guard readme-license [path]          # audit README license sections
wip-license-guard readme-license --dry-run       # preview what would change
wip-license-guard readme-license --fix           # apply standard block to all READMEs
```

### readme-license

Scans all repos for README license sections. Three modes:

- **No flags**: audit only. Reports non-standard, missing, and sub-tool READMEs that shouldn't have license sections.
- **--dry-run**: preview. Shows what each README has now and what would change. No files touched.
- **--fix**: apply. Replaces non-standard sections with the standard dual MIT/AGPLv3 block. Removes license sections from sub-tool READMEs.

Works on a single repo or a directory of repos:
```bash
wip-license-guard readme-license /path/to/one-repo
wip-license-guard readme-license /path/to/directory-of-repos
```
