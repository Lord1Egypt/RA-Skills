## Description:

Scan WordPress sites for security vulnerabilities, misconfigurations, and potential threats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

WordPress site owners, security professionals, penetration testers, and hosting providers use this skill to request security scans of public WordPress installations and receive categorized findings with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger scans of public WordPress sites without clear authorization safeguards.

Mitigation: Use it only for WordPress sites you own or have explicit permission to test.

Risk: Invoking the scanner sends the target URL to a third-party hosted API and may generate security probe traffic against that site.

Mitigation: Review the provider, pricing, rate limits, and operational approval path before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/wordpress-security-scanner)
- [WordPress Security Scanner API Docs](https://api.mkkpro.com:8031/docs)
- [WordPress Security Scanner API Route](https://api.mkkpro.com/security/wordpress-security-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown and JSON-oriented API request/response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scan requests and interprets categorized security findings with remediation guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
