# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0] - 2026-02-27

### ✨ Added

- SKILL.md reformatted to match `coding-agent` style
- Troubleshooting section with common issues
- Models section documenting available Qwen models
- Authentication section with OAuth and API Key options

### 🔧 Changed

- **SKILL.md**: Complete rewrite in English with coding-agent format
- **README.md**: English-only version (removed Chinese links)
- Simplified documentation structure
- Added `metadata` section to SKILL.md frontmatter

### 📝 Documentation

- All content now English-only for international audience
- Reference format: https://github.com/openclaw/skills/blob/main/skills/steipete/coding-agent/SKILL.md

---

## [1.1.0] - 2026-02-27

### ✨ Added

- Bilingual README documentation (EN / 中文)
- Example code directory (`assets/examples/`)
  - Basic task execution (`basic-task.example.sh`)
  - Code review workflow (`code-review.example.sh`)
  - CI/CD integration (`ci-cd.example.yml`)
  - Headless mode example (`headless-mode.example.js`)
- Complete command reference documentation (`references/qwen-cli-commands.md`)
- Project metadata file (`_meta.json`)

### 🔧 Changed

- **Refactored SKILL.md**: Adopted EvoMap/evolver style
  - 3-sentence overview (What it is / Pain it solves / Use in 30 seconds)
  - For / Not For lists
  - Quick start commands
  - Security boundaries table
- Directory structure: `skill/` → `scripts/`
- Documentation style: concise, technical, code-first

### 📝 Documentation

- Added README.md (English concise version)
- Added README.zh-CN.md (Chinese complete version)
- Added navigation links between language versions
- Added Emoji icons for better readability

### 🏷️ Release

- Tag: `v1.1.0`
- Commit: `HEAD`

---

## [1.0.0] - 2026-02-26

### ✨ Added

- Initial release
- Basic command wrapper (`scripts/qwen-code.js`)
  - `status` - Status check
  - `run` - Task execution
  - `review` - Code review
  - `headless` - Headless mode
  - `help` - Help information
- OpenClaw integration support
- Basic Skill definition file (`SKILL.md`)

### 🔧 Changed

- Project renamed to `qwen-code-skill`

### 📝 Documentation

- Initial README documentation
- Basic usage instructions

### 🏷️ Release

- Tag: `v1.0.0`
- Commit: `6f6fff1`

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.2.0 | 2026-02-27 | ✨ English-only, coding-agent format |
| 1.1.0 | 2026-02-27 | ✨ EvoMap style refactoring, bilingual support |
| 1.0.0 | 2026-02-26 | 🚀 Initial release |

---

## Upcoming

### [Unreleased]

- [ ] Add more example code for common workflows
- [ ] Support MCP server management
- [ ] Support Sub-Agent management
- [ ] Add unit tests for qwen-code.js script

---

## Release Notes

### Version 1.2.0 Highlights

🎯 **Core Improvement**: Reformatted to match OpenClaw's `coding-agent` skill style for consistency.

📚 **Documentation Updates**:
- English-only content for international audience
- SKILL.md follows coding-agent template format
- Added troubleshooting section with common issues
- Documented available Qwen models

🔧 **Structure Optimization**:
- Cleaner frontmatter with metadata
- Better organized sections
- Consistent with OpenClaw skill conventions

### Version 1.1.0 Highlights

✨ **EvoMap Style Refactoring**: Complete documentation overhaul following EvoMap/evolver project style.

📚 **Documentation Upgrade**:
- Bilingual README support (English / Chinese)
- Clear For / Not For boundaries
- Rich example code (Shell / YAML / JavaScript)
- Complete command reference documentation

🔧 **Structure Optimization**:
- Clearer directory structure (scripts/ / references/ / assets/)
- SKILL.md follows skill-creator best practices
- Enhanced metadata (author / version / description)

### Version 1.0.0 Highlights

🚀 **From Zero to One**: Completed basic integration of Qwen Code CLI into OpenClaw.

✅ **Core Features**:
- Status check
- Task execution
- Code review
- Headless automation

🔗 **OpenClaw Integration**: Background execution, process management, model selection.
