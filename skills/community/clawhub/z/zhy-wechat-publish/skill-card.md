## Description: <br>
Use when publishing HTML articles to WeChat Official Account drafts, especially when you need cover upload, automatic cover generation, body image rewriting, CSS-variable compatibility, or draft metadata like author and comment settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhylq](https://clawhub.ai/user/zhylq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare WeChat Official Account drafts from local HTML articles, including cover handling, body image upload, WeChat-compatible formatting, and draft metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads .env files from the skill directory, the current working directory, and an ancestor project path, which can expose unrelated secrets during execution. <br>
Mitigation: Use a dedicated skill-local .env containing only the required WeChat and image-generation keys, and run it from a workspace that does not contain unrelated secrets. <br>
Risk: The image upload helper can modify an .env file when --write-env is used. <br>
Mitigation: Avoid --write-env unless you have verified which .env file will be edited; update configuration manually when practical. <br>
Risk: The skill needs WeChat draft and media-upload access through app credentials. <br>
Mitigation: Use credentials intended for this workflow and confirm the WeChat IP whitelist before running draft or media upload commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhylq/zhy-wechat-publish) <br>
- [Publisher profile](https://clawhub.ai/user/zhylq) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and commands for creating WeChat drafts; scripts may upload images and create draft entries through WeChat APIs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
