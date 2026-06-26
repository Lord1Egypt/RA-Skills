## Description: <br>
Super File Manager helps agents scan cleanup candidates, preview file organization, detect duplicate files, run folder backups, move files with logs, and roll back logged operations across macOS, Linux, and Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yy756127197](https://clawhub.ai/user/yy756127197) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to clean up local files, organize directories, identify duplicates, create backups, move files with an audit log, and restore logged operations after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move, trash, back up, and restore local files. <br>
Mitigation: Run scan and preview commands first, and require explicit user confirmation before any move, trash, backup, or rollback action. <br>
Risk: Skipping backup verification can leave important backups unchecked. <br>
Mitigation: Avoid using --no-verify for important backups unless the user accepts the tradeoff. <br>
Risk: Restoring trashed files with common filenames may match by filename rather than exact trash metadata. <br>
Mitigation: Review the operation log and target path before restoring files from trash. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yy756127197/super-file-manager) <br>
- [README](README.md) <br>
- [CHANGELOG](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with command snippets and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file paths, scan summaries, backup reports, operation logs, and rollback guidance.] <br>

## Skill Version(s): <br>
2.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
