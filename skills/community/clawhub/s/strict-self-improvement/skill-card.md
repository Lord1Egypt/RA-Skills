## Description:

Captures agent learnings, errors, corrections, and feature requests in structured local records so recurring issues can be reviewed before promotion into persistent guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayv29](https://clawhub.ai/user/jayv29)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to log corrections, command failures, knowledge gaps, and requested capabilities, then apply a Rule of 3 review process before promoting recurring guidance into agent workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local learning records and hook-generated reminders can influence future agent behavior.

Mitigation: Prefer project-local setup, avoid user-global hooks, use restrictive matchers, and review scripts before enabling hooks.

Risk: Logs may contain secrets, personal data, private business context, raw prompts, or sensitive command output.

Mitigation: Redact sensitive content before logging or promoting entries, and require human review before persistent guidance updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jayv29/skills/strict-self-improvement)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and structured log-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local memory records and optional hook configuration; recurring promotions are intended for human review.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
