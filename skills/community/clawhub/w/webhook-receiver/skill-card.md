## Description:

Receive external webhooks and callbacks in real time by exposing a local HTTP endpoint via aitun tunnel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctz168](https://clawhub.ai/user/ctz168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to receive third-party webhooks, OAuth callbacks, payment notifications, form submissions, and other HTTP callbacks in local workflows without deploying a public server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer commands may execute remote scripts or unpinned packages.

Mitigation: Prefer a pinned package or verified release, and avoid pipe-to-shell installers unless the installation path has been reviewed.

Risk: Public webhook examples can expose local handlers to untrusted requests.

Mitigation: Bind local handlers narrowly where possible, verify webhook signatures, and return responses quickly.

Risk: Webhook logs may capture sensitive payloads, headers, signatures, cookies, personal data, or payment details.

Mitigation: Redact sensitive data from logs before storing or sharing them.

## Reference(s):

- [AiTun Homepage](https://aitun.cc)
- [ClawHub Skill Page](https://clawhub.ai/ctz168/skills/webhook-receiver)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, Python code examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public tunnel URLs and local webhook handler examples that should be reviewed before use.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
