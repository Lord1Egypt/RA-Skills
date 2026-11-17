## Description:

Extracts durable workflow preferences and project conventions from a session, then proposes the smallest valid update to global or project CLAUDE.md files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lq434239](https://clawhub.ai/user/lq434239)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to identify durable workflow preferences or project conventions from a session and propose compact updates to global or project CLAUDE.md files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable CLAUDE.md updates can change future agent behavior in unintended ways.

Mitigation: Review proposed rule changes carefully and keep confirmation enabled before writing.

Risk: Automatic session-end writes can persist unwanted memory updates if enabled without sufficient trust.

Mitigation: Avoid automatic session-end writes unless the workflow is trusted and durable memory updates are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lq434239/skills/self-improving-session)
- [Merge Reference Details](references/details.md)
- [Learning Rules](references/learning-rules.md)
- [Rule Quality Guide](references/rule-quality.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration guidance]

**Output Format:** [Markdown bullets and concise prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposes the smallest valid CLAUDE.md update and defaults to user confirmation before writing.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
