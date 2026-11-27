## Description:

Encrypted local secret store for OpenClaw agents. AES-256-GCM authenticated encryption with per-secret random IVs, master key in restricted-permission .master-key file. Store, retrieve, rotate, and audit secrets. Safe command injection writes to a restricted temp file by default and requires explicit confirmation before printing resolved commands. Losing the master key makes stored secrets unrecoverable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to store, retrieve, rotate, audit, and inject local secrets for OpenClaw workflows while keeping default display output masked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential values may be exposed through argv, persistent temp scripts, or audit output.

Mitigation: Review and fix credential handling before storing high-value production credentials; prefer masked output and default temp-file injection until the release has been remediated.

Risk: The release requests shell and elevated permissions that may be broader than necessary.

Mitigation: Limit deployment to reviewed environments, constrain the storage directory, and confirm that elevated permissions are only used for restrictive file-permission enforcement.

Risk: The local master key is required to recover stored secrets.

Mitigation: Back up the master key to a secure location and test recovery before relying on the store for important credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlacroix82/skills/secrets-manager)
- [Publisher profile](https://clawhub.ai/user/jlacroix82)
- [README](artifact/README.md)
- [Vetting report](artifact/VET-REPORT.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [CLI text output, masked secret values by default, and restricted-permission temp shell scripts for command injection]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit plaintext secrets only when explicitly requested through raw retrieval or confirmed stdout injection.]

## Skill Version(s):

1.1.19 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
