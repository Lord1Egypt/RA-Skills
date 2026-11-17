## Description:

Fetches public web pages by converting URLs into readable text or Markdown through URL-to-Markdown services, with a Scrapling fallback when those services fail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larriewong27](https://clawhub.ai/user/larriewong27)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill when they need to retrieve public web content from search pages, articles, or documentation links as readable text or Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full URLs may be sent to third-party URL conversion services, exposing tokens, credentials, private document links, internal hosts, or signed URLs.

Mitigation: Use the skill only with public pages and exclude password-reset links, signed download URLs, private documents, internal hosts, localhost, cloud metadata endpoints, and URLs containing tokens or credentials.

Risk: The Scrapling fallback suggests installing an unpinned package.

Mitigation: Require approval and a sandbox before installing Scrapling, and prefer pinned, reviewed dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/larriewong27/skills/zt-web-fetcher)
- [markdown.new](https://markdown.new/)
- [r.jina.ai](https://r.jina.ai/)
- [defuddle.md](https://defuddle.md/)
- [Scrapling](https://github.com/D4Vinci/Scrapling)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with URL patterns and inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied public URL; output quality depends on the target page and selected conversion service.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
