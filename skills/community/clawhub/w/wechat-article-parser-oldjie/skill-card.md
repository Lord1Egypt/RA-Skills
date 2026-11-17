## Description:

Parses WeChat Official Account article links and helps an agent extract key points, context, details, source links, and caveats without inventing unsupported content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oldjie](https://clawhub.ai/user/oldjie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent fetch and summarize WeChat Official Account articles while preserving important context, examples, data, links, prices, and author concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs browser automation against user-provided WeChat article URLs, and server security evidence flags URL handling and installation guidance as broader than users should accept without review.

Mitigation: Review before installing or executing, run only on trusted WeChat article URLs, and avoid automatic execution from arbitrary chat messages.

Risk: Dependency installation and URL handling may be less controlled than desired for routine use.

Mitigation: Use a fixed install that pins playwright and cheerio; publishers should replace substring URL checks with strict URL parsing and block redirects or subresources outside mp.weixin.qq.com.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oldjie/skills/wechat-article-parser-oldjie)
- [Node.js](https://nodejs.org)
- [Playwright](https://playwright.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary guidance plus plain text article metadata and body content from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided WeChat Official Account article URL and may use headless browser automation to retrieve article content.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
