## Description:

Compute SHA family hash values for file integrity verification. Use for checksums, data validation, and security verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security practitioners use this skill to compute and compare SHA checksum values for file integrity, data validation, and authenticity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation describes SHA-1, SHA-256, SHA-384, and SHA-512 behavior, while the included helper computes SHA-256 only.

Mitigation: Verify installed command behavior before relying on non-SHA-256 algorithms.

## Reference(s):

- [Sha Tool ClawHub page](https://clawhub.ai/dinghaibin/skills/sha-tool)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text hash values and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [File or stdin input; included helper computes SHA-256.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
