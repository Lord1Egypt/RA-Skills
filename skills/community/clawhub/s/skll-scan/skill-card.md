## Description:

Security scanning tool for OpenClaw Skills that detects malicious code patterns, extracts domains, and checks threat intelligence APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niuqun2003](https://clawhub.ai/user/niuqun2003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan OpenClaw Skills before installation, during audits, or before distribution. It helps identify suspicious code patterns, referenced domains, and threat-intelligence signals that need manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner results may be mistaken for installation approval.

Mitigation: Treat results as review input and manually review SKILL.md, install scripts, manifests, and files outside the Python, JavaScript, and TypeScript scan scope before deployment.

Risk: The skill overstates its security coverage for runtime behavior and obfuscated code.

Mitigation: Combine the static scan with manual review, complementary security tools, and deployment controls for critical systems.

Risk: Operational examples include scheduled scanning and third-party threat-intelligence lookups that can create privacy or operational risk.

Mitigation: Run with least privilege, harden and monitor scheduled jobs, and get approval before submitting internal domains or URLs to external threat-intelligence services.

## Reference(s):

- [Threat Intelligence APIs Reference](references/threat-intel-apis.md)
- [Abuse.ch URLhaus](https://urlhaus-api.abuse.ch/)
- [AbuseIPDB API](https://www.abuseipdb.com/api)
- [VirusTotal API](https://www.virustotal.com/api/)
- [AlienVault OTX API](https://otx.alienvault.com/api)
- [Google Safe Browsing API](https://safebrowsing.googleapis.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and text or JSON scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scanner can write a JSON report to /tmp when the script is run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
