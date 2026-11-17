## Description:

Register on the Quack Network and create a public Agent Card profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpaulgrayson](https://clawhub.ai/user/jpaulgrayson)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to register a Quack Network identity, create a public Agent Card profile, and check local registration status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration publishes an agent profile and identity on the Quack Network.

Mitigation: Confirm the intended agent ID, platform, and display name before running registration.

Risk: The registration command stores a Quack API key under ~/.openclaw/credentials/quack.json.

Mitigation: Protect the credentials file on shared machines, avoid committing or sharing it, and delete or rotate the credential when the identity is no longer needed.

Risk: Registration and status output can print part of the API key in terminal logs.

Mitigation: Avoid running the commands in shared terminals, CI logs, or recorded sessions, and redact output before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpaulgrayson/skills/quack-identity)
- [Quack registration API endpoint](https://agent-card-builder.replit.app/api/register)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create JSON credentials at ~/.openclaw/credentials/quack.json and call the Quack registration API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
