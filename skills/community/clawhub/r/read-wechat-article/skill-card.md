## Description:

Fetches user-provided WeChat Official Account article URLs and extracts cleaned article content, metadata, images, word count, and reading time.

This skill is for research and development only.

## Publisher:

[psyear](https://clawhub.ai/user/psyear)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to retrieve and normalize a user-supplied WeChat article into structured content for reading, summarization, archiving, or downstream text processing. Its documentation limits use to user-initiated, non-bulk, non-commercial, platform-compliant workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched article content can be intercepted or tampered with because HTTPS certificate verification is disabled.

Mitigation: Restore normal HTTPS certificate verification before using returned content in trusted workflows.

Risk: Redirects or fetched article text may be untrusted and could mislead downstream agents or users.

Mitigation: Validate redirects, preserve source attribution, and treat extracted article text as untrusted input.

Risk: Bulk or high-frequency fetching may violate platform rules or trigger access controls.

Mitigation: Keep use user-initiated, avoid bulk scraping, and apply conservative rate limits.

Risk: Dependency ranges are not pinned, which may reduce reproducibility across installations.

Mitigation: Pin and review dependency versions for production or trusted workflow deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psyear/skills/read-wechat-article)
- [Publisher profile](https://clawhub.ai/user/psyear)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON object containing article metadata, Markdown content, plain text content, image URLs, word count, and reading time; error responses include a success flag and message.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided WeChat article URL and performs network fetching with retry behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, setup.py, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
