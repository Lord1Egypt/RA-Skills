## Description: <br>
Publishes or saves WeChat Official Account articles by formatting content, uploading images, and creating drafts through the WeChat API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rookiebug1216](https://clawhub.ai/user/rookiebug1216) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to prepare WeChat Official Account posts from local Markdown, direct text, or a topic, choose a theme, upload images, and save the result as a WeChat draft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles WeChat App ID, App Secret, and access tokens. <br>
Mitigation: Use a dedicated or limited WeChat account, prefer environment variables or encrypted configuration, restrict credential file permissions, and rotate secrets regularly. <br>
Risk: Article content, saved drafts, and uploaded images are sent to WeChat services. <br>
Mitigation: Review content and images before execution, and avoid submitting confidential or private material unless the account and workflow are approved for that data. <br>
Risk: Remote image inputs and default cover-image fetching can expose private URLs or retrieve unintended content. <br>
Mitigation: Provide explicit local cover images where possible and do not pass internal, private, or sensitive URLs as image inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rookiebug1216/wechat-mp-skills) <br>
- [README.md](README.md) <br>
- [Credential encryption guide](ENCRYPTION.md) <br>
- [WeChat access token API](https://developers.weixin.qq.com/doc/subscription/api/base/api_getaccesstoken.html) <br>
- [WeChat image upload API](https://developers.weixin.qq.com/doc/subscription/api/material/permanent/api_uploadimage.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown or HTML article content plus JSON and CLI status from WeChat draft and media operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local files, upload images, save drafts to WeChat, and write optional JSON command output.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
