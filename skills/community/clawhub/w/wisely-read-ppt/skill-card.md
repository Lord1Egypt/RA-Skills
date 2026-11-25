## Description:

Parses PPTX and PDF files into page-by-page drafts, then visually checks the text and illustrations to produce illustrated and image-free DOCX documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sedey999](https://clawhub.ai/user/sedey999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to convert presentations or PDFs into editable, page-structured Word documents with reviewed text and image descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan is partial and reports a text-preservation risk in image removal.

Mitigation: Review text preservation and required tool access before installing; compare the image-free document with the illustrated version before relying on it.

Risk: Several local references could not be resolved during scanning.

Mitigation: Review the skill's required tools and local references before installation, as advised by the scan guidance.

## Reference(s):

- [ClawHub release: wisely-read-ppt 1.7.0](https://clawhub.ai/sedey999/skills/wisely-read-ppt)
- [Subagent workflow reference](reference/subagent-workflow.md)
- [macOS LibreOffice prerequisite checks](reference/macos-install.md)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [DOCX (illustrated and image-free versions)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Page-structured editable text with image markers and descriptions; the illustrated version also includes page screenshots and images.]

## Skill Version(s):

1.7.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
