## Description:

Fetch complete content from WeChat public account articles (mp.weixin.qq.com). Use when extracting content from WeChat official account links, especially when default web fetch gets incomplete content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ranhuang](https://clawhub.ai/user/ranhuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch public WeChat official account articles and convert extracted article content into Markdown when standard web fetching returns incomplete content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetch script can request arbitrary HTTP or HTTPS URLs rather than only WeChat article URLs.

Mitigation: Run the skill in a sandbox with restricted network egress, or modify it to allow only mp.weixin.qq.com and to validate redirects before deployment.

Risk: Unpinned Python dependencies can change behavior between installs.

Mitigation: Pin and review httpx, readability-lxml, and lxml versions for reproducible installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ranhuang/skills/ye-weixin-web-fetch)
- [Publisher profile](https://clawhub.ai/user/ranhuang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [JSON containing article metadata and Markdown content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content may be truncated to the configured maximum character limit.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
