---
name: skill-manager
description: [USM] Manages the distribution and visibility of skills across multiple AI Agents using the 2-layer 2-dimension Universal Skill Manager architecture. Use this skill when asked to "sync skills," "manage agents," "change a skill's scope/availability," "make a skill universal," or when investigating which skills are available to which agents.
---

# Skill Manager

You are the central manager of the **Universal Skill Manager (USM)** architecture.

This system resolves the fragmentation of skills across multiple AI Agents (Cursor, Claude Code, Codex, Gemini, OpenClaw, etc.) by maintaining a Single Source of Truth for skills.

## The Architecture (2-Layer 2-Dimension)

- **2 Layers**:
  1. `~/.skills/` (Global Hub) and `./.skills/` (Project Hub): This is where the physical skill files natively reside.
  2. Agent Directories (e.g., `~/.claude/skills/`, `~/.openclaw/skills/`): These directories simply contain **symlinks** pointing to the real skills in the Hub.

- **2 Dimensions** (Scope / Visibility):
  1. `universal`: A skill available to ALL registered Agents.
  2. Specific (e.g. `claude_code`, `cursor`): A skill restricted to specific Agents only.

## Specialist Agents (Progressive Disclosure)

When performing complex setup or configuration tasks, read the specialized instructions for the corresponding domain:

1. **New Skill Provisioning**: (Setting up `meta.yaml` and distributing a newly created/installed skill)
   👉 Read `agents/provision_agent.md`

## Your Responsibilities

### 1. Synchronizing Skills
Whenever a new skill is created (by `skill-creator`), a skill is installed (by `skill-installer`), or a skill's metadata is changed, you **MUST** run the synchronization script to update the symlinks.

**Command:**
```bash
bash ~/.skills/skill-manager/scripts/sync_skills.sh
```
Add `--project-dir <path>` if you need to synchronize project-level skills as well.

### 2. Managing Agent Platforms
The list of supported Agent platforms and their directories is stored in `~/.skills/agents.yaml`.
If the user wants to add support for a new Agent, manually add it to `agents.yaml` and then run the sync script.

### 3. Modifying Skill Scope
Each skill in the Hub has a `meta.yaml` file defining its dimension.
Schema details are in `references/meta_schema.md`.

Example `meta.yaml`:
```yaml
name: "doubao-image-gen"
version: "1.0"
# "universal" applies to all agents
scope: "universal"
# Or target specific agents:
# scope:
#   - cursor
#   - openclaw
```
If the user says: "Make `skill-xyz` visible to Cursor", you edit `~/.skills/skill-xyz/meta.yaml` to add `cursor` to its scope, then run `sync_skills.sh`.

### 4. Auditing Skill Distribution
If the user asks "Which skills are available to Claude?", you can check the scope fields in the various `meta.yaml` files in `~/.skills/`, or simply list the contents of the `~/.claude/skills/` directory to see the symlinks.

## Handoff & Lifecycle Integration

`skill-manager` acts as the **Final Stage** in the skill lifecycle. 

- **From `skill-creator`**: Once a new skill is drafted and verified, you are called to provision its metadata and sync it.
- **From `skill-installer`**: Once a remote skill is downloaded, you are called to distribute it to the local agent directories.

**CRITICAL**: In these handoff scenarios, you MUST immediately read `agents/provision_agent.md` and follow its workflow to complete the task. Do not simply run the sync script without verifying the `meta.yaml`.
