## Description:

Generate, validate, and lint systemd unit files (.service, .timer, .socket, .mount) with hardening and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate systemd service, timer, socket, and mount unit configurations and to validate or lint existing units before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated systemd units may create privileged services or exposed sockets if reviewed and deployed without changes.

Mitigation: Review every generated unit before installing or enabling it; prefer explicit non-root users and bind sockets to 127.0.0.1 unless public exposure is intended.

Risk: The linter is not a complete systemd security review.

Mitigation: Treat lint results as advisory and perform a separate systemd security review for production services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/systemd-unit-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, generated systemd unit content, and optional JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write generated unit output to a file when requested by the user.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
