## Description: <br>
Automates common Word/WPS document operations on Windows through COM, including reading text, editing content, formatting headings, headers and footers, page breaks, merge and split workflows, export to PDF or TXT, and image insertion for single-document use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fadeloo](https://clawhub.ai/user/Fadeloo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-automation users use this skill to issue command-line Word/WPS operations for individual Windows documents, such as extracting text, replacing content, adding headings or headers and footers, merging or splitting files, exporting documents, and adding images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit and write local Word/WPS documents, which can overwrite or alter important files if paths are chosen carelessly. <br>
Mitigation: Use copies for important documents, provide explicit output paths, and review generated documents before replacing originals. <br>
Risk: The automation may use Microsoft Word as a fallback when WPS is unavailable or not selected explicitly. <br>
Mitigation: Select the intended application with the documented app option and verify the local Word/WPS environment before running edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Fadeloo/tiangong-wps-word-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command examples; script outputs may include plain text, DOCX, PDF, TXT, or image-updated documents.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows with Microsoft Word or WPS Writer and Python with pywin32; intended for single-document operations rather than batch processing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
