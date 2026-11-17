## Description:

Retrieve masked card info from Reah using an access key; handles session generation, secure fetch, and decryption for agents automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelzou](https://clawhub.ai/user/axelzou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent retrieve Reah card details through an access key while keeping payment-card values masked or redacted in user-facing output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles payment-card access keys and decrypted PAN/CVC data.

Mitigation: Require explicit approval before each key read, keep access keys and raw card values out of user-facing responses, mask card info part A, and redact card info part B.

Risk: Broad purchase prompts can authorize unintended card use.

Mitigation: Scope any purchase or card use to a specific user-approved request and avoid broad authorization prompts.

Risk: Real access keys passed as command-line arguments can be exposed through shell history or process inspection.

Mitigation: Avoid putting real access keys in command-line arguments; prefer a confirmed environment-based read or another secure input path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelzou/skills/reah-agent-card)
- [Reah GraphQL endpoint](https://agents.reah.com/graphql)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with masked card details, redaction guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before every environment-based access-key read; raw access keys, secret keys, PAN, and CVC values should not be exposed.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
