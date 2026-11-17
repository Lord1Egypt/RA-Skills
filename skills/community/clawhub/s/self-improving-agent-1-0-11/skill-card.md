## Description:

Captures learnings, errors, corrections, and feature requests so agents can record lessons and promote durable guidance into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kgy7247](https://clawhub.ai/user/kgy7247)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to capture command failures, user corrections, knowledge gaps, feature requests, and recurring patterns in markdown learning logs. They can later review those logs and promote selected learnings into project or agent memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived content may be persisted and promoted into future agent instruction files, which can amplify incorrect or misleading guidance.

Mitigation: Require human review before promoting any learning into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, Copilot instruction files, or other durable agent memory.

Risk: Learning logs can accidentally capture secrets, raw transcript content, or sensitive operational details.

Mitigation: Do not log secrets or raw transcripts; redact sensitive command output and keep entries focused on reusable lessons.

Risk: Broad or global hooks can add persistent reminder behavior across sessions and projects.

Mitigation: Keep hooks project-scoped and opt-in, avoid global every-prompt hooks, and disable hooks when durable memory behavior is not desired.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance, Code]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional hook reminders and shell helper scripts for logging errors and extracting reusable skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
