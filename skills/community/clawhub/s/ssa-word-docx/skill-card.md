## Description: <br>
Create, read, and edit Word documents (.docx) with support for templates, tables, and styling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation users use this skill to generate, read, and edit local Word documents, including quotations, templates, styled tables, and DOCX layout details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business documents may include default quotation branding or placeholder values if reused without review. <br>
Mitigation: Replace the default quotation branding and verify generated document content before using it for real business communication. <br>
Risk: The quotation script can optionally import a neighboring quotation workflow validator when present. <br>
Mitigation: Use a trusted Python environment and review the optional quotation_schema dependency before relying on validation behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/ssa-word-docx) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [generate_quotation_docx.py](artifact/scripts/generate_quotation_docx.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is intended for local DOCX workflows and may produce or modify .docx files when the user runs generated code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
