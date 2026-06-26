## Description: <br>
Turns article text, files, or URLs into WeChat Official Accounts compatible Markdown and themed HTML, then publishes drafts or formal posts when WeChat publishing prerequisites are configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[08820048](https://clawhub.ai/user/08820048) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and publishing operators use this skill to normalize article content, choose a built-in Welight theme, generate WeChat-ready output, and optionally create a WeChat draft or formal post after credentials and account capabilities are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use WeChat Official Account credentials and network access to create drafts or publish posts. <br>
Mitigation: Keep app credentials in a trusted config or environment, use dry-run or draft mode first, and publish formally only after confirming account capability and user intent. <br>
Risk: Rendered article content, images, or theme output may not match the publisher's intent before posting. <br>
Mitigation: Review the generated Markdown, themed HTML, and image handling before creating a draft or submitting a formal publish request. <br>
Risk: URL-based article acquisition can fetch incomplete content or miss metadata. <br>
Mitigation: Continue only with usable content, state missing metadata, and keep normalized Markdown as the editable source before styling or publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/08820048/wechat-layout-publish) <br>
- [Publish Spec](references/publish-spec.md) <br>
- [Runtime Config](references/runtime-config.md) <br>
- [Theme Catalog](references/theme-catalog.md) <br>
- [Execution Spec](references/repo-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, WeChat-compatible HTML, JSON metadata, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown, HTML, metadata, or dry-run payload files; publishing requires configured WeChat credentials, network access, and account capabilities.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
