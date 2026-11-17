## Description:

Build full-stack web applications through 语构's chat-driven platform, including conversation management, development instruction delivery, build monitoring, result extraction, publishing, and version management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yugoo](https://clawhub.ai/user/yugoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, iterate, publish, and manage full-stack web applications on the 语构 platform from focused natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform credential-bearing network operations against the 语构 platform.

Mitigation: Use a revocable, least-privilege CREO4U_SKILL_API_KEY and avoid untrusted YUGOO_BASE_URL values.

Risk: The skill supports public publishing and destructive actions such as unpublishing, deleting conversations, and deleting versions.

Mitigation: Require explicit user approval before publishing, unpublishing, deleting conversations, deleting versions, finalizing versions, or uploading local files.

Risk: The --insecure option disables TLS certificate verification while transmitting authenticated requests.

Mitigation: Do not use --insecure except in controlled test environments with non-production credentials.

Risk: Generated applications may expose secrets or unsafe behavior if published without review.

Mitigation: Inspect generated applications for secrets and unsafe behavior before making them public.

## Reference(s):

- [语构 App Builder ClawHub listing](https://clawhub.ai/yugoo/skills/yugoo-app-builder)
- [yugoo publisher profile](https://clawhub.ai/user/yugoo)
- [语构 homepage](https://creo4u.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON-line command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CREO4U_SKILL_API_KEY for authenticated platform operations and may produce links to generated preview or published applications.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
