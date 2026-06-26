## Description: <br>
Helps an agent draft WeChat Official Account articles and save them to the account draft box using the WeChat public platform APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinian5216](https://clawhub.ai/user/xinian5216) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to prepare WeChat Official Account article content, upload a required cover image, and save a draft through shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat AppID, AppSecret, and access tokens to call WeChat APIs. <br>
Mitigation: Keep config.sh private, avoid logging or pasting tokens, rotate AppSecret when needed, and limit access through the WeChat IP allowlist. <br>
Risk: Incorrect article HTML, cover image setup, or API parameters can cause failed draft creation or unintended draft content. <br>
Mitigation: Review the article HTML and cover image before running the scripts, upload the cover image as permanent material first, and test with a restricted or test account where possible. <br>


## Reference(s): <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com) <br>
- [WeChat Official Account Draft API Reference](references/api_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xinian5216/wechat-mp-draft) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided WeChat AppID, AppSecret, access token handling, a cover image media ID, and review of article HTML before API submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
