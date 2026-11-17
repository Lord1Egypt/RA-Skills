## Description:

Reads publicly accessible WeChat public account articles and returns the title, account name, publication time, plain-text body, image link markers, and original URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianen](https://clawhub.ai/user/ianen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve text from publicly accessible WeChat public account article URLs for reading, summarization, analysis, or translation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL validation may be bypassed, allowing fetches outside the intended WeChat article host or into internal networks.

Mitigation: Validate that the parsed HTTPS hostname is exactly mp.weixin.qq.com and re-check redirects before trusting the skill in environments with private network access.

Risk: Fetched article pages may fail to parse if WeChat changes page structure or if the article is deleted or requires login.

Mitigation: Treat missing title, account name, publication time, or content as expected failure states and review outputs before downstream summarization or analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ianen/skills/wechat-public-article-reader)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Plain text or JSON containing title, account name, publication time, article content, image link markers, and URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a publicly accessible mp.weixin.qq.com article URL; no API key or cookie is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
