## Description:

Captures learnings, errors, and corrections to enable continuous improvement for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinqing](https://clawhub.ai/user/xinqing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record command failures, user corrections, missing capabilities, knowledge gaps, and reusable best practices in structured markdown logs. The skill also guides review and promotion of broadly useful learnings into future agent context when trusted by a human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived learnings can become persistent memory or future agent instructions.

Mitigation: Review every proposed entry and require trusted human approval before promoting content into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Risk: Hook-based reminders and error detection can broaden when learning capture is triggered.

Mitigation: Keep hooks opt-in and scoped, prefer the minimal activator hook by default, and avoid user-level always-on configuration unless the environment is trusted.

Risk: Logs may accidentally capture secrets, raw command output, transcripts, or private configuration.

Mitigation: Record concise sanitized summaries, redact sensitive values, and avoid logging full outputs or environment data unless explicitly approved.

## Reference(s):

- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [ClawHub Skill Page](https://clawhub.ai/xinqing/skills/wx-1212)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends structured learning, error, and feature-request entries; hook behavior is opt-in.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
