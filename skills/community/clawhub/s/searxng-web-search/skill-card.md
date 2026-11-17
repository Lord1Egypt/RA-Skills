## Description:

Search the web using a self-hosted SearXNG metasearch engine when an agent needs online information, recent news, topic research, or other current internet context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangtao](https://clawhub.ai/user/gangtao)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent users use this skill to give agents structured web search through a self-hosted SearXNG instance, including general web, news, image, IT, and science searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup examples can expose a persistent SearXNG service with weak secrets or unpinned dependencies.

Mitigation: Bind SearXNG to 127.0.0.1, avoid exposing port 8080 to untrusted networks, generate a unique secret key, and pin Docker images and dependencies.

Risk: Search queries may contain private or sensitive information that is sent to the configured SearXNG service and upstream engines.

Mitigation: Avoid sending secrets or private data as search queries and place shared instances behind authenticated access with rate limiting.

## Reference(s):

- [SearXNG Reference Guide](references/REFERENCE.md)
- [SearXNG Documentation](https://docs.searxng.org/)
- [Agent Skills Specification](https://agentskills.io/specification)
- [ClawHub Skill Page](https://clawhub.ai/gangtao/skills/searxng-web-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON search results or human-readable text, with Markdown documentation and shell/configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python requests, network access to a SearXNG endpoint, and JSON API enabled in SearXNG settings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
