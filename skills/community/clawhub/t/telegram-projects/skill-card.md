## Description:

Turns Telegram groups into persistent OpenClaw projects with long-lived instructions, knowledge files, project glossaries, and active-project synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain persistent per-Telegram-group project context, including reusable instructions, accumulated knowledge, glossaries, and active project status. It is suited for agents that need continuity across Telegram group conversations inside an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify persistent OpenClaw workspace memory and SOUL.md using local Telegram session data.

Mitigation: Review changes before execution, keep backups of persistent workspace files, and require explicit approval before SOUL.md updates.

Risk: Insufficient chat ID validation could associate or update the wrong Telegram project context.

Mitigation: Add strict chat ID validation and verify project identity before creating, syncing, or loading project memory.

Risk: Telegram-controlled names or content could be loaded into agent context as trusted project material.

Mitigation: Escape Markdown, treat Telegram-provided names and knowledge as untrusted data, and avoid loading them as instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moltbotmolty-del/skills/telegram-projects)
- [Publisher profile](https://clawhub.ai/user/moltbotmolty-del)
- [Project help artifact](artifact/PROJECT_HELP.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and Python scripts that create or update workspace project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify persistent OpenClaw workspace memory, project files, and SOUL.md when scripts are run.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
