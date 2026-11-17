## Description:

Guides an agent through autonomous signup for external web services, including browser automation, email verification, API key generation, and secure storage in 1Password.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create and bootstrap accounts on external web services while preserving authenticated browser session continuity, completing email or passkey verification, generating API keys, and storing resulting credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad authority for autonomous account creation, email access, API key creation, secret storage, and environment changes.

Mitigation: Use only in approved environments and require explicit approval before signup, paid tiers, API key generation, secret storage, or environment changes.

Risk: Signup details are sent to a hard-coded Notion registry.

Mitigation: Remove the registry requirement or make it opt-in before using the skill for general users.

Risk: Credential handling depends on access to email, browser sessions, and 1Password vault writes.

Mitigation: Limit email and vault scope, review generated secrets before reuse, and ensure credentials belong only to intended agent-controlled accounts.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser automation steps, API calls, credential storage commands, and environment variable wiring guidance.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
