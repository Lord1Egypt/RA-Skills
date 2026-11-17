## Description:

Query TrendAI Vision One threat intelligence for IOC lookup, threat feed review, intelligence reports, suspicious object management, and threat hunting by industry, campaign, actor, or CVE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andresark](https://clawhub.ai/user/andresark)

### License/Terms of Use:

MIT

## Use Case:

Security analysts, incident responders, and security automation developers use this skill to query TrendAI Vision One threat intelligence, inspect IOC context, review reports, and manage suspicious objects from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A high-privilege Vision One API key could allow an agent workflow to change suspicious-object blocking or logging state.

Mitigation: Use the least-privileged API key that supports the intended workflow, preferably View-only for read operations and a separate Configure-capable key only for intentional suspicious-object additions.

Risk: Suspicious-object additions can affect security controls for domains, URLs, IP addresses, hashes, or email senders.

Mitigation: Require user confirmation before write operations and review the indicator, action, risk level, description, and expiry before execution.

Risk: The security scan notes that redirect destinations are not checked by the HTTP client.

Mitigation: Avoid high-privilege tokens until redirect validation is reviewed or remediated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andresark/skills/vision-one-threat-intel)
- [Publisher Profile](https://clawhub.ai/user/andresark)
- [Project Homepage](https://github.com/andresark/agentic-threat-intel)
- [TrendAI Vision One](https://www.trendmicro.com/en_us/business/products/one-platform.html)
- [TrendAI Vision One Threat Intelligence API Reference](references/api-reference.md)
- [OData Filter Examples for Vision One Threat Intelligence](references/filter-examples.md)
- [Response Schemas](references/response-schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured plain text with command examples and key-value sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Vision One API key and optional region setting; GET workflows are read-only, while suspicious object additions modify blocking or logging state.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
