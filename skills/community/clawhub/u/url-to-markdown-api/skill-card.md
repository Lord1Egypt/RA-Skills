## Description:

Extracts a public web page into clean Markdown, plain text, or raw HTML using Scavio's URL extraction API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve publicly reachable pages as Markdown or text for summaries, questions, and retrieval workflows, or as HTML for parsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs and extracted page content are sent to Scavio; even a URL alone can disclose sensitive information.

Mitigation: Use only public, non-sensitive pages; avoid private documents, signed URLs, internal systems, and confidential knowledge bases.

## Reference(s):

- [Scavio Extract API documentation](https://scavio.dev/docs/extract?utm_source=agent-skills&utm_medium=skill&utm_campaign=url-to-markdown-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=url-to-markdown-api)
- [ClawHub skill listing](https://clawhub.ai/scavio-ai/skills/url-to-markdown-api)

## Skill Output:

**Output Type(s):** [Markdown, Plain text, HTML]

**Output Format:** [Page content in a JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source URL, extraction mode, content length, and credit usage.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
