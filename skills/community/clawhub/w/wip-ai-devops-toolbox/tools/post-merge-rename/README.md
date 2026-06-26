###### WIP Computer

# Post-Merge Branch Naming

Cleans up after itself. Merged branches get renamed with dates automatically.

## What it does

- Scans for merged branches that haven't been renamed
- Appends `--merged-YYYY-MM-DD` to preserve history
- We never delete branches. We rename them.

## Usage

```bash
bash post-merge-rename.sh
```

## Requirements

- git
- bash

## Interfaces

- **CLI**: Shell script
- **Skill**: SKILL.md for agent instructions

## Part of [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox)
