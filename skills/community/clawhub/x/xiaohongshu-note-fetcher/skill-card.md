## Description:

Fetches and organizes Xiaohongshu note page and search-result information into structured JSON, Markdown, CSV, and topic-planning materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2813223285](https://clawhub.ai/user/2813223285)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, and developers use this skill to collect public or authorized Xiaohongshu note metadata, search results, engagement signals, and planning exports from note URLs, keyword searches, TikHub API responses, or browser-assisted scraping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for cookies or API tokens and can send them to Xiaohongshu, TikHub, or a user-configured generic API endpoint.

Mitigation: Use only tokens and cookies suitable for the exact destination being called, avoid raw cookie files where possible, and do not point the generic API adapter at untrusted endpoints.

Risk: Scraping and broad network requests may collect or expose content outside the user's intended authorization boundary.

Mitigation: Use the skill only for Xiaohongshu URLs and data the user is authorized to access, respect platform terms and privacy requirements, and avoid bypassing platform safety mechanisms.

Risk: Generated CSV, Markdown, JSON, and templates can contain untrusted third-party-derived content.

Mitigation: Review generated files before opening them in spreadsheet software, publishing them, or reusing them in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2813223285/skills/xiaohongshu-note-fetcher)
- [Output Schema](references/output-schema.md)
- [TikHub Xiaohongshu search API endpoint](https://api.tikhub.io/api/v1/xiaohongshu/web/search_notes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands, plus generated JSON, Markdown, CSV, and text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured note records include URL, note ID, title, description, author, publication time, images, tags, interaction counts, fetch timestamp, and source status when available.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact publishing notes and package metadata list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
