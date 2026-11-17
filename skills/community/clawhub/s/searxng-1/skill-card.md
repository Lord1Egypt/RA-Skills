## Description:

Privacy-respecting metasearch using your local SearXNG instance. Search the web, images, news, and more without external API dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phucanh08](https://clawhub.ai/user/phucanh08)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and engineers use this skill to query a configured SearXNG instance for web, image, video, news, map, music, file, IT, and science search results without relying on commercial search APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to a configured SearXNG endpoint and could contain sensitive information.

Mitigation: Use only a SearXNG endpoint you control or trust, preferably localhost, and avoid sending sensitive queries through public instances.

Risk: TLS verification is disabled by default to support self-signed local certificates.

Mitigation: Use localhost or a trusted network, and change the request configuration to secure-by-default TLS verification when connecting to HTTPS endpoints that support it.

Risk: Broad search-like triggers may cause the skill to run for more prompts than intended.

Mitigation: Review prompts before execution and narrow trigger terms in future releases where possible.

Risk: Dependencies are declared without version pins or a lock file.

Mitigation: Pin dependencies or provide a lock file before deployment in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phucanh08/skills/searxng-1)
- [SearXNG Project](https://searxng.org)
- [SearXNG Installation Guide](https://docs.searxng.org/admin/installation.html)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Console text or JSON search results with markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured SEARXNG_URL endpoint and Python 3.11 or newer with httpx and rich.]

## Skill Version(s):

1.0.1 (source: server release evidence, frontmatter, and changelog released 2026-01-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
