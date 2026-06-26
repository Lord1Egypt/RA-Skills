---
name: readme-generator
description: "Auto-generate comprehensive, well-structured README.md files by analyzing your project's codebase, dependencies, configuration, and structure. Scans package.json, pyproject.toml, Cargo.toml, Dockerfile, CI configs, and source code to produce professional documentation. Use when the user wants to: (1) Create a README for a new project, (2) Regenerate an outdated README, (3) Document an open-source project for publishing, (4) Create project documentation from scratch, (5) Standardize README format across repos. Best for open-source maintainers, indie developers, teams standardizing documentation, and anyone who dreads writing README files."
version: 1.0.0
homepage: https://clawhub.ai
metadata:
  openclaw:
    emoji: "📖"
    requires:
      bins:
        - git
---

# README Generator

Turn your project into a **professional, well-documented README.md** — no manual writing required.

## When to Use

✅ **USE this skill when:**

- "Generate a README for my project"
- "My README is outdated, rewrite it"
- "Create docs for my open-source library"
- "I have a new repo with no documentation"
- "Standardize all READMEs in my org"
- "Add installation and usage sections to my README"
- "Generate API docs for my CLI tool"

❌ **DON'T use this skill when:**

- Need full API reference docs → use an API doc generator
- Need multi-page documentation site → use a docs site generator (Docusaurus, MkDocs)
- Need architecture decision records (ADRs) → use a decisions skill

## How It Works

1. **Scans project structure** — reads directory tree, identifies project type
2. **Reads key config files** — detects language, framework, package manager, test runner, CI/CD
3. **Analyzes source code** — identifies entry points, CLI commands, exported APIs, environment variables
4. **Checks existing docs** — reads existing README, CONTRIBUTING, CHANGELOG, LICENSE
5. **Generates** a comprehensive markdown document

## Generated Sections

The README automatically includes the sections that are relevant to your project:

### Always Included
- **Title & Badges** — Project name, description, license, CI status, version
- **Description** — What the project does and why it exists
- **Table of Contents** — For longer READMEs
- **Installation** — Language-appropriate install instructions

### Conditional (auto-detected)
- **Prerequisites** — Runtime requirements (Node, Python, Java, etc.)
- **Quick Start** — Minimal steps to get running
- **Usage / CLI** — Commands, flags, examples (detected from CLI tools)
- **API** — If a library/module is detected
- **Configuration** — Env vars, config files, dotenv support
- **Scripts** — npm scripts, Makefile targets, Justfile recipes
- **Docker** — If Dockerfile or compose files exist
- **Testing** — How to run tests
- **Project Structure** — If the layout is non-trivial
- **Contributing** — If CONTRIBUTING.md or contribution patterns exist
- **License** — If a license file is detected
- **Changelog** — Links to CHANGELOG.md or git tags

## Examples

### Generate from scratch

> "Generate a README for the current project"

→ Scans the entire project, produces a complete README.md.

### Regenerate existing

> "Regenerate the README but keep the custom sections"

→ Merges generated content with preserved custom content from the existing README.

### Focus on specific aspects

> "Generate a README focusing on the API section — I have a Python library"

→ Deep-dives into module exports, class signatures, and function parameters.

## Language/Framework Detection

The skill recognizes and tailors output for:

| Type        | Detected From                          |
|-------------|----------------------------------------|
| Node.js     | package.json, tsconfig.json, npm/yarn  |
| Python      | pyproject.toml, setup.py, requirements  |
| Rust        | Cargo.toml                             |
| Go          | go.mod, go.sum                         |
| Java/Kotlin | pom.xml, build.gradle                  |
| .NET/C#     | *.csproj, *.sln, NuGet.config          |
| Docker      | Dockerfile, compose.yaml               |
| Generic     | Makefile, shell scripts, any project   |

## Badge Support

Auto-includes badges for:
- **License** (from LICENSE file)
- **Language version** (from SDK/config files)
- **CI status** (detects GitHub Actions, GitLab CI, CircleCI)
- **Package version** (from registry files if publishable)

## Notes

- **Preserves custom content** — when updating an existing README, content outside generated sections is kept intact
- **Follows best practices** — output adheres to the [Standard README](https://github.com/RichardLitt/standard-readme) specification
- **Project-specific** — adapts to CLI tools, libraries, web apps, and monorepos differently
- **Open-source ready** — output is formatted for publishing to GitHub/GitLab immediately
