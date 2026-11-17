## Description:

Helps agents encrypt workspace API keys, tokens, and passwords with age and decrypt them when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asistentegordito](https://clawhub.ai/user/asistentegordito)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up age key material and encrypt or decrypt workspace secret files during local automation and repository backup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended decrypt workflow can run decrypted secret files as shell code and expose secrets in the live shell environment.

Mitigation: Avoid sourcing decrypted content from repositories, backups, or other people; prefer decrypting only for a specific command or parsing a strict dotenv format after review.

Risk: The age private key file unlocks encrypted workspace secrets.

Mitigation: Treat /root/.age/key.txt or $HOME/.age/key.txt as highly sensitive private key material and protect it with appropriate filesystem permissions and backup controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asistentegordito/skills/secure-workspace)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the age command-line tool and local key files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
