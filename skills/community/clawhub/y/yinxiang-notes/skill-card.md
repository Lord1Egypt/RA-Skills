## Description: <br>
印象笔记（中国版）集成 skill。使用 Developer Token 在印象笔记中创建、整理和搜索笔记。支持笔记本列表、创建笔记、更新笔记内容/标签、移动笔记到废纸篓、查看/清空废纸篓、搜索内容、增量同步到 Obsidian vault。适用于使用 app.yinxiang.com 的用户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suepradun](https://clawhub.ai/user/suepradun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Yinxiang/Evernote China notes from an agent workflow, including listing notebooks and tags, creating, updating, searching, deleting notes, managing trash, and syncing notes to an Obsidian vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Developer Token with broad access to a Yinxiang/Evernote account. <br>
Mitigation: Install only when the publisher is trusted, keep the token in a private .env file, and keep .env out of version control. <br>
Risk: The get_note_enml.py script retrieves a specific note and writes raw ENML content locally. <br>
Mitigation: Remove or avoid get_note_enml.py unless that exact diagnostic behavior is intended, and do not share terminal logs or generated note content. <br>
Risk: The Obsidian sync writes account content and attachments to a local vault path. <br>
Mitigation: Verify the target vault path before running sync_to_obsidian.py, especially on shared or backed-up systems. <br>
Risk: The empty_trash.py script can permanently delete all trashed notes. <br>
Mitigation: Run empty_trash.py only when irreversible deletion is intended and after reviewing the account trash contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suepradun/yinxiang-notes) <br>
- [Yinxiang Developer Token](https://app.yinxiang.com/api/DeveloperToken.action) <br>
- [Yinxiang NoteStore endpoint](https://app.yinxiang.com/shard/s16/notestore) <br>
- [Evernote ENML DTD](http://xml.evernote.com/pub/enml2.dtd) <br>
- [Yinxiang sandbox NoteStore endpoint](https://sandbox.yinxiang.com/shard/s1/notestore) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, Python script execution, local Markdown files, attachments, and HTML clip files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Developer Token and configured NoteStore URL; Obsidian sync writes local note, attachment, clip, and sync-state files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
