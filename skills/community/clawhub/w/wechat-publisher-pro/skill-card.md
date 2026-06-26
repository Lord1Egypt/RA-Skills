## Description: <br>
Helps an agent prepare and run a WeChat Official Account draft-publishing workflow for Markdown or HTML articles, including cover image upload and simple HTML formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qujingyang28](https://clawhub.ai/user/qujingyang28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to configure WeChat Official Account credentials, convert article content, upload a cover image, and create a draft for manual review before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires WeChat APPID and APPSECRET credentials that can authorize account actions. <br>
Mitigation: Treat APPSECRET like a password, provide it only at runtime, and keep it out of committed files, prompts, logs, screenshots, and shell history. <br>
Risk: The package can create WeChat drafts from local article and image files through external API calls. <br>
Mitigation: Use only accounts and files intended for this workflow, and manually inspect every created draft in WeChat before publishing publicly. <br>
Risk: Server security guidance reports weak safety controls and inconsistent setup instructions for some options. <br>
Mitigation: Review the package before installing and verify paths, dry-run behavior, environment-variable loading, digest, beautify, and author options before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qujingyang28/wechat-publisher-pro) <br>
- [Publisher profile](https://clawhub.ai/user/qujingyang28) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create WeChat draft content through the WeChat API when executed with user-provided account credentials.] <br>

## Skill Version(s): <br>
3.1.3 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
