## Description: <br>
微信公众号运营工具 helps agents support WeChat Official Account operations across topic research, article drafting, image preparation, formatting, publishing workflows, and performance review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liboss504](https://clawhub.ai/user/liboss504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to plan and prepare WeChat Official Account articles, configure publishing credentials, create drafts through the WeChat API, and review post-publication metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles WeChat Official Account credentials and browser session state that could allow account publishing actions if exposed. <br>
Mitigation: Store AppSecret values and saved browser state outside shared or synced workspaces, exclude them from git, restrict file permissions, and rotate secrets if exposure is suspected. <br>
Risk: The source includes high-impact IP whitelist guidance for API access. <br>
Mitigation: Whitelist only an outbound IP that the user controls or explicitly trusts, and avoid whitelisting 112.8.202.216 unless the runtime behind that address is known and trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liboss504/wechat-official-tool) <br>
- [WeChat Official Platform](https://mp.weixin.qq.com) <br>
- [WeChat API Base](https://api.weixin.qq.com) <br>
- [API Reference](references/api_ref.md) <br>
- [Credentials Guide](references/credentials_guide.md) <br>
- [Installation Guide](assets/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, JSON credential examples, and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided WeChat AppID/AppSecret credentials for API publishing workflows; generated content should be reviewed before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
