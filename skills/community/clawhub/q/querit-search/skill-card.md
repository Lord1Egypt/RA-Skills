## Description:

Web search via Querit.ai API for documentation, current events, facts, and web content, returning structured results with titles, URLs, snippets, and optional extracted page content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[interskh](https://clawhub.ai/user/interskh)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to search the web from OpenClaw, filter results by language, country, date, and domain, and optionally extract readable page content as markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer supports a one-line curl-to-bash path that downloads and executes files from a remote source.

Mitigation: Review and pin the source before installation, prefer a versioned release with hashes, and avoid the one-line installer for unattended environments.

Risk: Search queries and fetched URLs are sent to external services or websites.

Mitigation: Do not submit confidential queries, internal URLs, or sensitive page targets through the skill.

Risk: The page content fetcher can request arbitrary URLs.

Mitigation: Restrict use to public, non-sensitive URLs and avoid internal network or private-resource targets.

## Reference(s):

- [Querit Search on ClawHub](https://clawhub.ai/interskh/skills/querit-search)
- [Querit.ai](https://querit.ai)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Plain-text search results, extracted Markdown content, or raw JSON arrays.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QUERIT_API_KEY for search. Queries are limited to 72 characters, search results are limited to 100 per query, and content extraction fetches the supplied URL directly.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
