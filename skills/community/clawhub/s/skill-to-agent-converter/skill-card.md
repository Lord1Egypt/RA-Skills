## Description:

Convert OpenClaw skills into properly configured agents with correct workspace setup, binding, and orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drafthead](https://clawhub.ai/user/drafthead)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert OpenClaw skills into autonomous agents with workspace setup, identity and tool configuration, registration, and session spawning guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide persistent agent creation, OpenClaw agent configuration changes, and session spawning.

Mitigation: Use a test workspace first, review proposed configuration changes before applying them, and confirm the affected agents list before restarting or spawning agents.

Risk: Examples and generated workflows may expose session keys or agent memory if stored without access controls.

Mitigation: Do not store session keys in plaintext, keep agent identity and memory files private, and use restrictive filesystem permissions.

Risk: Cleanup examples may delete agent data if followed without review.

Mitigation: Replace destructive cleanup commands with preview, quarantine, backup, or restore-based procedures.

## Reference(s):

- [Usage Guide](references/usage-guide.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [War Room Skill Conversion Example](references/war-room-example.md)
- [ClawHub Skill Page](https://clawhub.ai/drafthead/skills/skill-to-agent-converter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent agent configuration changes and session-spawning commands.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
