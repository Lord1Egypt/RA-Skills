## Description: <br>
Converts RSS articles and web article URLs into WeChat Official Account-ready article data, HTML guidance, and optional draft-publishing workflow commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangbaixun](https://clawhub.ai/user/huangbaixun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content operators use this skill to fetch RSS or article URLs, extract article metadata and body content, and guide an agent in producing WeChat-compatible HTML. It also supports optional cover-generation and draft-publishing workflows when local credentials and scripts are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can fetch arbitrary article URLs. <br>
Mitigation: Use only public article URLs and avoid internal, private, or sensitive links. <br>
Risk: The workflow can use WeChat publishing credentials when local publishing is configured. <br>
Mitigation: Keep WeChat secrets out of shared or committed files and restrict permissions on local configuration files. <br>
Risk: Draft upload can publish or stage externally visible content if credentials and publishing scripts are configured. <br>
Mitigation: Require manual review of generated HTML and article metadata before any draft upload to WeChat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangbaixun/rss-to-wechat) <br>
- [User Guide](references/USER_GUIDE.md) <br>
- [WeChat HTML Template](references/html-template.md) <br>
- [Configuration Example](references/config.example.sh) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, JSON article data, and WeChat-compatible HTML instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local draft files and optional publishing commands when configured by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
