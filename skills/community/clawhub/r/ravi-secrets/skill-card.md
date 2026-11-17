## Description:

Store and retrieve key-value secrets in the Ravi encrypted secret store for API keys, environment variables, and tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunaksingwi](https://clawhub.ai/user/raunaksingwi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to store, list, retrieve, and delete key-value secrets such as API keys, environment variables, and service tokens through the Ravi secrets CLI. It is intended for secret values and notes, not website passwords or message access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secret values are sent to and returned from the Ravi secrets service as plaintext.

Mitigation: Install and use the skill only where that service boundary is acceptable, and avoid sharing or logging retrieved values.

Risk: Shell examples that pass tokens directly on the command line or list all secrets can expose sensitive values through shell history, process inspection, terminal scrollback, or logs.

Mitigation: Prefer narrowly scoped retrieval, avoid bulk listing when possible, and avoid pasting real tokens directly into reusable shell commands.

## Reference(s):

- [Ravi Secrets API schema](https://ravi.id/docs/schema/secrets.json)
- [ClawHub skill page](https://clawhub.ai/raunaksingwi/skills/ravi-secrets)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output can include plaintext secret values and should be handled as sensitive data.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
