## Description:

Encrypt API keys, tokens and passwords with age to protect secrets in your workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asistentegordito](https://clawhub.ai/user/asistentegordito)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users use this skill to encrypt API keys, tokens, and passwords with age before storing secrets in repositories or backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The usage flow sources decrypted secrets as shell code.

Mitigation: Decrypt only trusted files, validate simple key-value assignments before loading them, and avoid sourcing decrypted files from repositories or shared workspaces.

Risk: The scripts and documentation disagree between /root/.age/key.txt and $HOME/.age/key.txt.

Mitigation: Reconcile the key path before use and avoid running the workflow as root.

Risk: The skill runs local shell scripts around sensitive secret material.

Mitigation: Audit and adjust the workflow before installation or deployment, and confirm the age dependency is installed from a trusted source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asistentegordito/skills/secure-workspace-en)
- [Artifact homepage](https://github.com/asistentegordito/secure-workspace)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the age command-line tool and may create encrypted .age files and local age key material.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
