## Description: <br>
Automatically turns Zhihu trending topics into IT-style WeChat Official Account article drafts with topic selection, content research, image selection, HTML formatting, and draft creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dachenchen690-droid](https://clawhub.ai/user/dachenchen690-droid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, developers, and technical content teams use this skill to turn selected Zhihu hot topics into WeChat-ready IT articles, including research notes, formatted HTML, images, and a WeChat draft workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles WeChat service account credentials and cached access tokens that can create drafts and upload media. <br>
Mitigation: Use environment variables or a credential vault, avoid sharing credentials in chat, and remove or rotate cached WeChat tokens after use. <br>
Risk: Generated articles and selected images may be unsuitable, inaccurate, or inappropriate for publication without review. <br>
Mitigation: Review generated content, images, and WeChat draft previews before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dachenchen690-droid/zhihu-to-wechat) <br>
- [WeChat Official Account API reference](references/wechat_api.md) <br>
- [WeChat HTML style guide](references/wechat_html_style.md) <br>
- [IT article template](assets/it_article_template.md) <br>
- [WeChat Official Accounts platform](https://mp.weixin.qq.com) <br>
- [Unsplash Developers](https://unsplash.com/developers) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with generated article text, WeChat-compatible HTML, JSON-like API results, and shell command instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create WeChat drafts and upload media when configured with service account credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
