## Description:

Monitor SSL certificates for expiration, security issues, and compliance across domains and subdomains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to check SSL/TLS certificate expiration, retrieve certificate metadata, and run basic batch monitoring across domains and subdomains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a complete TLS security validation or compliance tool.

Mitigation: Use it only for certificate retrieval, metadata, and expiration monitoring unless hostname and trust-chain validation are independently fixed and verified.

Risk: Certificate checks require outbound network access to target domains and may fail because of DNS, firewall, timeout, or rate-limit conditions.

Mitigation: Run checks from an approved network location, review failed targets manually, and avoid treating connection failures as proof of certificate status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/derick001/skills/ssl-certificate-monitor)
- [Publisher profile](https://clawhub.ai/user/derick001)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce human-readable certificate status, certificate metadata, batch summaries, and JSON output for automation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
