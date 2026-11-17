## Description:

Sentry error tracking - list, triage, and resolve issues; manage releases and source maps via CLI and REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Sentry issues, fetch event details and stack traces, classify incident severity, and manage issue or release state through sentry-cli and the Sentry REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live Sentry issue, release, deploy, and source-map state.

Mitigation: Require explicit human approval before resolve, ignore, assign, release/deploy, source-map upload, or bulk-update actions.

Risk: The skill requires access to Sentry data through sentry-cli and REST API credentials.

Mitigation: Use a least-privileged Sentry token and install the CLI only from a verified package source.

## Reference(s):

- [Sentry REST API](https://sentry.io/api/0)
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/sentry-error-triage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and REST API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Sentry CLI commands, curl requests, issue classifications, and remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
