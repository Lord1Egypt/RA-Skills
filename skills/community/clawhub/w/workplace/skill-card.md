## Description:

Manage multiple workplaces with multi-agent orchestration, isolated memory, inter-agent communication, IDE context sync, and Telegram or Discord workplace controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dickwu](https://clawhub.ai/user/dickwu)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to initialize, switch, scan, synchronize, and manage multiple project workplaces while coordinating role-based agents and persistent project context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently alter project and agent state across repositories.

Mitigation: Review generated .workplace files and registry changes before relying on them for future sessions.

Risk: The skill can sync project and agent context into IDE instruction files and external memory.

Mitigation: Avoid syncing untrusted agent definitions or sensitive project context into Cursor, Claude Code, OpenCode, or supermemory.

Risk: The skill can support background agent workflows and deployment-related commands.

Mitigation: Require confirmation before deployment actions, child-repository initialization, or starting persistent/background agents.

Risk: The Rust build path may prompt users to install a toolchain through a remote shell command.

Mitigation: Inspect any Rust installation command before running it and prefer an already trusted local toolchain.

## Reference(s):

- [Workplace Skill Page](https://clawhub.ai/dickwu/skills/workplace)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Agent System](references/agent-system.md)
- [Chat Protocol](references/chat-protocol.md)
- [Command Reference](references/commands.md)
- [IDE Sync Guide](references/ide-sync.md)
- [Initialization Guide](references/init-guide.md)
- [Telegram UI Guide](references/telegram-ui.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON, JSONC, MDC, and Markdown configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local workplace registries, per-project .workplace directories, agent definitions, deployment templates, IDE context files, and chat/session state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
