## Description:

Key lifecycle management with Volcengine KMS. Use when users need key creation, rotation policies, encryption/decryption workflows, or key permission troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:


## Use Case:

Developers, security engineers, and cloud operators use this skill to manage Volcengine KMS key lifecycle tasks, encryption and decryption workflows, signing operations, and key permission troubleshooting with least-privilege checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: KMS actions can affect encryption keys and access to protected data.

Mitigation: Confirm the target account, key, operation, permissions, and logging expectations before allowing key creation, rotation, encryption, decryption, or signing actions.

Risk: Plaintext secrets could be exposed during key-management workflows.

Mitigation: Do not expose plaintext secrets in logs or responses, and return only needed key metadata, operation results, and audit hints.

## Reference(s):

- [Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with operational checklists and audit hints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, persistence, or hidden data handling is present in the release evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
