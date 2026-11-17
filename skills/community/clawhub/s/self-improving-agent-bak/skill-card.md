## Description:

Captures agent learnings, command errors, corrections, feature requests, and reusable patterns so future sessions can review or promote them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robertstarry-gif](https://clawhub.ai/user/robertstarry-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record corrections, command failures, knowledge gaps, and feature requests in workspace learning files, then promote broadly useful lessons into agent guidance or reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs may capture secrets, user data, or raw conversation details.

Mitigation: Review entries before writing or promoting them, redact sensitive data, and avoid copying raw conversation text into learning or instruction files.

Risk: Incorrect or misleading lessons may be promoted into future agent instruction files.

Mitigation: Require human review before promotion, keep promoted files version-controlled, and scan changes before deployment.

Risk: Global hooks may repeatedly inject memory and learning reminders into future sessions.

Mitigation: Enable hooks only when persistent agent memory is desired, prefer project-scoped configuration, and periodically review or disable stale hooks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/robertstarry-gif/skills/self-improving-agent-bak)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and optional generated skill scaffold files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning logs and generated skill scaffold files when the user or configured hooks apply the guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
