## Description: <br>
Create drafts and publish articles to WeChat Official Account, with API mode for service accounts and browser automation for personal subscription accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antaeus001](https://clawhub.ai/user/antaeus001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create WeChat Official Account drafts from supplied titles, article content, and cover images, then optionally submit or save them through WeChat API or browser-based workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on a WeChat Official Account and may create or submit account content. <br>
Mitigation: Install only for accounts where this authority is acceptable, prefer draft creation over immediate publishing, and manually review content before final publication. <br>
Risk: Browser mode may expose WeChat admin page content to an analyzer model or API endpoint. <br>
Mitigation: Prefer API mode when available; for browser mode, use a local or trusted analyzer endpoint and avoid external API keys unless the page data can be shared with that provider. <br>
Risk: Browser session data is stored in a local profile directory and debug or step modes can save page captures. <br>
Mitigation: Avoid shared machines, protect or clear the browser profile directory, and enable debug or step capture only when needed. <br>
Risk: WeChat admin UI changes can make browser automation incomplete or inaccurate. <br>
Mitigation: Use check-only or draft-saving workflows first and verify the resulting draft in WeChat before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antaeus001/wechat-official-account) <br>
- [Publisher profile](https://clawhub.ai/user/antaeus001) <br>
- [WeChat Official Account API endpoint](https://api.weixin.qq.com) <br>
- [WeChat Official Account admin](https://mp.weixin.qq.com) <br>
- [DashScope-compatible analyzer endpoint](https://coding.dashscope.aliyuncs.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create WeChat drafts, submit publication requests, save browser-session drafts, and print JSON status when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
