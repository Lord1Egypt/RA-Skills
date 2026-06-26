## Description: <br>
Organizes Word documents by formatting paragraphs, generating a table of contents, applying standard styles, and cleaning redundant spacing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okgptai](https://clawhub.ai/user/okgptai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can use this skill to standardize local Word documents for academic, business, or minimal presentation styles. It is intended for formatting, table-of-contents generation, style normalization, and cleanup of .docx or .doc files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can overwrite the input Word document when output_path is not specified. <br>
Mitigation: Run it only on a copy of the document or specify an explicit output_path before execution. <br>
Risk: The dependency check may install python-docx with pip, modifying the Python environment and requiring package download access. <br>
Mitigation: Review and approve the dependency step first, preferably in an isolated virtual environment with dependencies installed ahead of time. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/okgptai/word-document-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated workflow modifies local Word documents and may create a timestamped backup before saving.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
