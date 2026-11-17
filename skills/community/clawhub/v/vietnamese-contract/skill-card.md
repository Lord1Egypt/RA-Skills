## Description:

Creates Vietnamese legal contracts, agreements, commitments, and related legal documents with legal-basis lookup, structured drafting, Vietnamese spell checks, optional CCCD/CMND OCR, and professional .docx output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustydev212](https://clawhub.ai/user/trustydev212)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft Vietnamese legal documents and generate formatted .docx files. It supports common contract categories and can optionally extract identity data from Vietnamese CCCD/CMND images for user-confirmed document prefill.

### Deployment Geography for Use:

Vietnam

## Known Risks and Mitigations:

Risk: The skill can process Vietnamese CCCD/CMND national ID data and pass extracted identity text to an active AI model.

Mitigation: Use OCR only with explicit ID-holder consent, avoid remote AI verification unless provider and retention terms are acceptable, and delete uploaded ID images and OCR outputs after use.

Risk: The OCR workflow installs and runs additional image-processing dependencies.

Mitigation: Install dependencies in an isolated, pinned environment and review the skill before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trustydev212/skills/vietnamese-contract)
- [OpenClaw Viet Nam community](https://zalo.me/g/lajsqc334jqc5fezevvo)
- [CCCD OCR guide](references/cccd-ocr-guide.md)
- [Contract structures](references/contract-structures.md)
- [DOCX formatting and Vietnamese spell checks](references/docx-formatting.md)
- [Vietnamese legal bases](references/legal-bases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with code blocks and generated .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and pandoc; optional OCR workflow requires EasyOCR and OpenCV dependencies.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
