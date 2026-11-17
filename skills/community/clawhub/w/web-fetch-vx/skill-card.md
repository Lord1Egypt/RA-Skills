## Description:

Extracts clean article content and metadata from WeChat, news, and blog webpages, with Markdown, JSON, plain-text, and batch-processing support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3511815125](https://clawhub.ai/user/3511815125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-processing agents use this skill to extract readable text and article metadata from public WeChat articles, news pages, and blog posts for summarization, archival, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied URLs may cause private, internal, login-protected, or token-bearing destinations to be fetched through extraction tools or related services.

Mitigation: Use the skill only for intended public webpage extraction, and avoid private links, internal network URLs, login-protected pages, and URLs containing tokens unless that exposure is explicitly approved.

Risk: Webpage extraction can conflict with publisher access controls, rate limits, or attribution expectations.

Mitigation: Restrict use to public and authorized content, respect robots.txt and documented rate limits, and preserve source attribution when retaining extracted content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3511815125/skills/web-fetch-vx)
- [OpenClaw Web Content Extractor documentation](https://docs.openclaw.ai/skills/web-content-extractor)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Metadata, Guidance]

**Output Format:** [Markdown, JSON, or plain text extracted from webpages, optionally including title, author, date, word count, read time, images, and extraction timing metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-URL and batch extraction flows with options for output mode, maximum characters, metadata inclusion, timeout, user agent, proxy, and cache behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
