## Description: <br>
微信公众号文章发布工具。使用 wxgzh CLI 将 Markdown 文章发布到公众号草稿箱。触发场景：用户要发公众号文章、配置公众号 AppID/AppSecret、生成封面图、Markdown 转 HTML。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyhue1991](https://clawhub.ai/user/lyhue1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content publishers use this skill to prepare WeChat Official Account drafts from Markdown, configure account credentials, generate cover images, and convert Markdown to WeChat-ready HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses a third-party CLI that can publish WeChat Official Account draft content. <br>
Mitigation: Review the npm package and confirm the exact article, cover, account, and publishing options before running publish commands. <br>
Risk: The workflow handles sensitive WeChat AppID and AppSecret credentials. <br>
Mitigation: Do not paste secrets into shared chats or logs, and protect the local wxgzh configuration file. <br>


## Reference(s): <br>
- [wxgzh ClawHub release](https://clawhub.ai/lyhue1991/wxgzh) <br>
- [Public IP lookup](https://ip.sb/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local wxgzh configuration, generated cover images, converted HTML, and draft-publishing commands.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
