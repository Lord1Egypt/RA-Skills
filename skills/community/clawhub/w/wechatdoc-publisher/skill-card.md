## Description: <br>
Automates preparing a Markdown article for a WeChat Official Account draft by getting an access token, handling the cover image, uploading permanent media, building draft JSON, and submitting the draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liboss504](https://clawhub.ai/user/liboss504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators with a supported WeChat Official Account use this skill to convert a Markdown article and cover image into a WeChat draft for review before publication. <br>

### Deployment Geography for Use: <br>
Global where WeChat Official Account APIs are available. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires WeChat AppID/AppSecret credentials that can control the configured account. <br>
Mitigation: Keep wechat_credentials.json private and out of source control, use least-privilege operational access where possible, and rotate the AppSecret if exposure is suspected. <br>
Risk: Running the publish flow uploads persistent media and creates a draft in the configured WeChat account. <br>
Mitigation: Review the article, cover image, target account, and generated draft before publishing or sharing it. <br>
Risk: WeChat API calls depend on the account IP whitelist. <br>
Mitigation: Verify the correct outbound IP for the execution environment before adding it to the WeChat whitelist and keep the whitelist limited to trusted hosts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liboss504/wechatdoc-publisher) <br>
- [微信公众号 API 参考](references/api_ref.md) <br>
- [微信公众号凭证配置指南](references/credentials_guide.md) <br>
- [WeChat Official Accounts platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Markdown article path, cover image path, and local WeChat AppID/AppSecret credentials; scripts may create persistent media and a draft in the configured account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version record) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
