## Description: <br>
Convert LaTeX (.tex) academic papers to Word (.docx) with editable OMML equations, native Word tables, embedded figures, IEEE two-column format, and bibliography. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsyummy](https://clawhub.ai/user/wsyummy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and academic authors use this skill to convert LaTeX manuscripts into editable Word documents while preserving supported display equations, tables, figures, bibliography entries, and IEEE-style formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter adds a fixed company affiliation and Gmail address to generated documents without user control. <br>
Mitigation: Review or edit the converter before use, and inspect generated DOCX files to remove unwanted affiliation or email text before sharing, submitting, or publishing. <br>
Risk: Document conversion can change formatting or content in ways that are hard to notice before distribution. <br>
Mitigation: Run the verification script, compare the generated DOCX against the source document, and use the skill only on copies of source files. <br>
Risk: The workflow depends on local pandoc and Python packages. <br>
Mitigation: Install dependencies in a virtual environment and confirm pandoc is available before converting documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wsyummy/tex2docx) <br>
- [Pandoc documentation](https://pandoc.org) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Guidance] <br>
**Output Format:** [DOCX file with terminal progress and verification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local pandoc plus python-docx, lxml, and pypandoc_binary; supported display math is converted to editable OMML while inline math is plain text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
