## Description: <br>
Create, inspect, and edit Microsoft Word documents and DOCX files with reliable styles, numbering, tracked changes, tables, sections, and compatibility checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbo405](https://clawhub.ai/user/linbo405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill when an agent needs to create, inspect, review, or edit Word and DOCX files while preserving styles, numbering, comments, fields, tables, sections, and layout-sensitive document structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DOCX review workflows can expose hidden revisions, comments, metadata, or deleted text. <br>
Mitigation: Only provide documents the user is comfortable having the agent inspect or edit, and review tracked changes, comments, and metadata before sharing outputs. <br>
Risk: Complex DOCX layout, fields, references, numbering, and tables can drift across Word, LibreOffice, Google Docs, or conversion tools. <br>
Mitigation: Use OOXML-aware edits, preserve styles and anchors, and verify round-trip compatibility before delivery. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/linbo405/xiaomolong-word-docx) <br>
- [Skill homepage](https://clawic.com/skills/word-docx) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with optional code or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include document inspection, editing, and compatibility-check steps; the skill itself is non-executable guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
