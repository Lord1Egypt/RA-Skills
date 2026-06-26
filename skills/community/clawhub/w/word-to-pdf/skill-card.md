## Description: <br>
Convert Word documents (.docx) to PDF using Python's reportlab library, with support for Chinese characters, emoji, and basic formatting preservation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lirenweiM](https://clawhub.ai/user/lirenweiM) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and other users use this skill to convert local .docx documents into PDF files from the command line. It is especially relevant when basic paragraphs, headings, lists, Chinese text, and emoji need to be carried into the generated PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing converter dependencies from untrusted sources can introduce supply-chain risk. <br>
Mitigation: Install reportlab and python-docx from trusted package indexes, preferably inside a virtual environment. <br>
Risk: The converter reads local documents and writes output files, so accidental file selection can expose or transform unintended content. <br>
Mitigation: Run it only on documents the user intentionally selects and review the target output path before execution. <br>
Risk: Generated PDFs may not preserve full Word layout, images, tables, or emoji exactly. <br>
Mitigation: Review the generated PDF before sharing or relying on it, especially for documents with complex formatting. <br>
Risk: Missing CJK fonts can cause Chinese text to render incorrectly. <br>
Mitigation: Install a supported Chinese font or configure an appropriate system font before conversion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lirenweiM/word-to-pdf) <br>
- [Publisher profile](https://clawhub.ai/user/lirenweiM) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [PDF file with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a selected .docx file and writes a local .pdf file; conversion fidelity depends on document structure, installed fonts, and python-docx/reportlab behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
