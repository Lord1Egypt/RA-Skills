## Description:

Captures learnings, errors, corrections, and feature requests so agents can record recurring issues and improve future workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[czubi1928](https://clawhub.ai/user/czubi1928)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to capture command failures, user corrections, missing capabilities, and reusable process improvements as structured learning records. It also guides promotion of broadly applicable learnings into project or workspace memory after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files or promoted memory can carry incorrect guidance into future agent sessions.

Mitigation: Review logged learnings before reuse and require human approval before promoting entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or copilot-instructions.md.

Risk: Learning logs can capture secrets, private data, or sensitive operational context.

Mitigation: Redact secrets and private data before logging, and keep .learnings local or gitignored unless the contents have been reviewed.

Risk: Broad or user-level hooks can inject reminders in more contexts than intended.

Mitigation: Use narrow hook matchers, avoid user-level hooks, and install hooks only when persistent learning behavior is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/czubi1928/skills/self-improving-agent-1-0-5)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell-command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in persistent .learnings files or reviewed updates to agent instruction files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
