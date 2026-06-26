# Skill Template

## Frontmatter

```yaml
---
name: skill-name
description: "Brief description of what the skill does and when to use it"
version: 1.0.0
author: "Your Name"
metadata: {"clawdbot":{"emoji":"🔧"}}
allowed-tools: Bash(skill-name:*)
---
```

## Content Sections

1. **Overview** - Brief introduction and purpose
2. **Quick Start** - Basic usage examples
3. **Installation** - Setup instructions
4. **Usage** - Detailed usage guide
5. **Examples** - Practical use cases
6. **Best Practices** - Recommended approaches
7. **Troubleshooting** - Common issues and solutions
8. **License** - Licensing information

## Example Structure

```
skill-name/
├── SKILL.md             # Main documentation
├── _meta.json           # Skill metadata
├── references/          # Additional documentation
│   └── examples.md      # Usage examples
├── assets/              # Static assets
├── scripts/             # Helper scripts
└── hooks/               # Integration hooks
```