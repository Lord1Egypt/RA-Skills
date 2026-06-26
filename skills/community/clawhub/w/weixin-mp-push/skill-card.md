## Description: <br>
Supports generating WeChat Official Account articles and image-card posts, then pushing HTML or public image URLs to a selected account's draft box through QR-based configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lihengdao](https://clawhub.ai/user/lihengdao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, and agents use this skill to create WeChat Official Account posts in the required HTML format, configure one or more accounts through a QR authorization flow, and push prepared content to a chosen account's draft box. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores account-linked WeChat configuration locally in config.json. <br>
Mitigation: Keep config.json private, store only configuration produced by the QR authorization flow, and remove or rotate it when account access should no longer be available. <br>
Risk: Draft content and push actions are sent through the pcloud.ac.cn service. <br>
Mitigation: Use the skill only when that third-party processing is acceptable, and avoid sending confidential drafts unless the user has approved that exposure. <br>
Risk: Publishing and draft cleanup actions can affect the selected WeChat account. <br>
Mitigation: Review the target AppID before each push and invoke cleanupDrafts only when the user explicitly intends to clear drafts for that account. <br>
Risk: Timeout responses may still represent background success, which can lead to duplicate pushes if retried immediately. <br>
Mitigation: Check WeChat service notifications or the draft box before retrying after a timeout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lihengdao/weixin-mp-push) <br>
- [Publisher profile](https://clawhub.ai/user/lihengdao) <br>
- [WeChat configuration wizard](https://app.pcloud.ac.cn/design/weixin-mp-push.html) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML content requirements, JSON configuration examples, shell commands, and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local config.json and HTML files, then call a third-party service to push drafts to WeChat Official Account accounts.] <br>

## Skill Version(s): <br>
3.0.6 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
