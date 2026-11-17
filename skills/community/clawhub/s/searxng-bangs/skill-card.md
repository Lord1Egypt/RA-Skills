## Description:

Privacy-respecting web search via SearXNG with DuckDuckGo-style bangs support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rpeters511](https://clawhub.ai/user/rpeters511)

### License/Terms of Use:

CC0

## Use Case:

Developers, engineers, and agent users use this skill to run web, news, image, video, and science searches through a SearXNG instance, including direct engine searches with DuckDuckGo-style bangs. It is most useful when a self-hosted or trusted SearXNG endpoint is available and the agent needs JSON search results without API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive queries can be sent to public SearXNG instances or to plaintext endpoints if configured that way.

Mitigation: Prefer a self-hosted SearXNG instance, require HTTPS for non-local endpoints, and avoid public instances for confidential searches.

Risk: Privacy claims depend on the SearXNG endpoint and deployment configuration rather than the skill alone.

Mitigation: Review endpoint ownership and configuration before use, and pin the SearXNG container image to a reviewed digest or version.

## Reference(s):

- [SearXNG API Reference](references/api.md)
- [SearXNG installation documentation](https://docs.searxng.org/admin/installation.html)
- [SearXNG public instance directory](https://searx.space)
- [DuckDuckGo bang shortcuts](https://duckduckgo.com/bang)
- [ClawHub skill page](https://clawhub.ai/rpeters511/skills/searxng-bangs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON search results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include query, number_of_results, and result objects with title, url, and content fields; errors are returned as JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
