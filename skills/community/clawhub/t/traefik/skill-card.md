## Description:

Avoid common Traefik mistakes in router priority, TLS configuration, Docker label syntax, and middleware ordering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and platform engineers use this skill as quick operational guidance for configuring Traefik routers, Docker labels, TLS, entrypoints, middleware, services, file providers, and debugging settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational Traefik snippets can affect dashboard exposure, TLS behavior, certificate issuance, and authentication.

Mitigation: Review and adapt dashboard exposure, TLS, ACME, and BasicAuth settings for the deployment before applying them.

Risk: Incorrect routing, middleware ordering, or Docker label syntax can cause outages or misrouted traffic.

Mitigation: Validate configuration in a staging environment and review router priorities, entrypoints, services, and middleware order before production use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with inline configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No hidden execution, persistence, or data access behavior reported by security evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
