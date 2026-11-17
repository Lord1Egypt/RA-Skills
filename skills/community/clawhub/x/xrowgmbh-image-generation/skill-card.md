## Description:

Create or revise document, PDF, web, or review images with the requested format, sharp raster output, and artifact validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xrowgmbh](https://clawhub.ai/user/xrowgmbh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to create or revise images for documents, web pages, reviews, and release artifacts, while preserving requested formats and checking the resulting assets before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image revisions can drift from the requested format or style, making the result unsuitable for its consumer.

Mitigation: Keep the requested format and style, and confirm the output file format before delivery.

Risk: Raster images may be too small or hard to read at their final display size, especially in print-bound PDFs.

Mitigation: Render at the intended source resolution and check dimensions and readability; use sufficient pixels and about 300 DPI metadata for print-bound PNGs.

Risk: A downstream PDF or DOCX may drop or mishandle an intended image.

Mitigation: Inspect the final downstream document to confirm that the intended image is present and readable.

Risk: Scanner coverage is partial because some referenced local paths were not bundled; the inspected components had no reported findings.

Mitigation: Review the complete skill contents and referenced files before installation, treating unavailable paths as unassessed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xrowgmbh/skills/xrowgmbh-image-generation)

## Skill Output:

**Output Type(s):** [Image files, Guidance]

**Output Format:** [Image files in the requested raster or vector format, with validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves requested format and style; checks image dimensions, DPI, and downstream embedding when applicable.]

## Skill Version(s):

1.147.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
