## Description:

OCR and extract tables from scanned PDFs and images using MinerU, converting image-based table structures into structured Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and data-entry automation users use this skill to invoke MinerU table OCR for scanned PDFs and image files, producing structured Markdown from table images and scanned documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party MinerU CLI and service for OCR processing.

Mitigation: Install only after reviewing and trusting MinerU/OpenDataLab, and prefer a pinned, reviewed CLI version.

Risk: Documents processed through MinerU may be sent to an external service.

Mitigation: Use the skill only for documents appropriate for that service and avoid sending sensitive content unless approved.

Risk: The MinerU token is required for extraction and can grant access to the service.

Mitigation: Keep MINERU_TOKEN scoped, protected, and out of logs, prompts, and committed files.

## Reference(s):

- [MinerU homepage](https://mineru.net)
- [MinerU token management](https://mineru.net/apiManage/token)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)
- [ClawHub skill page](https://clawhub.ai/mzlzyca/skills/table-ocr)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to use mineru-open-api with a MinerU token for PDF and image table extraction.]

## Skill Version(s):

0.4.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
