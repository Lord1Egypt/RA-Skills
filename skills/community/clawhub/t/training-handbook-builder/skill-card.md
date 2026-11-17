## Description:

Generates Chinese-language training handbooks and printable Word documents with structured chapters, cover pages, tables, highlights, case callouts, table-of-contents fields, and page numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwenqi123123](https://clawhub.ai/user/liuwenqi123123)

### License/Terms of Use:

MIT-0

## Use Case:

Training teams, educators, and organizational documentation authors use this skill to research, structure, and generate Chinese-language training manuals, operation guides, white papers, and printable handbook-style materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The disclosed dependency install step is not pinned and could install an unexpected python-docx version.

Mitigation: Use an isolated Python environment and pin python-docx to a reviewed version before running the generation script.

Risk: The skill relies on web research for current policies, cases, and industry material, which can introduce stale or unsuitable content.

Mitigation: Confirm web research is appropriate for the handbook topic and verify policy names, publication dates, issuing organizations, and cited facts before publication.

Risk: The output is designed for Chinese-language handbooks and may not fit another language or locale without adaptation.

Mitigation: Confirm Chinese-language output is intended before using the generated document template or publishing the handbook.

## Reference(s):

- [培训手册内容结构参考](references/content_structure.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell commands for generating a Word .docx handbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a customizable .docx handbook through python-docx; Word field updates may be needed for the table of contents and page numbers.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
