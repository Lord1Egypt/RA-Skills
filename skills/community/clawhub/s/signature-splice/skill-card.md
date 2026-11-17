## Description:

Preprocesses signature images, places them in a specified order within a PDF signature area, and renders the result for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomuiv](https://clawhub.ai/user/tomuiv)

### License/Terms of Use:

MIT

## Use Case:

People preparing forms, agreements, and other PDFs can arrange authorized handwritten or electronic signature images in a designated area and review the resulting document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signatures may be placed on a document without the signers' authorization.

Mitigation: Use only when authorized to place each signature on the target document.

Risk: Signature images, generated PDFs, and previews contain sensitive information.

Mitigation: Use a private output directory and remove temporary files when they are no longer needed.

Risk: An inserted signature image could be mistaken for a cryptographic PDF signature or proof of consent.

Mitigation: Treat the result as image placement only; use a separate digital-signature and consent process when required.

## Reference(s):

- [Signature Splice on ClawHub](https://clawhub.ai/tomuiv/skills/signature-splice)
- [Publisher profile](https://clawhub.ai/user/tomuiv)
- [Workflow guide](artifact/references/workflow.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can generate a PDF with image-based signatures and PNG previews for visual review.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
