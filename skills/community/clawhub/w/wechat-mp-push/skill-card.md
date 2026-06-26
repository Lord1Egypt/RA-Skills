## Description: <br>
支持通过AI生成符合公众号规范的图文（文章和贴图），并推送到公众号草稿箱，兼容其它SKILL生成的图文、图片进行推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lihengdao](https://clawhub.ai/user/lihengdao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to draft WeChat Official Account articles or image-card posts, save the required account configuration, and push generated HTML or public image URLs to a WeChat draft box. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pcloud QR authorization wizard and API receive WeChat account identifiers and unpublished draft content. <br>
Mitigation: Install and use the skill only when that service is trusted for the account and content involved, and keep config.json private. <br>
Risk: The documented cleanupDrafts action can clear account drafts if invoked for the wrong account or without clear intent. <br>
Mitigation: Do not invoke cleanupDrafts unless the user explicitly asks to clear drafts and has confirmed the target account and deletion scope. <br>
Risk: Pushing to the wrong AppID can send draft content to an unintended WeChat account. <br>
Mitigation: Verify the target AppID or selected account before each push, especially when multiple accounts are present in config.json. <br>
Risk: The push script may report timeout responses as successful background work, which can lead to duplicate pushes if retried immediately. <br>
Mitigation: After a timeout, check WeChat service notifications or the draft box before retrying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lihengdao/wechat-mp-push) <br>
- [WeChat MP Push configuration wizard](https://app.pcloud.ac.cn/design/wechat-mp-push.html) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML content, JSON configuration, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can submit generated HTML or image URL payloads to a WeChat draft workflow and returns JSON status from the push script.] <br>

## Skill Version(s): <br>
3.0.6 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
