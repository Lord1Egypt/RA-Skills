## Description:

Securely interact with Bitwarden/Vaultwarden vaults using rbw CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tripleight](https://clawhub.ai/user/tripleight)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to retrieve and manage Bitwarden or Vaultwarden items with the rbw CLI, including field access, synchronization, scripted usage, and systemd service integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Non-interactive automation examples can persist or expose a Bitwarden/Vaultwarden master password.

Mitigation: Prefer interactive unlock, systemd LoadCredential or LoadCredentialEncrypted, or another secret manager; avoid plaintext credential files and passwords in shell commands or inherited environments.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and systemd configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides command patterns, troubleshooting guidance, and secure automation considerations for rbw.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
