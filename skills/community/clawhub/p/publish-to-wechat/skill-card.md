## Description: <br>
AI-ready skill to format and publish Markdown articles to WeChat Official Accounts using Wenyan CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyriswu](https://clawhub.ai/user/kyriswu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to prepare Markdown articles with WeChat-compatible frontmatter, formatting, images, and Wenyan CLI publish commands for WeChat Official Accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content and upload referenced images to a WeChat Official Account using WeChat credentials. <br>
Mitigation: Review the article, frontmatter, cover image, image paths, and destination account before running publish commands. <br>
Risk: WeChat credentials may be exposed if copied into chat, files, logs, or source control. <br>
Mitigation: Provide credentials through secure environment variables or a secret manager, and avoid printing or storing the secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kyriswu/publish-to-wechat) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML frontmatter and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WECHAT_APP_ID and WECHAT_APP_SECRET to be provided securely before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
