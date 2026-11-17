## Description:

Captures learnings, errors, and corrections so coding agents can maintain concise self-improvement notes for future work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huihuilu](https://clawhub.ai/user/huihuilu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, feature requests, and reusable lessons during coding sessions. It is intended for project or workspace learning logs that can later be reviewed and promoted into durable agent guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning notes and promoted guidance can introduce incorrect or misleading agent behavior if accepted without review.

Mitigation: Review learning entries and proposed promotions manually before adding them to persistent agent context files or sharing them across sessions.

Risk: Learning logs may capture secrets, private configuration, raw command output, or transcript details.

Mitigation: Record short sanitized summaries, redact sensitive values, and avoid storing full source files, environment variables, tokens, or private keys.

Risk: Optional hooks can inspect command output and inject reminders into agent context.

Mitigation: Keep hooks opt-in, project-scoped, and narrowly matched; enable error-detection hooks only in trusted environments.

Risk: The evidence reports conflicting package identities and an unrelated gog dependency.

Mitigation: Resolve the skill-a, skill-b, and skill-gitee identity mismatch and remove the unrelated gog requirement before enabling hooks or promoting the release.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local .learnings markdown files and may provide optional hook configuration reminders.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
