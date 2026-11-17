## Description:

Word Studio helps agents create publication-ready Word documents for reports, papers, contracts, resumes, and other professional document types with templates, tables, charts, images, tables of contents, and multilingual formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and document authors use this skill to generate structured Word documents such as business reports, academic papers, contracts, resumes, meeting minutes, and financial or government-style documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documents are written locally, so the output location should be reviewed before execution.

Mitigation: Run the skill in an isolated workspace and confirm the target path before creating files.

Risk: The skill includes templates for legal, academic, financial, and government-style documents, but the templates are document-generation helpers rather than compliance advice.

Mitigation: Have qualified reviewers check domain-sensitive content before relying on or distributing generated documents.

Risk: .doc conversion depends on LibreOffice and may not preserve the requested format if conversion is unavailable.

Mitigation: Prefer .docx output and verify converted documents before sharing them.

## Reference(s):

- [Word Studio Skill Page](https://clawhub.ai/tobewin/skills/word-studio)
- [Formatting Standards](references/formatting-standards.md)
- [Document Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with Python and shell code blocks that produce Word document files, usually .docx.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus python-docx and pillow; .doc conversion depends on LibreOffice and may fall back to .docx.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
