###### WIP Computer

# README Formatter

Generate or validate READMEs that follow the WIP Computer standard. Badges, title, tagline, "Teach Your AI" block, features, interface coverage table, license.

## What it does

- Generates separate section files (README-init-badges.md, README-init-features.md, etc.) so you can edit any section independently
- Deploy assembles them into the final README
- Same pattern as release notes: staging, review, deploy
- Validates existing READMEs against the standard

## Templates

All standard content lives in `ai/wip-templates/readme/`. Edit the templates, every tool picks up the changes. No code changes needed.

| Template | What it is |
|----------|-----------|
| `wip-lic-footer.md` | License section (plain text + markdown formats) |
| `cla.md` | Contributor License Agreement |
| `LICENSE.md` | Full dual MIT+AGPLv3 LICENSE file |
| `prompt.md` | Standard "Teach your AI" install prompt template |

Both `wip-readme-format` and `wip-license-guard` read from these templates at runtime.

## Usage

```bash
# Generate section files for review
node tools/wip-readme-format/format.mjs /path/to/repo

# Assemble sections into final README
node tools/wip-readme-format/format.mjs /path/to/repo --deploy

# Preview without writing
node tools/wip-readme-format/format.mjs /path/to/repo --dry-run
```

## Requirements

- node (18+)

## Interfaces

- **CLI**: Command-line tool
- **Skill**: SKILL.md for agent instructions

## Part of [AI DevOps Toolbox](https://github.com/wipcomputer/wip-ai-devops-toolbox)
