## Description:

Reads WeChat Official Account article links, extracts article metadata and content, and returns a concise summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shianaixuexi-cell](https://clawhub.ai/user/shianaixuexi-cell)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and workspace operators use this skill to process mp.weixin.qq.com article links and receive the article title, author, account, publish time, extracted content, and summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network fetching could reach unintended web services if redirects, host validation, response size, or retry behavior are not constrained.

Mitigation: Strictly validate HTTPS mp.weixin.qq.com hosts, disable or revalidate redirects, and bound response sizes and retry settings before use in environments with internal network access.

Risk: Sensitive article links and extracted content may be processed by the skill and the surrounding summarization flow.

Mitigation: Avoid sensitive or private article links unless the deployment owner has reviewed and accepted the data handling path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shianaixuexi-cell/skills/wechat-article-reader-0)
- [Publisher profile](https://clawhub.ai/user/shianaixuexi-cell)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Structured text with article metadata, a summary, and optional JSON data from the handler.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network access is required to fetch supported WeChat article pages.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
