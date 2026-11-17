## Description:

Fetches web pages from specific URLs and converts them to clean, structured Markdown via trusted APIs, enabling Agents to parse and extract data more effectively.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuruofan](https://clawhub.ai/user/wuruofan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to fetch public web pages and convert them into cleaner Markdown so agents can parse, summarize, and extract information more effectively.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full URLs may be sent to third-party conversion services, including URL paths that contain private tokens, reset links, pre-signed URLs, internal resource names, or user identifiers.

Mitigation: Avoid private, internal, tokenized, reset, or pre-signed URLs, and ask the user before sending any URL to an external conversion service.

Risk: Fallback behavior could route around a platform domain-safety warning through another conversion service.

Mitigation: Do not use a proxy-style fallback to bypass platform safety warnings; stop or request safer user-provided content when a URL is blocked.

Risk: The security verdict is suspicious because the skill can automatically send full user URLs to external services.

Mitigation: Review the skill carefully before installation and limit use to public web pages where exposing the URL to the conversion provider is acceptable.

## Reference(s):

- [Web Fetch as Markdown on ClawHub](https://clawhub.ai/wuruofan/skills/web-fetch-as-markdown)
- [Cloudflare markdown.new conversion service](https://markdown.new/)
- [Jina AI Reader endpoint](https://r.jina.ai/)
- [Markdown For Agents fallback endpoint](https://markdownforagents.com/r)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown converted from web page content with brief service or limitation messages when fetching cannot proceed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The converted content is intended to remove ads, navigation, and clutter when the external conversion service succeeds.]

## Skill Version(s):

1.2.1 (source: release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
