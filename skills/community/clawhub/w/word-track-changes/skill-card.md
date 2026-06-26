## Description: <br>
Enables Microsoft Word's Track Changes on DOCX documents using native OOXML elements, with cross-run text matching, paragraph-level replacement, visible insertions and deletions, and support for text split across multiple w:t nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elio-huang-15](https://clawhub.ai/user/elio-huang-15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to edit DOCX files while preserving visible tracked revisions that can be reviewed, accepted, or rejected in Microsoft Word. It is useful for replacing text, inserting paragraphs, marking deletions, and applying batches of document revisions while preserving formatting where possible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill rewrites user-selected DOCX files and may expose tracked changes or author metadata to document recipients. <br>
Mitigation: Write to a new output path, keep an original backup, and review the Word Review pane before sharing the edited DOCX. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local DOCX files with Microsoft Word Track Changes markup; users should review the Word Review pane before sharing edited documents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
