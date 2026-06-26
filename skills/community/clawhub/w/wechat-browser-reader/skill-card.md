## Description: <br>
Read WeChat Official Account articles (mp.weixin.qq.com) through Chrome DevTools browser automation when HTTP-based extractors fail due to captcha, JavaScript encryption, or anti-scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmlgit](https://clawhub.ai/user/zmlgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve and summarize user-provided WeChat Official Account articles when normal HTTP extraction fails. It guides the agent through an isolated Chrome DevTools session, captcha handling, content loading, and article text extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Chrome remote-debugging session can expose browser state if it is attached to a normal signed-in profile. <br>
Mitigation: Use a dedicated temporary Chrome profile for the debugging session, avoid sensitive accounts, and close the remote-debugging browser when finished. <br>
Risk: Repeated WeChat access may trigger captcha or rate-limiting. <br>
Mitigation: Follow the skill's verification flow when captcha appears and wait before retrying if captcha keeps recurring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zmlgit/wechat-browser-reader) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zmlgit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces extracted article fields such as title, author, content length, and full article text when the browser session succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
