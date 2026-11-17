## Description:

Intelligent PDF reader and content extractor powered by MinerU API for extracting and summarizing content from PDFs, including scanned files, academic papers, reports, and books through the mineru-open-api CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and document-review workflows use this skill to read, extract, and summarize PDF content, including scanned, table-heavy, academic, financial, legal, and multilingual documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF content may be processed through external MinerU-related tooling without an explicit privacy disclosure in the artifact.

Mitigation: Use the skill only with PDFs appropriate for that tooling and avoid confidential documents unless the service's data handling is understood and approved.

Risk: The artifact recommends a mutable global npm installation for mineru-open-api.

Mitigation: Prefer a pinned, local, sandboxed installation before running extraction commands.

## Reference(s):

- [Smart PDF Reader on ClawHub](https://clawhub.ai/veeicwgy/skills/smart-pdf-reader)
- [Publisher profile: veeicwgy](https://clawhub.ai/user/veeicwgy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown and text extracted from PDFs, with optional output files and concise summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke mineru-open-api flash-extract or extract commands, including OCR, table recognition, and VLM model options described by the artifact.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
