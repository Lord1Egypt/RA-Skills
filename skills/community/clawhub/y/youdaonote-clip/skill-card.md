## Description:

Saves clipped web pages, including supported dynamic pages and Twitter/X posts, into Youdao Cloud Notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lephix](https://clawhub.ai/user/lephix)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to capture web page content, images, and source URLs into Youdao Cloud Notes from supported Chinese content sites, Twitter/X posts, and general browser-accessible pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload clipped page text, image data, source URLs, and possibly AI-chat transcripts through broad network and credential paths.

Mitigation: Use it only with trusted pages and trusted Youdao MCP configuration, and avoid sensitive internal pages unless endpoint validation and image fetching safeguards are tightened.

Risk: Custom MCP endpoints or untrusted clipping targets may route private content or credentials outside the intended service path.

Mitigation: Avoid custom MCP URLs unless they are known HTTPS endpoints and review the configured environment variables before installation.

## Reference(s):

- [YoudaoNote Clip ClawHub listing](https://clawhub.ai/lephix/skills/youdaonote-clip)
- [Marked Markdown parser](https://github.com/markedjs/marked)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API calls, Files]

**Output Format:** [Markdown confirmation table, command-line JSON metadata, and remote note content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YOUDAONOTE_API_KEY and local tools listed by the release metadata; execution can create temporary clipping data under /tmp.]

## Skill Version(s):

1.21.8 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
