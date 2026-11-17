## Description:

Generate valid RSS 2.0 or Atom 1.0 feeds from public post-list pages without native feeds, producing well-formed feed XML and an optional self-hostable HTML discovery wrapper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kidehen](https://clawhub.ai/user/kidehen)

### License/Terms of Use:

MIT

## Use Case:

Developers, publishers, and automation users use this skill to create synthetic RSS or Atom feeds from publicly accessible blog, news, or post-list pages that do not expose a native feed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching pages through broad third-party, authenticated, or shell-based routes can expose private URLs, credentials, API keys, cookies, or intranet targets.

Mitigation: Use only public pages; do not provide private or signed URLs, cookies, Authorization headers, API keys, or intranet targets.

Risk: Authenticated LLM-mediated routes and direct shell fetching may be inappropriate outside controlled environments.

Mitigation: Prefer public page-fetching routes and avoid shell or authenticated LLM routes unless the execution environment is controlled and reviewed.

Risk: Generated HTML can carry unsafe scraped content if it is hosted without escaping or sanitization.

Mitigation: Escape or sanitize generated HTML before hosting and validate generated feeds before publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kidehen/skills/rss-generator-skill)
- [URIBurner WEB_FETCH OpenAPI Definition](https://linkeddata.uriburner.com/chat/functions/openapi.yaml)
- [Protocol Routing](references/protocol-routing.md)
- [Post Extraction Rules](references/extraction-rules.md)
- [Feed Templates](references/feed-templates.md)
- [HTML Feed Discovery Wrapper Template](references/html-wrapper-template.md)
- [Feed Validation Checklist](references/validation-checklist.md)
- [W3C Feed Validator](https://validator.w3.org/feed/)
- [RSS Board Validator](https://www.rssboard.org/rss-validator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with XML, HTML, and shell command code blocks; generated feed XML and optional HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output saves a feed XML file; optional modes can return raw XML, an HTML discovery wrapper, or both.]

## Skill Version(s):

1.0.0 (source: release metadata and skill heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
