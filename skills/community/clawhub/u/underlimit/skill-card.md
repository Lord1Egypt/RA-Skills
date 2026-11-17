## Description:

Shrink a scanned PDF to fit an upload size limit (a government, visa, university or job portal's 2 MB or 5 MB cap), offline, without sending the document anywhere. Use when the user has a PDF that is too big to upload, asks to compress or shrink a scanned PDF, or must get IDs, contracts, tax forms or other scans under a file-size limit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirceamitu](https://clawhub.ai/user/mirceamitu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Underlimit to shrink scanned PDFs to a portal's file-size limit on the machine holding the document, without uploading the source PDF to a service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive documents are processed using externally downloaded software dependencies.

Mitigation: Review and pin the package version before processing sensitive documents; for strict offline handling, provision dependencies first and block networking during processing.

Risk: Compression can reduce readability, and scanned output does not retain selectable text from text-bearing pages.

Mitigation: Check the output's readability and text-loss warnings before uploading it; do not use the compressed result when selectable text is needed.

## Reference(s):

- [Underlimit browser app and project information](https://mirceamitu.github.io/underlimit/)
- [Underlimit on ClawHub](https://clawhub.ai/mirceamitu/skills/underlimit)

## Skill Output:

**Output Type(s):** [Files, Shell commands, JSON]

**Output Format:** [A compressed PDF file and a JSON status object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The original PDF is not overwritten; if it already meets the limit, no output file is created. Text-bearing pages are rasterized, so selectable text is not retained.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
