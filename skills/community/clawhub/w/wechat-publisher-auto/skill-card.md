## Description: <br>
Converts Markdown or HTML articles into WeChat Official Account-ready content, optionally rewrites drafts through a configured AI provider, and publishes them to a WeChat draft box. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuesf](https://clawhub.ai/user/yuesf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and agent users can use this skill to convert Markdown or HTML articles, configure WeChat Official Account credentials, optionally humanize draft text through an AI provider, and create draft posts for later review in WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on a WeChat Official Account and create public-account draft content. <br>
Mitigation: Use a dedicated WeChat credential with the smallest practical blast radius and review drafts in WeChat before publishing. <br>
Risk: AI humanization can send draft article text to the configured external AI provider. <br>
Mitigation: Disable AI humanization for confidential drafts unless the configured provider is approved for that content. <br>
Risk: Credentials are stored locally or loaded from environment files. <br>
Mitigation: Protect local configuration and environment files, rotate exposed credentials, and avoid sharing workspaces that contain them. <br>
Risk: The bundled shell helper is flagged as unsafe in the server security guidance. <br>
Mitigation: Avoid scripts/publish.sh until its behavior is reviewed and fixed; prefer directly invoking the installed CLI with reviewed arguments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuesf/wechat-publisher-auto) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [WeChat Official Account developer platform](https://developers.weixin.qq.com/) <br>
- [WeChat Official Account admin console](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets; generated article content may be HTML before being submitted as a WeChat draft.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May act on configured WeChat credentials, local article files, cover images, and optional AI-provider settings.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
