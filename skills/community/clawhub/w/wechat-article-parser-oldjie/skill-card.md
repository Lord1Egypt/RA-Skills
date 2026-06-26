## Description: <br>
解析微信公众号文章，提取核心要点和干货。当用户发送公众号文章链接时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oldjie](https://clawhub.ai/user/oldjie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill in supported agents to fetch WeChat Official Account articles and produce concise, detail-preserving summaries. It is intended to preserve key points, context, links, prices, examples, data, and author viewpoints when they appear in the article. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup may clone code and install Node.js, Playwright, and browser dependencies. <br>
Mitigation: Review the artifact and lockfiles before installation, approve dependency and browser downloads explicitly, and install in a normal user account or sandbox where possible. <br>
Risk: The fetch script opens a user-provided WeChat article URL in headless Chromium and processes page content. <br>
Mitigation: Use only intended mp.weixin.qq.com article URLs, avoid entering credentials in the browser session, and review extracted content before relying on summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oldjie/wechat-article-parser-oldjie) <br>
- [Node.js](https://nodejs.org) <br>
- [Playwright](https://playwright.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown summary plus extracted article metadata and body text from the fetch script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The fetch script accepts a WeChat Official Account article URL and prints title, author, publish time, and article text for the agent to summarize.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
