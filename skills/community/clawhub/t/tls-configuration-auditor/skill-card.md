## Description:

Audit TLS/SSL configuration of servers and applications, including protocol versions, cipher suites, certificate chain validity, HSTS headers, and alignment with PCI-DSS, NIST, and Mozilla recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and operations teams use this skill to audit HTTPS endpoints for TLS protocol support, certificate health, cipher strength, security headers, and compliance-oriented findings before assessments or remediation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TLS probes run network checks against the host supplied by the user; an incorrect or unauthorized HOST value could test the wrong system.

Mitigation: Use the skill only on systems you own or are authorized to test, and validate the HOST value before running commands.

Risk: Generated command snippets and audit findings may be treated as authoritative compliance evidence without review.

Mitigation: Review shell snippets before execution and treat generated findings as a starting point for security or compliance validation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and audit report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces host-specific TLS audit findings, recommendations, and optional monitoring script or CI job guidance.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
