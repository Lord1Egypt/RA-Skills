# Release Notes: wip-ldm-os v0.4.48

Adopt Agent Skills Spec. SKILL.md is now pure instructions (163 lines). Product content moved to references/.

## What changed

- SKILL.md rewritten from 390 lines to 163 lines of pure instructions
- Product pitch, skill descriptions, command tables, interface detection all moved to references/ directory
- references/PRODUCT.md: what LDM OS is, what it installs, what changes
- references/SKILLS-CATALOG.md: included and optional skills with full descriptions
- references/COMMANDS.md: full command reference table
- references/INTERFACES.md: interface detection table
- AIs now load reference files on demand instead of getting everything at once
- Research docs saved: Agent Skills Spec, gstack patterns (Garry Tan), AgentCard analysis

## Why

We shipped v0.4.42-v0.4.47 trying to make the SKILL.md work better. Six releases. AIs still ignored the instructions. Root cause: 16KB of mixed product pitch and instructions. The Agent Skills Spec says < 5000 tokens for SKILL.md body, context goes in reference files. AgentCard and gstack prove this works.

## Issues closed

- Partial #113 (universal installer pattern: SKILL.md + references/ structure established)

## How to verify

```bash
wc -l SKILL.md            # should be ~163 lines
ls references/             # PRODUCT.md, SKILLS-CATALOG.md, COMMANDS.md, INTERFACES.md

# Dogfood in fresh session:
# Read https://wip.computer/install/wip-ldm-os.txt
# AI should follow the steps, not dump the entire file
```
