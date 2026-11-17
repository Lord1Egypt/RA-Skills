## Description:

Checks UDI device identifiers, production identifiers, and Basic UDI-DI structure for format errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Medical-device developers and regulatory teams use this skill to check UDI format and structure before reviewing registration materials. Results require human verification against issuer records and current requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloading an unreviewed or changed script may expose users to unintended local code execution.

Mitigation: Install the reviewed package or a pinned, trusted source rather than fetching the latest raw script.

Risk: A valid format or check digit may be mistaken for regulatory compliance or proof of an identifier's issuer.

Mitigation: Have a qualified reviewer confirm issuer records and current official UDI requirements before regulatory decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/udi-format-validator)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable validation results or machine-readable JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 0 for pass, 1 for findings, and 2 for usage errors; output is primarily in Chinese.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
