## Description:

Compute SHA-256 cryptographic hash values for files and text. Use for secure data verification and integrity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, release engineers, and operators use this skill to compute SHA-256 checksums for file integrity verification, software distribution checks, and related data authentication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented stdin example may not work with the inspected bundled script, which hashes a file argument and otherwise defaults to a local file named a.txt.

Mitigation: Use an explicit file argument when invoking the helper, and verify command wiring before publishing stdin-based examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/sha256-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with bash command examples and hexadecimal SHA-256 checksum text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script emits a single SHA-256 digest for a file argument.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
