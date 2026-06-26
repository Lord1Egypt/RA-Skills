## Description: <br>
Posts Zhihu column articles and short thoughts by using Chrome Browser Relay to control a user's logged-in Chrome tab. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[InuyashaYang](https://clawhub.ai/user/InuyashaYang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and content operators use this skill to prepare and publish Zhihu column articles or short thoughts through a browser session they have already logged into and attached with Chrome Browser Relay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Zhihu browser tab and may publish public content with under-scoped confirmation controls. <br>
Mitigation: Require the agent to show the exact title, body, and media to the user and obtain explicit approval before clicking publish. <br>
Risk: The skill depends on browser relay access to an authenticated session. <br>
Mitigation: Use a dedicated browser profile or account where possible and attach only the intended Zhihu tab. <br>
Risk: Zhihu DOM selectors and editor behavior may change. <br>
Mitigation: Take an interactive snapshot before acting and verify that the selected controls still match the article or thought editor. <br>


## Reference(s): <br>
- [Zhihu DOM selector reference](references/dom-selectors.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Zhihu column editor](https://zhuanlan.zhihu.com/write) <br>
- [Zhihu home](https://www.zhihu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with browser actions, JavaScript snippets, shell commands, and optional JSON helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare Zhihu-friendly HTML and character counts for article or thought content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
