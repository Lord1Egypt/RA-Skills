## Description: <br>
Complete Word document processing skill for creating, reading, editing, converting, comparing, commenting on, and analyzing .docx and .doc files, including Chinese official-document formats, tables, images, tracked changes, and comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WenRichard](https://clawhub.ai/user/WenRichard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and document automation agents use this skill to create, inspect, edit, convert, compare, annotate, and summarize Word documents. It is especially suited to workflows that need DOCX/DOC handling, Chinese official-document templates, tracked changes, document comments, and conversion to PDF, Markdown, or images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process and alter local Word documents, including tracked changes and comments. <br>
Mitigation: Use a disposable workspace or sandbox, keep original copies, and manually verify documents after edits or after accepting tracked changes. <br>
Risk: The install and conversion workflows may run host tools and install system packages such as LibreOffice, pandoc, Poppler, and antiword. <br>
Mitigation: Review installation steps before use and install only in environments where those host-level dependencies are acceptable. <br>
Risk: The artifact includes URL and SFTP file-fetching workflows, which can introduce untrusted remote document inputs. <br>
Mitigation: Avoid remote inputs unless the source is trusted and scan fetched documents before processing them. <br>
Risk: Template and advanced document workflows can involve generated Python or XML edits. <br>
Mitigation: Review generated scripts and XML changes before execution or packaging. <br>


## Reference(s): <br>
- [TDOC Docx ClawHub release](https://clawhub.ai/WenRichard/tdoc-docx) <br>
- [Publisher profile](https://clawhub.ai/user/WenRichard) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [OpenClaw metadata](artifact/_meta.json) <br>
- [Python requirements](artifact/requirements.txt) <br>
- [Official document template rules](artifact/templates/official_document/rules.md) <br>
- [Red-head document template rules](artifact/templates/red_head/rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown, JSON, plain text, shell commands, Python code snippets, and generated document files such as DOCX, PDF, Markdown, images, and diff reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local Word-processing artifacts and may call local Python, LibreOffice, pandoc, Poppler, antiword, URL, or SFTP workflows when installed and requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, pyproject.toml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
