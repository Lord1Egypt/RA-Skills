## Description:

Helps agents parse PDF, Word, and CNKI documents, synthesize evidence-traceable literature reviews, adapt journal style when samples are provided, and generate Word documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liqiang12689](https://clawhub.ai/user/liqiang12689)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and academic writers use this skill to turn user-provided literature files into evidence-traceable narrative reviews, evidence matrices, citation audits, and editable Word documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided documents or folders and creates extracted text and DOCX files locally.

Mitigation: Provide only the documents needed for the review, avoid broad directories, and check generated files before sharing or reusing them.

Risk: Untrusted PDF, Word, or CNKI files carry normal document-processing risk, especially when optional converters, OCR tools, or package installs are involved.

Mitigation: Process untrusted files in a constrained local environment and review any optional sudo package install before running it.

Risk: Incomplete extraction, OCR errors, or metadata-only inputs can lead to unsupported review claims or citation mistakes.

Mitigation: Review the extraction manifest, warnings, citation audit, and evidence matrix before relying on the generated literature review.

## Reference(s):

- [Document Ingestion](references/document-ingestion.md)
- [Evidence Extraction](references/evidence-extraction.md)
- [Synthesis and Structure](references/synthesis-and-structure.md)
- [Journal Style Profile](references/journal-style-profile.md)
- [Citation and Quality Audit](references/citation-and-quality-audit.md)
- [Word Output](references/word-output.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown reports and editable DOCX files, with optional shell commands for local parsing and document generation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create extracted text, manifest JSON, Markdown source, and DOCX output from user-provided documents.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
