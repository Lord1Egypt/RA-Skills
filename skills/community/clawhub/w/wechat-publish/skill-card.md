## Description: <br>
Creates WeChat Official Account article drafts from copy and images, with guidance for generating assets, uploading them to WeChat materials, and publishing when the account supports it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams and agents use this skill to prepare illustrated articles, upload required media to WeChat, and create WeChat Official Account drafts for review or publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses WeChat credentials to upload permanent media and create or submit public content. <br>
Mitigation: Keep AppID, App Secret, and access tokens out of logs and shell history, and limit credential use to the intended WeChat account. <br>
Risk: Generated text or images could be published before a human verifies accuracy, rights, and account suitability. <br>
Mitigation: Review the generated draft and uploaded images in WeChat, and require explicit approval before any public publish command is run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuchenggong19851114-design/wechat-publish) <br>
- [WeChat Official Accounts platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash, JSON, and HTML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat AppID, App Secret, access token, and account permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
