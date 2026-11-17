## Description:

Web Intel provides a unified entry point for web search and information extraction, routing requests across content-extraction handlers, Jina Reader, Firecrawl, and a local web-access CDP proxy based on task needs and mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to search the web, extract page content, and route finance, news, competitor-research, and direct-URL tasks to the appropriate retrieval path. It is intended as a reusable web intelligence layer for other skills and sub-agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deep mode can use a logged-in Chrome session through the local CDP proxy to read arbitrary page text.

Mitigation: Avoid deep mode on private accounts, internal dashboards, localhost services, or URLs containing tokens unless explicit confirmation and destination allowlists are added.

Risk: Requests may route URLs or queries to third-party extraction and search services.

Mitigation: Review URLs before use and avoid sending confidential, access-controlled, or token-bearing content to external retrieval services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halfmoon82/skills/web-intel)
- [Jina Reader endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON stdout for tool results, with Markdown and shell-command guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result payloads include query or URL, mode, task type, selected tool, result snippets or extracted content, web_access availability, latency, and optional notes; extracted content is truncated by mode.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
