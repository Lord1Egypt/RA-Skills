## Description: <br>
Publishes articles to WeChat Official Account drafts when a user asks to publish or save a WeChat draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixinran2015](https://clawhub.ai/user/lixinran2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an agent prepare and publish HTML, Markdown, plain text, or configured article content into the WeChat Official Account draft workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to install dependencies, launch Playwright, run login flows, and publish content through a third-party CLI. <br>
Mitigation: Confirm the user's request is explicit before running install, browser, login, or publish commands, and review the referenced publisher project before use. <br>
Risk: WeChat authentication cookies may be present on the user's machine during draft publishing. <br>
Mitigation: Do not read or expose cookie contents, and keep WeChat cookie files out of git. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lixinran2015/publish-wechat-draft) <br>
- [Publisher project homepage](https://github.com/lixinran2015/weixingongzhonghao) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated article files when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run npm, Playwright, login, and publish commands after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
