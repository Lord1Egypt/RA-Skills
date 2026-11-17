## Description:

Triple Layer Memory helps agents preserve long-conversation context through Mem0 retrieval, structured workspace memory files, and session compression and handoff workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0range-x](https://clawhub.ai/user/0range-x)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add persistent memory, session handoff, quality gating, and channel-aware recall to OpenClaw workspaces. It is intended for long-running agent sessions where continuity across context windows matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes future agent behavior through memory, agent startup, and heartbeat instructions.

Mitigation: Install it only in an isolated workspace where this behavior is desired, and review or remove the MEMORY.md, AGENTS.md, and HEARTBEAT.md snippets before use.

Risk: Long-lived memory files can retain secrets, regulated data, or incorrect context across sessions.

Mitigation: Avoid storing secrets or regulated data, inspect memory entries regularly, and archive or delete entries that should not influence future work.

Risk: Security evidence reports broken scoping controls for multi-channel or multi-user use.

Mitigation: Fix channel authorization and filename validation before using the skill across multiple channels or users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0range-x/skills/triple-layer-memory)
- [Skill usage guide](SKILL.md)
- [Mem0 channel isolation guide](docs/mem0-channel-isolation.md)
- [Memory architecture template](templates/MEMORY_ARCHITECTURE.md)
- [Mem0](https://github.com/mem0ai/mem0)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks, plus workspace memory files and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may create or update persistent workspace memory, session handoff, heartbeat, and archive files.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
