## Description:

ZM PPTX 检查与审核工具用于读取、解析、提取、检查、拆分、合并或审核 PPTX 文件，重点支持渲染核验、文本抽取、备注、版式和资源检查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation reviewers use this skill to inspect PPTX files, extract text, review notes, layouts, and assets, and validate rendered output. It also supports template-based editing, cleanup, repacking, and creation of presentations when those workflows are appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines PPTX review with editing, cleanup, and creation workflows that can alter or remove presentation content.

Mitigation: Use copies or version-controlled presentations and keep backups before running cleanup, editing, or repacking workflows.

Risk: The LibreOffice helper may rely on an LD_PRELOAD native shim in temporary storage.

Mitigation: Use the conversion helper only in a contained workspace and avoid the preload shim where /tmp is shared or untrusted.

Risk: Dependency setup can encourage broad local or global installs.

Mitigation: Pin dependencies in an isolated project environment instead of installing globally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-pptx-inspect-review-tool)
- [Publisher profile](https://clawhub.ai/user/jerryxn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify PPTX-related files when users run the referenced helper scripts.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
