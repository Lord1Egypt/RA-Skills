## Description:

Get your agent identity (email, phone, owner name) and manage identities. Do NOT use for reading messages (use ravi-inbox), sending email (use ravi-email-send), or credentials (use ravi-passwords or ravi-secrets).

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunaksingwi](https://clawhub.ai/user/raunaksingwi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Ravi-provided email, phone, and owner identity details and to list, create, or switch permanent identities when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive identity data such as email addresses, phone numbers, owner details, and identity UUIDs.

Mitigation: Treat returned identity details as sensitive and share or store them only when needed for the user's task.

Risk: Creating or switching identities can have permanent account effects and may require a paid plan.

Mitigation: Create or switch identities only after explicit user instruction and confirm paid-plan implications before creating a new identity.

## Reference(s):

- [Ravi Identities API Reference](https://ravi.id/docs/schema/identities.json)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, JSON]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sensitive identity details such as email addresses, phone numbers, owner details, and identity UUIDs.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
