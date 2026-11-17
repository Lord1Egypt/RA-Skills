## Description:

Logs agent-infrastructure issues such as prompt drift, rule conflicts, hook failures, and context bloat, with optional project-scoped reminders and reviewed-diff safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to record recurring agent-infrastructure issues, keep redacted learning logs, and propose reviewed improvements to prompt files, hooks, memory policies, and skill templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent infrastructure logs can capture sensitive prompt, command, or environment details.

Mitigation: Keep .learnings entries short and redacted; do not log secrets, tokens, private keys, environment variables, raw hook output, or full transcripts.

Risk: Optional hooks run with agent permissions and may inspect command output when enabled.

Mitigation: Keep hooks project-scoped, enable them only when needed, and avoid the optional PostToolUse output detector in untrusted workspaces.

Risk: Generated skill scaffolds may contain incomplete or unsuitable guidance if kept without review.

Mitigation: Review generated SKILL.md files before keeping or publishing them, and apply infrastructure changes only from a reviewed diff requested in the current session.

## Reference(s):

- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/jose-compu/skills/self-improving-meta)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, learning-log templates, and optional skill scaffold text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default behavior is log-only; file creation and skill scaffolding are user-gated and should be reviewed before publishing.]

## Skill Version(s):

1.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
