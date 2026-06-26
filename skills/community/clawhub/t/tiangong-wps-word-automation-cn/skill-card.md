## Description: <br>
Automates common Word and WPS Writer document operations on Windows via COM, including reading text, replacing or inserting content, setting headings, headers and footers, page breaks, merging, splitting, exporting, and adding images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation users use this skill to have an agent run local Windows commands that operate on individual Word or WPS Writer documents. It is intended for single-document workflows such as extraction, edits, formatting, export, merge, split, and image insertion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document operations can overwrite or alter original files when replacing text, inserting content, merging, splitting, exporting, or adding images. <br>
Mitigation: Work on copies of trusted documents and choose save, output, and output-directory paths carefully before running commands. <br>
Risk: The automation opens local documents through Microsoft Word or WPS Writer on Windows, so untrusted documents may expose the user to document-borne risks outside the skill itself. <br>
Mitigation: Run the skill only on trusted files in a controlled local environment with Word or WPS security settings kept enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jirboy/tiangong-wps-word-automation-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local command guidance for Windows Word/WPS automation; generated files depend on the selected command and user-provided paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
