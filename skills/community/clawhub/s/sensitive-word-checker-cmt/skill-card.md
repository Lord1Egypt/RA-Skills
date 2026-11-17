## Description:

Checks PDF, Word, and Excel files for sensitive or prohibited words from a built-in or external word library and highlights matches in yellow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[betty831221](https://clawhub.ai/user/betty831221)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external reviewers, and document compliance teams use this skill to scan contracts and business documents for configured sensitive terms, then produce highlighted review copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Output handling can overwrite a document when the output directory resolves to the same location and filename as the input document.

Mitigation: Use a separate output folder, keep backups of originals, and review generated files before relying on them for contract or business decisions.

Risk: Dependency installation and document parsing may expose sensitive business files to unpinned or untrusted local packages.

Mitigation: Install dependencies in a virtual environment from pinned, trusted packages before processing important documents.

## Reference(s):

- [Usage Guide](artifact/references/usage.md)
- [ClawHub Skill Page](https://clawhub.ai/betty831221/skills/sensitive-word-checker-cmt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated highlighted document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces highlighted DOCX, XLSX, or PDF copies using a built-in 65-word library or an external DOCX word list.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
