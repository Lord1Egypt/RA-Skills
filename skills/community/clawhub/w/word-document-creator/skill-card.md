## Description: <br>
Creates and validates Word .docx documents by using Microsoft Word COM to create a native template and python-docx to write styled content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woaiwojia8899](https://clawhub.ai/user/woaiwojia8899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents on Windows use this skill to generate styled Word documents from a title, content blocks, and an output path. It is suited to document-generation workflows that can run Microsoft Word COM automation and python-docx. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unrelated memory/database persistence references create unclear data handling expectations. <br>
Mitigation: Use only with non-sensitive documents unless the persistence references are removed or made opt-in with documented data scope, retention, and deletion controls. <br>
Risk: User-supplied output paths may write to unintended locations or overwrite existing Word files. <br>
Mitigation: Review output paths before execution and write generated documents to a dedicated working directory. <br>
Risk: The skill depends on local Microsoft Word COM automation and a Windows-specific Python environment. <br>
Mitigation: Install and test it only in an environment with Microsoft Word, pywin32, and python-docx available before using it in a workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/woaiwojia8899/word-document-creator) <br>
- [Publisher Profile](https://clawhub.ai/user/woaiwojia8899) <br>
- [Artifact Skill Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [DOCX files with status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Microsoft Word COM, python-docx, and a Windows Python environment; validates file existence, file size, and document structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
