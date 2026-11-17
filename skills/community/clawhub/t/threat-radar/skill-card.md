## Description:

Continuously scans Docker images, dependencies, network ports, SSL/TLS, and OpenClaw configuration for CVE-related security findings and produces alerts and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:


## Use Case:

Developers and operators running OpenClaw infrastructure use this skill to review local services, dependencies, container images, configuration, and CVE status, then receive security posture summaries and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the skill materially overstates CVE and SSL capabilities.

Mitigation: Do not rely on it as a real vulnerability scanner until the mock CVE feed and SSL validation are fixed; verify findings with trusted security tools.

Risk: The skill can scan workspace dependency files, Docker image names, OpenClaw configuration, and credential-file metadata.

Mitigation: Review scan scope before installation, restrict workspace access where appropriate, and avoid running it in sensitive environments without approval.

Risk: The security guidance calls for confirming alerting and network behavior before sensitive use.

Mitigation: Validate configured notification channels and network activity before enabling scheduled scans or alerts.

## Reference(s):

- [Threat Radar ClawHub listing](https://clawhub.ai/mariusfit/skills/threat-radar)
- [NVD CVE example reference](https://nvd.nist.gov/vuln/detail/CVE-2021-23337)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Configuration, Guidance]

**Output Format:** [CLI text, JSON, CSV, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes severity summaries, scan history, watched software entries, and remediation suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
