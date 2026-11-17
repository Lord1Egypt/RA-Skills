## Description:

Use Scan.now when the user wants a passive security assessment of a website they are authorized to test, or wants to inspect a suspicious public link for phishing signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrick86](https://clawhub.ai/user/henrick86)

### License/Terms of Use:

MIT-0

## Use Case:

External website owners and security practitioners use the skill to request passive checks of sites they are authorized to assess, or to inspect public links for phishing signals and redirects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs are sent to Scan.now and may contain sensitive information.

Mitigation: Use public links without passwords, access tokens, or confidential details, and review the Scan.now MCP privacy policy before sharing sensitive information.

Risk: Assessing a website without permission could exceed authorized scope.

Mitigation: Run website assessments only after the user confirms ownership or explicit permission.

Risk: A clean scan or low phishing score may provide false reassurance.

Mitigation: Treat results as limited signals, not proof of safety; newly reported phishing pages may not yet be listed.

## Reference(s):

- [Scan.now methodology](https://scan.now/methodology)
- [ClawHub skill release](https://clawhub.ai/henrick86/skills/scan-now-tools)
- [Publisher profile](https://clawhub.ai/user/henrick86)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language security assessment findings, phishing indicators, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public URLs and selected scan scope or redirect options; results are informational and do not prove a site is safe.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
