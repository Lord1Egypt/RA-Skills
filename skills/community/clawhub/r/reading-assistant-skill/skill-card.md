## Description: <br>
对话读书助理 helps users manage book excerpts as a local reading-notes knowledge base with tagging, search, import, export, and reading statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ludiansheng](https://clawhub.ai/user/ludiansheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, students, and knowledge workers use this skill to capture book excerpts, organize tags, search notes, import highlights, export reading records, and generate reading statistics in a local personal knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, display, import, export, and maintain personal reading notes in a local ./reading-notes knowledge base. <br>
Mitigation: Use explicit reading-assistant commands, keep imports to trusted note-export files, and review search, view, and export results before sharing them. <br>
Risk: Delete, import, export, and custom output-path workflows can overwrite or remove local note data. <br>
Mitigation: Confirm destructive actions carefully, keep backups of ./reading-notes, and avoid custom export paths unless overwriting that destination is safe. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ludiansheng/reading-assistant-skill) <br>
- [Chapter recognition rules](references/chapter-rules.md) <br>
- [Reading notes data structure](references/data-structure.md) <br>
- [Import format specification](references/import-formats.md) <br>
- [Export template guide](references/export-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text, Markdown or HTML exports, script-backed summaries, and local JSON note records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains a local ./reading-notes knowledge base and can import, export, display, overwrite, or delete note files when the user confirms those operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
