## Description:

Privacy-respecting metasearch using your local SearXNG instance. Search the web, images, news, and more without external API dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run web, image, news, video, and category searches through a configured SearXNG instance. It is useful when an agent needs metasearch results without relying on a commercial search API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled helper script can create a persistent host-networked SearXNG Docker service and remove an existing container named searxng.

Mitigation: Review or replace run-searxng.sh before use; remove host networking, avoid persistent restart behavior unless intended, pin the container image, bind only to localhost, and require confirmation before replacing an existing container.

Risk: Searches are routed through the configured SearXNG instance, which may expose sensitive queries if the instance is public or untrusted.

Mitigation: Use a local or organization-controlled SearXNG instance and avoid sensitive searches on public instances.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/asterisk622/skills/xiaoding-searxng)
- [SearXNG](https://searxng.org)
- [SearXNG Installation Documentation](https://docs.searxng.org/admin/installation.html)
- [SearXNG Settings Documentation](https://docs.searxng.org/admin/settings/settings.html)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown or terminal-formatted search summaries, with optional JSON search result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable SearXNG instance configured with SEARXNG_URL; direct CLI usage supports category, language, time range, result limit, and JSON output options.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
