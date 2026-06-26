## Description: <br>
Helps agents create, read, edit, convert, validate, and analyze Microsoft Word .docx documents, including document structure, formatting, tracked changes, comments, images, tables, and XML repair guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sougannkyou](https://clawhub.ai/user/sougannkyou) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and agents use this skill to produce guidance, code snippets, and shell-command workflows for creating, inspecting, editing, converting, and validating .docx files. It is suited to Word document work such as reports, memos, letters, tracked changes, comments, tables, images, and document XML repair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DOCX editing, conversion, and validation commands can modify local files or expose sensitive tracked changes and comments. <br>
Mitigation: Review commands before execution, work on copies of important documents, and inspect tracked changes or comments before sharing outputs. <br>
Risk: Globally installed document tooling, including npm dependencies, may change behavior or introduce supply-chain risk. <br>
Mitigation: Vet and pin dependencies where possible before installing or using them in a workflow. <br>
Risk: Manual DOCX XML edits can produce invalid or corrupted documents. <br>
Mitigation: Validate generated or repacked DOCX files and retain the original document until the edited output is confirmed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sougannkyou/toolkit-docx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file operations and document conversion or validation steps that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.21.4 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
