## Description:

Search the web using a self-hosted SearXNG instance with a privacy-respecting metasearch interface that aggregates results from multiple engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clockworksquirrel](https://clawhub.ai/user/clockworksquirrel)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure and query a self-hosted SearXNG instance for web, image, news, video, technical, and science search results through JSON responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example setup can expose a persistent unauthenticated SearXNG service on the network.

Mitigation: Review before installing on untrusted or internet-reachable machines; prefer binding Docker to 127.0.0.1 and add TLS, authentication, firewalling, and rate limits before remote access.

Risk: The example configuration includes a placeholder secret and an unpinned container image.

Mitigation: Generate a real random secret and pin the SearXNG container image before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clockworksquirrel/skills/searxng-local)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the optional SEARXNG_URL environment variable and returns SearXNG result fields such as title, url, content, engines, score, and category.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
