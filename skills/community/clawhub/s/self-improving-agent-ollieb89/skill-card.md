## Description:

Capture errors, corrections, and recurring patterns into structured `.learnings/` logs, then promote durable guidance into workspace memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ollieb89](https://clawhub.ai/user/ollieb89)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to capture recurring corrections, command failures, capability gaps, and reusable best practices, then promote durable guidance into workspace memory files for future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to turn conversation feedback into persistent agent instructions without enough approval and scoping controls.

Mitigation: Install only in workspaces where persistent agent-memory updates are desired, prefer project-local hooks over global hooks, and manually review proposed changes to learning or memory files.

Risk: Learning files or memory updates may accidentally preserve secrets, credentials, raw transcripts, or sensitive user data.

Mitigation: Do not store secrets, credentials, raw transcripts, or sensitive user data in `.learnings/`, `SOUL.md`, `AGENTS.md`, `TOOLS.md`, or related memory files.

Risk: Broad hook matchers can inject reminders in sensitive or unrelated workspaces.

Mitigation: Avoid empty matchers in sensitive work and scope hook activation to projects and events where learning capture is explicitly desired.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/ollieb89/skills/self-improving-agent-ollieb89)
- [Entry Examples](references/examples.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update `.learnings/` logs and propose durable workspace-memory updates when the user applies the guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
