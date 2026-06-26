## Description: <br>
安全文件编辑器 helps agents preview file edits, create backups, write changes atomically, and roll back changes through a Python API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suda6632](https://clawhub.ai/user/suda6632) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to edit a writable text file with a preview step, a backup, an audit log, and a rollback path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit any writable file. <br>
Mitigation: Use it only on user-approved paths, avoid secrets, system files, and production data unless separate backups exist, and restrict filesystem access around the agent where possible. <br>
Risk: The promised confirmation safeguard is not enforced by the Python API. <br>
Mitigation: Always run dry_run first, inspect the proposed diff manually, and require an explicit external approval step before calling with dry_run set to false. <br>
Risk: Incorrect old_text matching can replace unintended content. <br>
Mitigation: Use sufficiently unique old_text, review the preview output, and keep the generated backup path for rollback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suda6632/safe-file-editor) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Python implementation](artifact/safe_file_editor.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Files, Guidance] <br>
**Output Format:** [Python dataclass results with diff-style text, backup paths, hashes, and log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run calls return previews without writing; commit calls can modify one writable file, create a backup, and return rollback information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact SKILL.md also states v1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
