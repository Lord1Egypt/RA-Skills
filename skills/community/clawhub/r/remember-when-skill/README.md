# Remember When - OpenClaw Skill

This skill transforms an OpenClaw agent into a **Digital Archivist**. It enables the agent to monitor conversations, identify memorable content, and persist it to a local storage engine via CLI.

## 🚀 Installation

The recommended way to install this skill is via `skills.sh`:

```bash
npx skills add https://github.com/2mes4/remember-when --skill remember-when-skill
```

## 🛠 Features for Agents
- **Automatic Summarization**: Converts raw chat logs into meaningful memories.
- **Media Persistence**: Copies shared photos, videos, and audios to local daily folders.
- **Context Awareness**: Remembers who is in the group and what the group is for.
- **Autonomous Auditing**: Uses the `inventory` command to identify and fill gaps in history.

## 📋 Requirements
- **Remember-When CLI**: Must be installed and available in the system PATH.
- **Shell Access**: The agent must have permissions to execute local terminal commands.

## 📖 Instructions (SKILL.md)
The core logic resides in `SKILL.md`, which acts as the System Prompt for the agent. It defines the "Archivist" persona and provides exact syntax for command execution.
