## Description:

Provides an agent workflow for statically scanning an authorized project directory for common credential patterns and preparing a masked findings report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check authorized project directories for common credential patterns before committing and to prepare a masked findings report with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation command is unpinned, and the supplied material does not establish that the advertised credential scan works; some code was only partially inspected.

Mitigation: Pin and review the installer and skill revision, then verify the scanning behavior before relying on reports.

## Reference(s):

- [Secret Leak Scan Lite on ClawHub](https://clawhub.ai/nenadzivotic/skills/secret-leak-scan-lite)
- [Publisher profile: nenadzivotic](https://clawhub.ai/user/nenadzivotic)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON findings report followed by a concise remediation list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The intended report identifies pattern type, file, line, and a masked fingerprint; findings are treated as potentially live credentials.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
