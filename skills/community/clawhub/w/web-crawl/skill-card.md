## Description:

Advanced web crawling and content extraction tool with multiple extraction modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nowhitestar](https://clawhub.ai/user/nowhitestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to crawl single or multiple web pages, extract text, Markdown, links, or structured JSON, and prepare source material for web research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs, including internal network targets.

Mitigation: Run it only where unrestricted outbound crawling is acceptable and block localhost, private IP ranges, cloud metadata addresses, unusual ports, and redirects to prohibited destinations.

Risk: Parallel or research-driven crawling can contact multiple untrusted URLs automatically.

Mitigation: Require explicit user confirmation before parallel crawls or research workflows against untrusted URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nowhitestar/skills/web-crawl)
- [README](artifact/README.md)
- [Usage examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Links, Shell commands, Guidance]

**Output Format:** [Plain text, Markdown, JSON, and research guidance with inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports extraction modes text, markdown, links, structured, and full; content may be truncated by max_length.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
