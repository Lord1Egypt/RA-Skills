## Description:

Privacy-respecting metasearch using a configured SearXNG instance for web, image, news, video, and other searches without external API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macdesire](https://clawhub.ai/user/macdesire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route search requests through their own SearXNG instance and retrieve formatted or JSON search results across supported categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad search triggers can route general search prompts to the configured SearXNG instance unexpectedly.

Mitigation: Install only when this routing is intended, and consider narrowing triggers before enabling the skill in shared or sensitive environments.

Risk: Search terms can contain secrets or sensitive regulated data.

Mitigation: Avoid sending secrets or sensitive regulated data as search terms, especially when using shared, remote, or public SearXNG instances.

Risk: Disabled HTTPS certificate verification can make remote or public HTTPS SearXNG instances risky.

Mitigation: Prefer a local or private SearXNG server, or enable TLS verification with a trusted CA bundle before using remote HTTPS instances.

Risk: Runtime dependencies may change because dependency pinning should be reviewed.

Mitigation: Review and pin dependencies before deployment in controlled or production environments.

## Reference(s):

- [SearXNG homepage](https://searxng.org)
- [SearXNG documentation](https://docs.searxng.org/)
- [SearXNG installation guide](https://docs.searxng.org/admin/installation.html)
- [ClawHub skill page](https://clawhub.ai/macdesire/skills/searxng-backup)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown-formatted search results, JSON search payloads, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable SearXNG instance configured through SEARXNG_URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
