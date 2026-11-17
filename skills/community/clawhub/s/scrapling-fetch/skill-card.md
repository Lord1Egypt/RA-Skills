## Description:

Scrapling Fetch helps agents retrieve webpage content, including pages protected by common anti-bot checks, and return cleaned JSON, Markdown, or plain text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imgolye](https://clawhub.ai/user/imgolye)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to fetch article or webpage content from WeChat Official Accounts, Medium, Substack, Cloudflare-protected pages, and ordinary web pages for research, summarization, and content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted URL could cause unsafe Python execution in the fetch path.

Mitigation: Pass the URL as a safe subprocess argument, validate and escape URL input, and avoid interpolating user input into python -c code.

Risk: The paid fetch script includes live-format billing behavior and a hardcoded SkillPay API key.

Mitigation: Remove the embedded key, rotate the exposed credential, load credentials from user-controlled secret storage, and require explicit billing consent before any charge.

Risk: Fetching private, tokenized, internal, or sensitive URLs could expose confidential content or enable internal network access.

Mitigation: Block internal network targets and avoid using the skill on sensitive URLs unless the publisher adds clear allowlists and data-handling controls.

Risk: Fast mode sends target URLs through a third-party reader service.

Mitigation: Make third-party proxying opt-in and disclose the data path before sending URLs to external services.

## Reference(s):

- [Known anti-bot site guidance](references/antibot-sites.md)
- [Scrapling project](https://github.com/D4Vinci/Scrapling)
- [Jina Reader](https://jina.ai/reader)
- [Scrapling Fetch on ClawHub](https://clawhub.ai/imgolye/skills/scrapling-fetch)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON by default, plain text with --text, and Markdown content in extracted page fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content length is bounded by --max-chars; the default maximum is 50000 characters.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
