## Description:

读取微信公众平台文章内容（mp.weixin.qq.com）。当用户发送微信文章链接、需要读取微信文章内容、提取公众号文章时自动激活。支持突破微信反爬限制，获取完整文章文本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lcwatergm-afk](https://clawhub.ai/user/lcwatergm-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to fetch readable text from WeChat public-platform article links for summarization, extraction, and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted URL could cause unintended shell command execution in the helper script.

Mitigation: Validate HTTPS mp.weixin.qq.com URLs and avoid shell=True when fetching article pages.

Risk: The helper could contact non-WeChat network targets through user-supplied or redirected URLs.

Mitigation: Reject off-domain redirects and enforce the expected WeChat host before network access.

Risk: Some WeChat articles may be inaccessible or incomplete because of permissions or anti-crawling controls.

Mitigation: Ask the user to confirm extracted content before using it for downstream analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lcwatergm-afk/skills/weixin-article-read)
- [Example WeChat article URL from skill documentation](https://mp.weixin.qq.com/s/kItlJmjOnq6p6tXtYGHrGQ)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style article text or plain text printed by a helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one WeChat article URL and returns extracted article content when accessible.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
