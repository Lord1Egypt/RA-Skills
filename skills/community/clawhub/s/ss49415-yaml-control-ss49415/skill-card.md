## Description:

Inert control skill used to measure parser behaviour of the prepublication scanner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bucsaradu](https://clawhub.ai/user/bucsaradu)

### License/Terms of Use:

MIT-0

## Use Case:

Security and platform engineers use this control fixture to assess how a prepublication scanner parses YAML metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags host/user checks and listing environment-variable names as unexplained by the stated purpose.

Mitigation: Review the script before installing, and run it only where this system metadata can be logged or shared safely.

Risk: The security scan was partial because a referenced path was missing and a binary file was outside analyzer coverage.

Mitigation: Review the full package, including files the analyzer did not cover, before relying on the scan.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bucsaradu/skills/ss49415-yaml-control-ss49415)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The probe prints a marker, hostname, user ID, and environment variable names.]

## Skill Version(s):

0.0.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
