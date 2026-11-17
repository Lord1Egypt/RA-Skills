## Description:

Guides users through generating transmission CAD drawings and creating guest production sheets through the JXT mechanical parts workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External engineering users use this skill to select transmission products, provide design inputs, review calculated parameters, adjust values, and create guest production sheets for CAD drawing generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transmission design inputs are sent to jixietools.com and unauthenticated guest production records may be created there.

Mitigation: Ask for explicit user confirmation before the first external request and before creating a production sheet; do not send sensitive design data unless the user approves.

Risk: Shell API examples can become unsafe if user-provided parameter values are interpolated directly into command strings.

Mitigation: Prefer a structured HTTP client or safely serialized JSON request bodies when executing the workflow.

Risk: Production status polling can continue repeatedly against the external service.

Mitigation: Use bounded polling or ask the user whether to continue monitoring after a reasonable interval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liv09370/skills/transmission)
- [JXT mechanical tools API](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown with tables, status updates, links, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation between workflow steps and may return external production sheet links.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
