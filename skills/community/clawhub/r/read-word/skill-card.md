## Description:

Read Microsoft Word documents (.docx and .doc) with Chinese support, extract text, search keywords, and save output as UTF-8 text files without requiring Microsoft Word.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincent-big-fish](https://clawhub.ai/user/vincent-big-fish)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract text from Microsoft Word .docx and legacy .doc files, search document paragraphs for keywords, inspect basic document statistics, and optionally export extracted text as UTF-8 text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Word documents from untrusted sources may trigger vulnerabilities in document parsing dependencies.

Mitigation: Open only documents from trusted sources where possible and keep parsing dependencies updated or pinned according to deployment policy.

Risk: The optional output flag can create or overwrite a text file at a user-specified path.

Mitigation: Use output paths that are intended for new or replaceable files and review the path before execution.

Risk: Legacy .doc extraction is partial and may produce incomplete or garbled text for complex files.

Mitigation: Validate extracted text before relying on it, and convert problematic legacy documents to .docx when higher fidelity is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincent-big-fish/skills/read-word)

## Skill Output:

**Output Type(s):** [text, files, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, UTF-8 text files, Python return values, and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-specified Word documents locally; optional export writes to a user-specified output path.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, _meta.json, __init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
