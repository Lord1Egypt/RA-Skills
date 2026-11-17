## Description:

Comprehensive website audit combining uptime checking, TLS certificate inspection, and security headers grading in one command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and security reviewers use Siteaudit to check websites they own or are authorized to test for uptime, HTTPS/TLS status, certificate expiry, and common security header gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes disclosed network checks against user-provided websites, and audited servers can observe those connections.

Mitigation: Use it only for websites you own or are authorized to test; avoid private, internal, or third-party hosts without permission.

Risk: The output is a lightweight website health and header audit, not a complete security assessment.

Mitigation: Treat findings as triage signals and review important issues with appropriate operational or security tooling before acting.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Plain text report or JSON object from the Siteaudit Python CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 0 when all checked sites are healthy; exit code 1 when issues are detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
