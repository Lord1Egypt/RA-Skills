## Description: <br>
Browse, search, and extract text from papers in a local Zotero library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyononthemoon](https://clawhub.ai/user/lyononthemoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and users with a local Zotero library use this skill to search papers, inspect item metadata, read stored PDFs, summarize documents, and export extracted PDF text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a user's local Zotero database and stored PDFs, which may contain private research data. <br>
Mitigation: Install only when local Zotero access is intended, review the configured database and storage paths before use, and avoid sharing outputs that include sensitive library content. <br>
Risk: Using the output option saves extracted document text as plaintext at the selected path. <br>
Mitigation: Choose output paths deliberately, limit extraction with page or info options when appropriate, and remove plaintext exports that are no longer needed. <br>
Risk: The artifact includes hard-coded Windows Zotero paths that may not match the user's environment. <br>
Mitigation: Update the database and storage paths before running the scripts in a different Zotero installation. <br>


## Reference(s): <br>
- [Zotero SQLite Database Schema](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write extracted PDF text to a user-specified plaintext output file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
