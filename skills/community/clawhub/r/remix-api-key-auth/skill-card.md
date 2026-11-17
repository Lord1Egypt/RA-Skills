## Description:

Configure and verify bearer API key authentication for Remix agent publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuckstock](https://clawhub.ai/user/chuckstock)

### License/Terms of Use:


## Use Case:

Developers and agent publishers use this skill to create, store, configure, verify, and troubleshoot Remix API keys for server-side agent publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Remix API key may be exposed if copied into browser code, logs, or non-secret configuration.

Mitigation: Store the key only in server-side secret management and rotate it if exposure is suspected.

Risk: Authentication verification calls could affect a real project if run directly in production.

Mitigation: Use a test project or low-impact authenticated request when validating the key.

## Reference(s):

- [Remix API Keys](https://remix.gg/api-keys)
- [Remix API Base URL](https://api.remix.gg)
- [Remix API Documentation](https://api.remix.gg/docs)
- [ClawHub Skill Page](https://clawhub.ai/chuckstock/skills/remix-api-key-auth)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, URLs, and HTTP header examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
