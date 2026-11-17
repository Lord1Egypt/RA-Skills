## Description:

Audits software and AI-agent security across Windows, macOS, and Linux/WSL, correlates findings with vulnerability feeds, and supports approved updates with post-remediation verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexar69-pixel](https://clawhub.ai/user/alexar69-pixel)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and system administrators use this skill to inventory software, identify vulnerabilities and AI-agent exposures, plan approved package updates, and verify their results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved package updates can change system software.

Mitigation: Review the generated plan and hash before applying updates, and verify installed versions afterward.

Risk: Stored reports and cache files may retain software inventory and masked credential-exposure evidence.

Mitigation: Restrict access to ~/.security-maintainer and review retained reports and cache files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexar69-pixel/skills/security-maintainer)
- [Vulnerability mapping reference](artifact/references/vulnerability_mapping.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown and JSON reports, remediation plans, and verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Applying updates requires approval of a plan ID and hash.]

## Skill Version(s):

1.2.5 (source: skill metadata, pyproject.toml, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
