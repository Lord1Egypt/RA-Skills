## Description:

Search the web using SearXNG and return ranked results with titles, URLs, and content snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noblepayne](https://clawhub.ai/user/noblepayne)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve current web results, documentation, news, and fact-checking material from a configured SearXNG instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the configured SearXNG instance and may expose sensitive text to that service.

Mitigation: Use only a trusted SearXNG instance, prefer HTTPS for non-local endpoints, and avoid searching for secrets or highly sensitive content.

Risk: The artifact references scripts/search.clj, but the server security guidance notes that the script is missing from the package.

Mitigation: Verify the search script is present and executable before deployment, or supply the missing script from a trusted source.

Risk: Search behavior depends on the availability, configuration, and rate limits of the configured SearXNG instance.

Mitigation: Operate or select a reliable SearXNG instance and handle empty results, timeouts, and rate-limit responses during use.

## Reference(s):

- [SearXNG API Reference](references/api-guide.md)
- [SearXNG Documentation](https://docs.searxng.org/)
- [ClawHub Skill Page](https://clawhub.ai/noblepayne/skills/searxng-local-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Formatted text search results with titles, URLs, snippets, scores, and engine names.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are ranked and may be filtered by category, time range, language, and result count.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
