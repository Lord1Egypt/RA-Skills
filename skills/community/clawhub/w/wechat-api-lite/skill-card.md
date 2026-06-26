## Description: <br>
A lightweight WeChat Official Account API skill for token management, image upload, and article draft creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youhan2021](https://clawhub.ai/user/youhan2021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use this skill to automate WeChat Official Account media upload and draft creation while keeping the publishing workflow minimal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local WeChat AppID, AppSecret, and cached access tokens. <br>
Mitigation: Keep config.env and scripts/.token_cache private, apply restrictive file permissions where possible, and do not commit or paste credentials or tokens. <br>
Risk: Upload and create-draft commands send selected files and draft JSON content to the WeChat Official Account API. <br>
Mitigation: Review draft JSON and selected image paths before running upload or create-draft commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/youhan2021/wechat-api-lite) <br>
- [WeChat Official Account Platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can print access tokens, media IDs, uploaded image URLs, draft media IDs, and draft counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
