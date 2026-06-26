## Description: <br>
知识星球公开笔记管理：创建笔记、编辑笔记、查看笔记详情、查看笔记列表、删除笔记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsxq](https://clawhub.ai/user/zsxq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to manage public Knowledge Planet notes for a logged-in user, including creating, listing, viewing, editing, and deleting notes. It is intended for public shareable notes only, not private or sensitive information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notes created or edited with this skill are public to anyone with the link. <br>
Mitigation: Review note text and image attachments before approving creation or edits, and do not include private or sensitive information. <br>
Risk: Delete operations permanently remove notes and cannot be recovered. <br>
Mitigation: Confirm the target note ID and current note contents with the user before approving deletion. <br>
Risk: The skill acts through the user's logged-in zsxq-cli account. <br>
Mitigation: Install and use it only when the agent should manage Knowledge Planet notes for that account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zsxq/zsxq-note) <br>
- [note +create](artifact/references/zsxq-note-create.md) <br>
- [note +list](artifact/references/zsxq-note-list.md) <br>
- [note +detail](artifact/references/zsxq-note-detail.md) <br>
- [note +edit](artifact/references/zsxq-note-edit.md) <br>
- [note +delete](artifact/references/zsxq-note-delete.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with zsxq-cli shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires zsxq-cli and an authenticated Knowledge Planet account.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
