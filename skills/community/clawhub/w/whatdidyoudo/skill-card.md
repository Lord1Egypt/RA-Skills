## Description:

Reconstruct and display a plain-language log of recent agent tool calls, actions taken, and decisions made.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openauthority](https://clawhub.ai/user/openauthority)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review what an agent recently did in the current session, including tool calls, file operations, commands, and high-level decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Action summaries may reveal filenames, command names, and workflow details from the current session.

Mitigation: Use the skill for the current user's transparency review, rely on the redaction policy for secrets, and avoid sharing generated summaries outside the intended audience without review.

Risk: The output is a narrative reconstruction from current session context, not a structured audit log.

Mitigation: Use it for quick session review, and use a production audit log when exact arguments, timestamps, response codes, or policy decisions are required.

## Reference(s):

- [What Did You Do ClawHub listing](https://clawhub.ai/openauthority/skills/whatdidyoudo)
- [OpenAuthority plugin audit log reference](https://github.com/Firma-AI/openauthority)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown/plain text action summaries with numbered lists and summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redacts credential-like values and avoids full file contents; output is reconstructed from current session context rather than a structured audit log.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
