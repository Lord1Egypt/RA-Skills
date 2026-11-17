## Description:

Removes light translucent text watermarks and flat-colour header logos from scanned page images or PDFs, with per-page checks to help assess content preservation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c0s1n3](https://clawhub.ai/user/c0s1n3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can clean suitable lecture notes, handouts, workbooks, and other scanned documents in image or PDF form. The workflow is intended for light translucent watermarks and flat-colour header logos, with representative pages reviewed before relying on results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated pixel checks cannot guarantee that every cleaned page is free of content changes.

Mitigation: Keep the originals and inspect representative cleaned pages before relying on the results.

Risk: PDF output is rasterized and loses selectable text.

Mitigation: Retain the original PDF when searchable text is needed, and review the rasterized output.

Risk: Header-logo removal may remove a logo the user wants to keep.

Mitigation: Use the documented --no-logo option when the header logo should remain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c0s1n3/skills/scan-watermark-removal)
- [PDF and header-logo handling](references/pdf-and-logo.md)
- [Watermark colour and signature guide](references/watermark-signature.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Verification metrics]

**Output Format:** [Cleaned image files or rasterized PDF, with per-page verification metrics in terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Original files are preserved; PDF output is rasterized and does not retain selectable text.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
