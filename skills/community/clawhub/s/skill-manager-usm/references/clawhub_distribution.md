# Analysis: Distributing USM Skills via ClawHub

This document outlines how to publish and synchronize skills developed within the Universal Skill Management (USM) ecosystem to the **ClawHub** public registry.

## 📦 Publishing Workflow

### 1. Unified Structure (Prerequisite)
ClawHub expects a folder containing at least a `SKILL.md` file with valid frontmatter.
- **Path**: `~/.skills/<slug>/`
- **Required Metadata**:
  - `name`: Human-readable name.
  - `description`: [USM] tagged description for better menu identification.

### 2. Authentication
Before publishing, you must authenticate the CLI:
```bash
clawhub login
```
*Note: This usually opens a browser to authorize your GitHub/ClawHub account.*

### 3. Manual Publication
To publish a specific skill for the first time or as a major update:
```bash
clawhub publish ~/.skills/<slug> --version <semver> --changelog "Added USM support"
```

### 4. Automated Synchronization (`skill-manager` Integration)
The `clawhub sync` command is ideal for maintaining the USM Global Hub:
```bash
# Scan local skills and publish updates
clawhub sync --root ~/.skills/ --bump patch --all
```

### 5. Naming Conflict Resolution (Slug Logic)
ClawHub requires **globally unique slugs**.
- **Slug Ownership**: If the slug `skill-creator` is already taken, a `publish` command will fail unless you are the owner.
- **Display Name vs. Slug**: You can have a common display name (e.g., "Docker Manager") but the slug MUST be distinct.

**Recommended Resolution Strategies:**
1. **Namespace Prefixing**: Use a personal or organization prefix (e.g., `ziwei-docker` or `usm-installer`).
2. **Local Overwrite Protection**: `skill-installer` will check for existing directories in `~/.skills/` before installing. If a local skill has the same name as a registry slug, it will prompt for a rename.

## 🛠 Integration into USM Ecosystem

### `skill-creator` (The Builder)
- Add a final step in the development loop: **"Launch to Registry"**.
- AI can prompt: "Your skill has passed all evals. Would you like to publish it to ClawHub now?"

### `skill-manager` (The Orchestrator)
- **Registry Inventory**: `skill-manager` can track which local skills are also available on the registry.
- **Sync Engine**: Integrate `clawhub sync` into the sync workflow to ensure that updates made locally are automatically pushed to the registry (for owners).

### `skill-installer` (The Acquisition)
- Continues to serve as the `install` and `update` client for users consuming these skills.

## 📑 Next Steps
1.  **Draft `agents/registry_agent.md`** for `skill-manager` to handle these commands.
2.  **Add `registry_preferences`** to `meta.yaml` to track registry slugs and versions.
