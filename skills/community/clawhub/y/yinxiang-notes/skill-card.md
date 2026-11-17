## Description:

印象笔记（中国版）集成 skill。使用 Developer Token 在印象笔记中创建、整理和搜索笔记。支持笔记本列表、创建笔记、更新笔记内容/标签、移动笔记到废纸篓、查看/清空废纸篓、搜索内容、增量同步到 Obsidian vault。适用于使用 app.yinxiang.com 的用户。

This skill is ready for commercial/non-commercial use.

## Publisher:

[suepradun](https://clawhub.ai/user/suepradun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a Yinxiang Notes account from an agent, including listing notebooks and tags, creating, updating, deleting, and searching notes, and syncing notes to a local Obsidian vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires broad access to a Yinxiang/Evernote account through a Developer Token.

Mitigation: Install only when that account access is acceptable, use a dedicated skill-scoped secret location, and remove token-printing debug output before deployment.

Risk: The skill can write note contents and attachments to local disk during Obsidian sync.

Mitigation: Review and restrict the sync destination, protect the local vault, and avoid syncing sensitive notebooks unless local persistence is intended.

Risk: Trash-emptying behavior can permanently delete notes.

Mitigation: Require explicit confirmation before permanent trash deletion and review the trash contents before running destructive commands.

Risk: An undocumented note export script may expose note content outside the documented workflow.

Mitigation: Delete or document get_note_enml.py before release so reviewers and users understand its behavior.

Risk: A configurable NoteStore URL could send requests to an unintended endpoint.

Mitigation: Validate the NoteStore URL against expected Yinxiang production or sandbox hosts before making API calls.

## Reference(s):

- [Yinxiang Developer Token](https://app.yinxiang.com/api/DeveloperToken.action)
- [Yinxiang NoteStore API endpoint](https://app.yinxiang.com/shard/s16/notestore)
- [Yinxiang Sandbox NoteStore API endpoint](https://sandbox.yinxiang.com/shard/s1/notestore)
- [Evernote ENML DTD](http://xml.evernote.com/pub/enml2.dtd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can cause API-backed account changes and local file writes when the generated commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
