## Description:

Soul Memory provides local long-term memory management for AI agents, including memory search, tagging, auto-save, heartbeat cleanup, and OpenClaw context injection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofqin2026](https://clawhub.ai/user/kingofqin2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an AI agent local memory retrieval, classification, and context injection workflows. It is especially oriented toward OpenClaw users who want persistent memories, heartbeat cleanup, CLI access, and prompt-time memory summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell execution paths may be unsafe if commands are built or launched without strict argument handling.

Mitigation: Replace shell execution with argument-array execution and avoid passing user-controlled strings through a shell.

Risk: Local memory persistence may capture private memories, credentials, or sensitive context.

Mitigation: Remove credential keywords from capture rules or apply redaction before any memory is persisted.

Risk: Cron and heartbeat changes may alter background behavior without enough operator awareness.

Mitigation: Require explicit opt-in before installing, modifying, or enabling cron and heartbeat automation.

Risk: The web UI may expose stored memory or controls if reachable on a network without protection.

Mitigation: Bind the web UI to localhost, add authentication, and avoid deployment on exposed interfaces until reviewed.

Risk: Unpinned dependencies and privileged execution increase installation and runtime blast radius.

Mitigation: Pin dependencies and run the skill as an unprivileged user.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kingofqin2026/skills/soul-memory)
- [Project Homepage](https://github.com/kingofqin2026/Soul-Memory-)
- [Project README](https://github.com/kingofqin2026/Soul-Memory-/blob/main/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, JSON CLI output, shell commands, and prompt-injected text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local memory/context files and inject selected memory summaries into agent prompts.]

## Skill Version(s):

3.5.13 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
