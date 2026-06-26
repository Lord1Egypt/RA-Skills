# Skill Manager

The central orchestrator for the **Universal Skill Management (USM)** architecture. It manages the distribution, synchronization, and scope of AI skills across multiple agent platforms (Claude, Cursor, Codex, Gemini, etc.).

## ❓ Why Skill Manager?

As you build or install more AI skills, you'll encounter several **pain points**:
- **Fragmentation**: Skills are scattered across hidden directories (`~/.cursor/rules`, `~/.claude/skills`, etc.), making them hard to find and manage.
- **Redundancy & Inconsistency**: Manually copying a skill to multiple agent folders leads to version drift. You update it for Cursor, but the Claude version remains stale.
- **Manual Overhead**: Setting up a new agent or project from scratch requires manually linking or copying dozens of skills.

**Skill Manager solves this by providing:**
1. **Single Source of Truth**: All physical files live in one place (`~/.skills/`).
2. **Automated Distribution**: One command (`sync_skills.sh`) broadcasts updates to all your tools via symbolic links.
3. **Granular Control**: Use `meta.yaml` to define which agent gets which skill (Universal vs. Specific).

## 🚀 The 2-Layer 2-Dimension Architecture

This project implements a robust "Source of Truth" pattern:
- **Global Hub (Layer 1)**: All physical skill files reside in `~/.skills/`.
- **Agent Directories (Layer 2)**: Individual agents (e.g., `~/.claude/skills/`) contain only symbolic links to the Global Hub.
- **Universal/Specific (Dimensions)**: Skills are broadcast to all or selected agents based on their `meta.yaml` configuration.

---

## 🛠 The Skill Ecosystem

`skill-manager` works in harmony with two other core components:

### 1. [skill-creator](https://github.com/ZiweiAxis/skill-creator) (The Builder)
- **Role**: Used to scaffold and build new skills from scratch.
- **Workflow**: 
  1. Use `skill-creator` to generate a new skill folder in `~/.skills/`.
  2. Define the agent instructions in `SKILL.md`.
  3. **Handoff**: Once the skill is ready, use `skill-manager` to distribute it.

### 2. [skill-installer](https://github.com/ZiweiAxis/skill-installer) (The Courier)
- **Role**: Pulls or updates skills from external registries like ClawHub or SkillHub.
- **Workflow**:
  1. Run `clawhub install <skill-name>`.
  2. The installer places the skill in the Global Hub.
  3. **Handoff**: Call `skill-manager` to ensure the new skill is symlinked to the appropriate agent directories.

---

## 📖 Usage Guide

### Syncing Skills
To synchronize the entire system based on current `meta.yaml` definitions:
```bash
./scripts/sync_skills.sh
```
This script will:
1. Scan all skills in `~/.skills/`.
2. Read the `scope` field in each `meta.yaml`.
3. Create or remove symlinks in agent-specific directories (defined in `agents.yaml`).

### Configuring Scope
Every skill must have a `meta.yaml`.
```yaml
name: "my-skill"
version: "1.0"
scope: "universal" # or ["claude_code", "cursor"]
```
- `universal`: Skill is available to ALL registered agent platforms.
- `[list]`: Skill is only symlinked to the specified agents.

---

## 🏗 Directory Structure
- `scripts/`: Implementation of the sync and migration engines.
- `references/`: Schemas and documentation for the USM standard.
- `meta.yaml`: Meta-definition for the manager itself.
- `SKILL.md`: The AI-facing instruction router for this skill.
