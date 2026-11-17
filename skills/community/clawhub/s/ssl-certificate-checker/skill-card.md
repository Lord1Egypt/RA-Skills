## Description:

Check SSL/TLS certificate details including expiration date, issuer, validity, cipher suites, and security warnings for any domain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardodpanda](https://clawhub.ai/user/leonardodpanda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to check public SSL/TLS certificate expiration, issuer, validity, cipher suite details, and HTTPS configuration warnings for domains they are responsible for monitoring or troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain names supplied to shell commands can be unsafe if copied from untrusted input.

Mitigation: Validate domains as DNS names or IP addresses before using them in OpenSSL commands.

Risk: OpenSSL checks contact the specified host and may reveal that a domain was queried from the user's environment.

Mitigation: Run checks only against domains the user is authorized to inspect and avoid sensitive internal certificates unless dedicated internal tooling is approved.

## Reference(s):

- [SSL Certificate Checker on ClawHub](https://clawhub.ai/leonardodpanda/skills/ssl-certificate-checker)
- [leonardodpanda ClawHub profile](https://clawhub.ai/user/leonardodpanda)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenSSL command examples and concise interpretation of certificate details.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
