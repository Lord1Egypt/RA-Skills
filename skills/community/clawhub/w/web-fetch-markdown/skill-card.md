## Description:

Fetch web pages as reduced markdown via jina.ai for users who want condensed URL content and lower token usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidu](https://clawhub.ai/user/qidu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external agent users use this skill to fetch public web pages through jina.ai and return condensed Markdown when token conservation is important.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send full user-supplied URLs to jina.ai, including private or token-bearing links.

Mitigation: Use it only with public URLs; do not use password reset links, signed download URLs, internal hosts, private documents, authenticated pages, or URLs containing secrets unless the skill adds blocking or confirmation controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qidu/skills/web-fetch-markdown)
- [jina.ai markdown fetch endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown content returned from a fetched public web page, with concise usage guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses jina.ai to extract and reduce page content before returning it to the user]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
