## Description: <br>
Automates WeChat Official Account draft creation and publishing workflows through API scripts, including access-token management plus cover and body-image uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlr25](https://clawhub.ai/user/zlr25) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, content operators, and automation agents use this skill to prepare WeChat Official Account article drafts, upload selected local images, and connect article publishing steps to scripted or scheduled workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat AppID and AppSecret credentials and caches access tokens locally. <br>
Mitigation: Keep config.json and .tokens out of source control, restrict local file permissions, and rotate credentials or tokens if exposed. <br>
Risk: Selected cover and article body images are uploaded to the WeChat material library. <br>
Mitigation: Review image paths and article HTML before execution so only intended files are uploaded. <br>
Risk: Scheduled publishing workflows can repeatedly create drafts or upload files if cron jobs are left active. <br>
Mitigation: Monitor scheduled jobs and remove or disable cron entries when the publishing workflow is no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zlr25/wechat-accounts-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/zlr25) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com) <br>
- [Usage README](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Python or Node.js code references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces WeChat draft creation guidance and commands that may upload selected local image files and create drafts through the WeChat API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
