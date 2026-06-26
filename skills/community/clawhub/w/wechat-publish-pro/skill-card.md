## Description: <br>
Converts Markdown articles into WeChat Official Account styled HTML and can publish them as WeChat draft articles with theme and cover-image support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuesf](https://clawhub.ai/user/yuesf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and agent users can use this skill to prepare Markdown articles for WeChat Official Accounts and create draft posts after configuring WeChat credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use WeChat Official Account credentials to create external draft articles. <br>
Mitigation: Install only from a trusted publisher, provide credentials deliberately, and review drafts in the WeChat console before public release. <br>
Risk: Credentials may be stored or loaded from local configuration and environment files. <br>
Mitigation: Protect local config files, avoid sharing sensitive unpublished content, and prefer environment-specific secret handling where possible. <br>
Risk: The helper script includes unsafe environment-file sourcing and eval-based command execution behavior identified by the security evidence. <br>
Mitigation: Avoid scripts/publish.sh until the helper script is fixed; prefer explicit wechat-publish-pro CLI commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuesf/wechat-publish-pro) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/) <br>
- [WeChat developer platform](https://developers.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, HTML, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and generated WeChat-formatted HTML or draft creation actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local Markdown, HTML, image, and configuration files and may create WeChat draft content through the WeChat API when credentials are configured.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
