## Description:

Inspect and troubleshoot Traefik reverse proxies via read-only API, dashboard, logs, and config checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naamah75](https://clawhub.ai/user/naamah75)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose Traefik routing, service, middleware, TLS, log, and dynamic configuration issues. It supports read-oriented inspection through Traefik and Mantrae APIs and guides cautious handling of sensitive dumps, credentials, and configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated Mantrae API access can exceed the skill's read-only troubleshooting description.

Mitigation: Use narrowly scoped read-only Traefik and Mantrae credentials, restrict available Mantrae methods to read-oriented endpoints, and require explicit human approval before create, update, delete, restore, or arbitrary RPC calls.

Risk: Disabling TLS verification or using plaintext non-loopback URLs can expose infrastructure data or credentials.

Mitigation: Prefer HTTPS with certificate verification, avoid --insecure except for controlled diagnostics, and keep plaintext URLs limited to loopback or trusted internal networks.

Risk: Traefik raw data, support dumps, and access logs can include sensitive routing details, configuration, or identity-provider query strings.

Mitigation: Summarize findings, redact secrets and long authentication-related query strings, and share raw dumps only when explicitly needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/naamah75/skills/traefik-mantrae-diagnostics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize JSON API responses and log excerpts; sensitive routing details, support dumps, credentials, and long OIDC query strings should be minimized.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
