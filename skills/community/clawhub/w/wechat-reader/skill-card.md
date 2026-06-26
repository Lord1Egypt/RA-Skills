## Description: <br>
Read WeChat public account articles when a user shares a mp.weixin.qq.com link, asks to read or summarize a WeChat article, or mentions public-account article content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imwyvern](https://clawhub.ai/user/imwyvern) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to open user-provided WeChat public-account article links with browser automation, extract visible article content, and summarize or translate it on request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens WeChat article links in a browser and summarizes visible page content. <br>
Mitigation: Confirm user intent before opening vague WeChat-related requests and summarize only content visible in the browser session. <br>
Risk: Some WeChat content may require login. <br>
Mitigation: Inform the user when a login wall appears and avoid entering WeChat credentials through the agent unless the user explicitly chooses to do so. <br>


## Reference(s): <br>
- [WeChat Article Reader on ClawHub](https://clawhub.ai/imwyvern/wechat-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text summaries, translations, and access-status notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include article text, image alt text, captions, or a notice that content is removed or login-gated.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
