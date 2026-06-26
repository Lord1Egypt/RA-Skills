---
name: repo
metadata:
  author: es6kr
  version: "0.1.0"
description: Project initialization toolkit. contributing - auto-generate CONTRIBUTING.md from project structure [contributing.md]. "init", "project init", "initialize project", "contributing guide", "CONTRIBUTING.md", "contributing generate" triggers
---

# Init

Project initialization toolkit — scaffolding, boilerplate generation, and setup automation for new or existing projects.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| contributing | Auto-generate CONTRIBUTING.md from project structure analysis | [contributing.md](./contributing.md) |

## Quick Reference

### Contributing (Auto-generate CONTRIBUTING.md)

```bash
/init contributing    # Analyze project and generate CONTRIBUTING.md
```

Key steps:
1. Detect project type (monorepo, single package, npm workspaces)
2. Analyze config files (package.json, .editorconfig, eslint, husky)
3. Detect directory structure and dependencies
4. Generate CONTRIBUTING.md with detected settings

What gets detected:
- **Requirements**: Node.js version, package manager from `engines` and `packageManager`
- **Code Style**: indent, EOL, charset from `.editorconfig`
- **Lint Config**: ESLint rules, Prettier settings
- **Build Commands**: scripts from `package.json`
- **Commit Convention**: Conventional Commits format with detected scopes
- **Pre-commit Hooks**: husky configuration
- **Monorepo Structure**: package dependency graph and build order

[Detailed guide](./contributing.md)

## Design Philosophy

- **Detection over assumption**: Only include sections for settings that actually exist in the project
- **Language-aware**: Match project language (English for open source, Korean for internal)
- **Non-destructive**: Always confirm before overwriting existing files
