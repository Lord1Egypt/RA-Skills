## Description:

Formats, validates, and manages diagrams for Chinese-language Word (.docx) consulting deliverables across financial due diligence, legal due diligence, risk assessment, tax risk assessment, and financial analysis reports using configuration-driven Python tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiwikibk](https://clawhub.ai/user/hiwikibk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and document-production teams use this skill to normalize Word report styling, insert grayscale structured diagrams, and generate delivery-readiness validation summaries for five client-facing consulting report types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and update path can pull changing remote code and unpinned dependencies.

Mitigation: Install from a pinned reviewed commit and pin Python or npm dependency versions before production use.

Risk: The skill creates persistent files under ~/.workbuddy and runs local Python scripts on user documents.

Mitigation: Run it only on documents appropriate for local processing and review generated documents before delivery.

Risk: The optional Mermaid backend introduces additional runtime dependencies.

Mitigation: Use the default structured renderer unless Mermaid-specific diagram types are required.

## Reference(s):

- [Formatting standards](artifact/references/formatting_standards.md)
- [ClawHub skill page](https://clawhub.ai/hiwikibk/skills/word-formatter)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Formatted DOCX files, PNG diagrams, Markdown validation summaries, and concise shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Never overwrites the original input document; generated outputs should be reviewed before delivery.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
