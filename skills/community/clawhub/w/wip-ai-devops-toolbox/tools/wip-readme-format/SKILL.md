---
name: wip-readme-format
description: Reformat any repo's README to follow the WIP Computer standard.
license: MIT
interface: [cli, skill]
metadata:
  display-name: "README Formatter"
  version: "1.0.0"
  homepage: "https://github.com/wipcomputer/wip-ai-devops-toolbox"
  author: "Parker Todd Brooks"
  category: repo-management
  capabilities:
    - readme-generation
    - readme-validation
    - section-staging
  requires:
    bins: [node]
  openclaw:
    requires:
      bins: [node]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-readme-format"
        bins: [wip-readme-format]
        label: "Install via npm"
    emoji: "📝"
compatibility: Requires node. Node.js 18+.
---

# README Formatter

Reformats a repo's README to follow the WIP Computer standard. Agent-first, human-readable.

## Commands

```
wip-readme-format /path/to/repo              # rewrite README.md
wip-readme-format /path/to/repo --dry-run    # preview without writing
wip-readme-format /path/to/repo --check      # validate, exit 0/1
```

## What happens

1. Detects all interfaces (CLI, Module, MCP, OC Plugin, Skill, CC Hook)
2. Reads package.json for name, description, repo URL
3. Reads SKILL.md for features
4. Generates the README following the standard:
   - WIP Computer header + interface badges
   - Title + tagline
   - "Teach Your AI" onboarding block
   - Features list
   - Interface coverage table (toolbox repos only)
   - More Info links
   - License block
5. Moves technical content to TECHNICAL.md (never deleted)

## The standard

```
[badges]
# Tool Name
Tagline.

## Teach Your AI to [verb]
[onboarding prompt block]

## Features
[feature list]

## Interface Coverage (toolbox only)
[auto-generated table]

## More Info
- Technical Documentation ... link
- Universal Interface Spec ... link

## License
[standard block]
```

## Interfaces

CLI, Skill
