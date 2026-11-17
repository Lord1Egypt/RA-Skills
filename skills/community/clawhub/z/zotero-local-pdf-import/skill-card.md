## Description:

通过 Zotero 本地连接器将用户提供的本地 PDF 文件导入 Zotero 文库，并支持单文件导入、文件夹批量导入、导入到已有分类、分类列表查看和最近附件检查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mxingchtongaelofficial2568](https://clawhub.ai/user/mxingchtongaelofficial2568)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to import local PDF files into a running Zotero desktop library through Zotero's local connector. It is intended for workflows where the user provides local PDF paths, a Zotero connector port, and optionally an existing Zotero collection name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary notes that the skill tells agents to automatically install a Python dependency before use.

Mitigation: Install reviewed dependencies manually in a virtual environment and avoid the automatic dependency-install path unless the user explicitly accepts that behavior.

Risk: The security guidance notes that the skill acts on PDF paths and Zotero ports supplied during use.

Mitigation: Use only PDF paths, folders, and Zotero ports that the user intentionally provides for the current import task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mxingchtongaelofficial2568/skills/zotero-local-pdf-import)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report dependency checks, Zotero connector status, selected collections, per-PDF import results, summary counts, collection listings, and recent attachment records.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
