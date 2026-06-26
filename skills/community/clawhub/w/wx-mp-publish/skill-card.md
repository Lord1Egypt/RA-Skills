## Description: <br>
微信公众号文章发布技能，可将带 YAML frontmatter 的 Markdown 文章转换为微信友好的 HTML，上传封面图，创建草稿，并提供 API 发布或手动发布指引与常见错误处理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shimonxin](https://clawhub.ai/user/shimonxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare and publish Markdown articles to a WeChat public account workflow. It helps convert Markdown to styled HTML, manage cover images and drafts, inspect quota/status, and fall back to manual publishing when account permissions block API publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a WeChat public-account workflow with credential access. <br>
Mitigation: Install only for accounts where this access is intended, keep WeChat credentials scoped and protected, and review configuration before executing publishing commands. <br>
Risk: The bundled scripts include draft deletion and rebuild behavior that could alter account-level drafts. <br>
Mitigation: Review or remove delete and rebuild scripts before installation, and require manual confirmation for publish, delete, and rebuild actions. <br>
Risk: The skill includes local record-writing and optional local facts or tracker updates. <br>
Mitigation: Disable or review local facts and article-tracker updates unless that local state management is explicitly desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shimonxin/wx-mp-publish) <br>
- [微信公众号发布最佳实践](references/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated HTML/API workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or delete WeChat drafts and may read local WeChat credential configuration when the provided Node.js scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
