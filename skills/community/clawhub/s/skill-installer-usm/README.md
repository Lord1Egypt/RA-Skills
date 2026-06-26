# Skill Installer

The acquisition engine for the **Universal Skill Management (USM)** architecture. It facilitates the search, installation, and updating of skills from centralized registries.

## 🌟 Overview

`skill-installer` is the bridge between external skill ecosystems (like [ClawHub](https://clawhub.ai)) and your local USM Hub (`~/.skills/`). It ensures that skills are downloaded to the correct global location before they are distributed to specific agent platforms.

## 🛠 Features

- **Multi-Registry Support**: Native integration with `clawhub` and `skillhub`.
- **Global Hub Deployment**: Automatically installs skills into `~/.skills/` for universal access.
- **Dependency Management**: Checks for required CLI tools (like `clawhub` NPM package) before execution.

## 🔄 The Lifecycle Workflow

1. **Discovery**: Search for skills using `clawhub search <query>`.
2. **Installation**: Download the skill artifacts using `clawhub install <slug>`.
3. **Provisioning**: (Handled by `skill-manager`)
   - Configure `meta.yaml` scope.
   - Synchronize symbolic links to agent directories using `sync_skills.sh`.

## 🏗 Ecosystem Integration

After installing a skill with `skill-installer`, you should always consult **[skill-manager](https://github.com/ZiweiAxis/skill-manager)** to:
- Finalize the skill's distribution scope.
- Update the active symlinks for your agent platforms (Cursor, Claude Code, etc.).

---

## 🏗 Directory Structure
- `SKILL.md`: The primary instruction set for the installer.
- `meta.yaml`: USM metadata for the installer itself.
- `LICENSE.txt`: Apache License 2.0.

## 🤝 Credits
This tool is based on the **`skill-install`** implementation from **OpenClaw**.
