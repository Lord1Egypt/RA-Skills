## Description:

TDOC Docx helps agents create, read, edit, convert, compare, annotate, and analyze Word documents, including DOCX/DOC files, Chinese official document formats, tables, images, comments, and tracked changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenrichard](https://clawhub.ai/user/wenrichard)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, document-heavy teams, and external users can use this skill to automate Word document creation, extraction, editing, conversion, diffing, review comments, tracked changes, and word-count analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A template can steer the agent into web search and generated Python execution without clear user control.

Mitigation: Require explicit approval for web search and generated code execution, and review or disable the red-head template before deployment.

Risk: Helper scripts can install system dependencies, fetch remote files, and use shared /tmp LibreOffice helpers.

Mitigation: Run the skill in a constrained environment, review remote file sources before fetching, and avoid sensitive documents until shared /tmp helper behavior is remediated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wenrichard/skills/tdoc-docx)
- [Skill Definition](artifact/SKILL.md)
- [Official Document Template Rules](artifact/templates/official_document/rules.md)
- [Red-Head Document Template Rules](artifact/templates/red_head/rules.md)
- [Python Dependencies](artifact/requirements.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, Python snippets, JSON edit rules, and generated document files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify DOCX, DOC, PDF, Markdown, JSON, image, and diff-report files depending on the user's request.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, pyproject.toml, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
