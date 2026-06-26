## Description: <br>
微信读书 AI 阅读助手，可通过扫码登录获取阅读进度、归档章节内容、拉取标注笔记，并支持围绕阅读内容的 AI 对话。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colorlessboy](https://clawhub.ai/user/colorlessboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate WeRead browser sessions, export reading progress, chapters, highlights, notes, screenshots, and chat records for personal reading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores WeRead session cookies and private reading data in local files. <br>
Mitigation: Use it only on trusted machines, keep the generated profile and books directories out of shared or synced folders, and delete profile/weread-cookies.json when the session is no longer needed. <br>
Risk: The login flow includes an avoidable unsafe shell call for QR download. <br>
Mitigation: Review or patch the login flow to use Node or Playwright download APIs before deployment. <br>
Risk: The artifact warns that third-party WeRead automation may create account risk. <br>
Mitigation: Use an account and workflow appropriate for that risk and confirm the service terms before relying on automated export. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/colorlessboy/weread-dl) <br>
- [Playwright documentation](https://playwright.dev) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated local Markdown, JSON, screenshot, cookie, and chapter files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local WeRead cookies, reading history, notes, chapter text, screenshots, metadata, and chat logs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
