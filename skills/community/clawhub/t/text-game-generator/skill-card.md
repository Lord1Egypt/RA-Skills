## Description: <br>
根据用户主题生成文字游戏剧本，内置19种成熟模板（古代家族、偶像养成、末日求生、校园恋爱、修仙等），支持导出Word文档到桌面。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[810722796-lgtm](https://clawhub.ai/user/810722796-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, game designers, and interactive-fiction creators use this skill to generate structured Chinese text-game scripts from a requested theme or one of the bundled genre templates. It can also format the generated script as Markdown and export it to a Word document when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Word export workflow uses a user-controlled title in a shell command, which could run unintended commands if the title is malformed. <br>
Mitigation: Use Word export only after an explicit export request, keep titles benign, and sanitize or quote the title before running the export command. <br>
Risk: Generated game scripts may contain genre-specific romance, survival, family, or power-dynamic content that is not suitable for every audience. <br>
Mitigation: Review the selected template and generated script before sharing or exporting it, and adjust content boundaries for the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/810722796-lgtm/text-game-generator) <br>
- [文字游戏剧本模板汇总](artifact/references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown text-game script with optional shell command for Word export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a .docx file on the user's desktop when the Word export workflow is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
