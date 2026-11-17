## Description:

Routes blocked academic sites through the CERNET Scholar reverse-proxy path so agents can access resources such as GitHub, Hugging Face, Docker Hub, Google Scholar, and Wikipedia without a VPN when an education-network route is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[njhxy168](https://clawhub.ai/user/njhxy168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill when direct access to supported academic or developer resources fails from an environment with a working CERNET Scholar route. It provides command-line helpers and proxy configuration guidance for resolving supported hostnames through Scholar and fetching content through that path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reroutes web traffic through a custom proxy path and bundled certificate authority, which can expose sensitive sessions or credentials if used indiscriminately.

Mitigation: Use it only for trusted Scholar proxy traffic, avoid reusable credentials and private access tokens, keep the proxy bound to 127.0.0.1, and stop it after use.

Risk: The artifact documents TLS-bypass flags that reduce HTTPS protections.

Mitigation: Prefer the bundled Scholar CA path over TLS-disable flags, and avoid disabling certificate verification unless a reviewer has accepted that risk for a specific session.

Risk: Some domains are not supported by the Scholar DoH path and may fail or fall back to direct network access.

Mitigation: Resolve target hostnames first, use the proxy only for supported 205.164.50.x mappings, and connect directly when the target is already reachable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/njhxy168/skills/scholar-access)
- [Scholar DNS-over-HTTPS endpoint](https://doh.scholar.work/dns-query)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also help produce downloaded files when the curl wrapper is used.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
