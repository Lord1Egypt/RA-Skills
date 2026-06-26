## Description: <br>
快速记录想法和笔记到本地文件，支持添加、查看、搜索和查看今日笔记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ikicc](https://clawhub.ai/user/ikicc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to capture local notes, review saved notes, search note content, and inspect notes for the current day. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The search command can be steered outside the notes folder. <br>
Mitigation: Constrain searches to ~/.quick-notes before use and avoid passing untrusted search arguments. <br>
Risk: The clear command deletes all stored notes without confirmation. <br>
Mitigation: Require explicit confirmation or move notes to a recoverable location before deleting them. <br>
Risk: Local notes may contain sensitive information. <br>
Mitigation: Do not use this skill for sensitive notes unless the search scope and clear behavior are hardened. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ikicc/quick-note) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Text responses and Markdown note files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Notes are stored locally by date under ~/.quick-notes/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
