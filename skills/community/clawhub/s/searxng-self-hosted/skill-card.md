## Description:

Search the web using a self-hosted SearXNG instance with privacy-respecting metasearch that aggregates results from multiple engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clockworksquirrel](https://clawhub.ai/user/clockworksquirrel)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to query a self-hosted SearXNG service, retrieve JSON search results, and work with categorized, language-specific, or paginated web search output from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance can expose an unauthenticated persistent SearXNG search service.

Mitigation: Bind the service to localhost or a private network before use.

Risk: The sample configuration uses a placeholder secret key.

Mitigation: Replace the placeholder with a random secret before operating the service.

Risk: Search queries can disclose secrets, sensitive project names, or private intent to configured search engines.

Mitigation: Avoid putting secrets or sensitive project details in searches.

Risk: The Docker setup references a mutable container image tag.

Mitigation: Pin the SearXNG container image to a reviewed version or digest for long-term use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clockworksquirrel/skills/searxng-self-hosted)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and JSON response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include title, URL, content snippet, engines, score, and category when returned by the configured SearXNG JSON endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
