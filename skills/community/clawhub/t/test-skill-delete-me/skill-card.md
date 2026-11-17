## Description:

Captures learnings, errors, and corrections so coding agents can maintain reusable project memory and improve recurring workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexecuteinc](https://clawhub.ai/user/nexecuteinc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, feature requests, and reusable practices in structured markdown learning logs. It also provides optional hook reminders and a helper for extracting high-value learnings into reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and promoted workspace memory can preserve incorrect, sensitive, or overbroad guidance.

Mitigation: Keep .learnings local by default, redact secrets and sensitive details, and require explicit review before promoting entries into agent instruction files.

Risk: Global hooks and cross-session context can inject reminders or learning material into sessions where they are not intended.

Mitigation: Enable hooks deliberately, scope them to appropriate projects or workspaces, and review cross-session transcript or message use before sharing context.

Risk: Captured command outputs or transcripts may include confidential project, personal, or business information.

Mitigation: Log concise summaries instead of raw transcripts, remove sensitive command output, and supervise any extracted skill before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nexecuteinc/skills/test-skill-delete-me)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and reusable templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local .learnings files, workspace guidance files, hook reminders, or new skill scaffolds when the user enables those workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
