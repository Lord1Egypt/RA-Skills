## Description:

Extracts structured data from websites, including tables, lists, prices, articles, and metadata, using HTML parsing with caching and no external dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract structured content from public web pages or supplied HTML, and to monitor public pages for changes when local persistence is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound scraping can make HTTP/HTTPS requests to user-provided URLs, and the server security review reports weaker SSRF protection than advertised.

Mitigation: Use only public, non-sensitive URLs unless the runtime enforces network egress controls that block loopback, private, link-local, and cloud metadata addresses.

Risk: Cache and watch features can store scraped page data on disk.

Mitigation: Avoid cache or watch features for sensitive pages, use no-cache mode for one-time extraction, and clear stored scraper data after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jlacroix82/skills/smart-scraper-web)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Security Audit](artifact/AUDIT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with CLI commands and structured text extraction output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make outbound HTTP/HTTPS requests and may write cache or watch snapshots when those features are used.]

## Skill Version(s):

1.3.7 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
