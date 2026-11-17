## Description:

腾讯文档 Markdown 技能，支持新建 Markdown 并写入内容、下载、删除、读取、更新、重命名等操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to create, read, download, update, rename, and delete Tencent Docs Markdown documents from natural-language requests or Python/CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Tencent Docs account-session cookies and can act with the permissions of that account.

Mitigation: Use a dedicated Tencent Docs account where possible, keep .cookies.json private, and run logout to clear saved credentials when work is complete.

Risk: Update, delete, and rename operations can mutate or remove Tencent Docs content.

Mitigation: Provide only explicit HTTPS docs.qq.com document URLs and confirm the target document before approving destructive actions.

Risk: The security review notes URL-validation and scoping issues that deserve review before installation.

Mitigation: Update the flagged URL-validation behavior before using the skill with sensitive documents.

Risk: Read and download operations expose document content to the current agent session, terminal output, or local files.

Mitigation: Avoid using the skill with highly sensitive documents unless the execution environment and output handling are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wscats/skills/tencent-docs-markdown)
- [Tencent Docs](https://docs.qq.com)
- [Tencent Docs desktop](https://docs.qq.com/desktop)
- [Python](https://www.python.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown content, Tencent Docs URLs, local .md files, status text, and JSON-like command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Docs session cookies stored in .cookies.json for authenticated operations.]

## Skill Version(s):

1.1.7 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
