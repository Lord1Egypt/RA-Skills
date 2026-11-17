## Description:

Search using a custom SearXNG instance via HTTP API. Enables privacy-friendly web search by aggregating results from multiple search engines. Supports query, format (json/csv/rss), language, time range, categories, engines, pagination, and safe search filtering. Requires a user-provided or configured SearXNG instance URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyijun](https://clawhub.ai/user/cyijun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run web searches through a configured SearXNG instance, narrow searches by language, time range, category, engine, safe-search level, and page number, then present returned results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the configured SearXNG instance, which may expose sensitive investigative terms to that server.

Mitigation: Use a trusted HTTPS or self-hosted SearXNG instance and avoid submitting secrets, private project names, or sensitive search terms to public instances.

Risk: Some public SearXNG instances disable JSON, CSV, or RSS output or enforce rate limits.

Mitigation: Confirm the instance supports the required output format before relying on it, and space repeated requests to respect server limits.

## Reference(s):

- [SearXNG Engines and Categories Reference](references/engines_and_categories.md)
- [ClawHub Skill Page](https://clawhub.ai/cyijun/skills/web-search-by-searxng)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and formatted search results or JSON text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output depends on the configured SearXNG instance, enabled result formats, selected engines, and rate limits.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
