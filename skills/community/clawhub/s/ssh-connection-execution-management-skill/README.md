# SSH MCP OpenClaw Skill

This directory contains the instruction skill manual for the OpenClaw agent. It guides the LLM on how to manage SSH connections, handle persistent sessions, manage keys, and execute bulk operations.

---

## File Contents

* [SKILL.md](file:///save_data/projects/ssh_mcp/skill/SKILL.md): Declares the OpenClaw skill manifest header, YAML metadata, and core instruction prompts.

---

## Usage

When OpenClaw loads this skill, the guidelines in `SKILL.md` are appended to the agent's system prompt or tool-usage instructions. It teaches the agent:
1. To open persistent connections via `ssh_exec` (action `open`) and reuse them across commands.
2. To use `ssh_bulk_exec` or `ssh_bulk_audit` for parallel fleet operations with auto-cleanup of transient sessions.
3. How to check execution progress via `ssh_exec` (action `status`) and stream/filter logs using `ssh_exec` (action `logs`).
4. To link keys cleanly to connection profiles instead of using hardcoded details.
