## Description: <br>
Publish and download WeChat Public Platform content and Baijiahao articles via a local CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-chen2050](https://clawhub.ai/user/ai-chen2050) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare, publish, download, and inspect WeChat Public Platform and Baijiahao content through `wechat-public-cli` commands. It also guides configuration of account credentials, article metadata, custom CSS, downloads, and statistics queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live WeChat and Baijiahao account credentials. <br>
Mitigation: Keep `wechat-public.config.json` out of source control and shared folders, prefer environment variables or a secret store, and restrict local file permissions. <br>
Risk: Publish and send-all commands can affect live public accounts and audiences. <br>
Mitigation: Require explicit human confirmation before running publish or send-all commands, and review article metadata, media, and recipient scope before execution. <br>
Risk: The skill depends on an external local CLI and upstream package or repository. <br>
Mitigation: Install only when the publisher and external CLI are trusted, and review the package or repository before granting account credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-chen2050/wechat-public-cli) <br>
- [Declared project homepage](https://github.com/ai-chen2050/obsidian-wechat-public-platform) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and CSS examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local CLI usage guidance for commands that may publish content, send messages, download articles, emit JSON statistics, or update article styling.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
