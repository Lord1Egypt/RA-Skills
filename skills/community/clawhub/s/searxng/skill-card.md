## Description:

Privacy-respecting metasearch using your local SearXNG instance. Search the web, images, news, and more without external API dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abk234](https://clawhub.ai/user/abk234)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent search a configured SearXNG instance for web, image, news, video, and other category results without commercial search API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the configured SearXNG server, which can expose sensitive search terms if the server is remote, public, or not controlled by the user.

Mitigation: Prefer a localhost or otherwise trusted SearXNG instance, and avoid sending sensitive terms to public instances.

Risk: TLS certificate verification is disabled by default to support local self-signed certificates.

Mitigation: Enable certificate verification or trust a specific local CA before using a remote HTTPS SearXNG instance.

Risk: Generic search triggers may cause the skill to run for broad lookup requests.

Mitigation: Review the configured endpoint and search terms before use when requests may contain private or regulated information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abk234/skills/searxng)
- [ClawHub publisher profile](https://clawhub.ai/user/abk234)
- [SearXNG homepage](https://searxng.org)
- [SearXNG documentation](https://docs.searxng.org/)
- [SearXNG installation guide](https://docs.searxng.org/admin/installation.html)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown search result tables or JSON search result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output varies by query, result limit, category, language, time range, and SEARXNG_URL configuration.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
