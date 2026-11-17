## Description:

Rapid OCR extracts text and structured fields from invoices, train tickets, travel receipts, and other document images using RapidOCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaojiren](https://clawhub.ai/user/gaojiren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, finance teams, and travel operations users can use this skill to recognize receipt and ticket images, then extract OCR text and common invoice or train-ticket fields for review and downstream entry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive OCR output from invoices, travel records, or receipts may appear in shared logs, terminals, or downstream records.

Mitigation: Run the skill in a controlled environment and avoid sending OCR output to shared destinations unless that handling is intended.

Risk: The PyPI OCR dependency downloads model files during first use, which creates network and supply-chain considerations.

Mitigation: Use a sandbox or pinned dependency set, pre-download models in a trusted environment for offline use, and confirm first-run network access before deployment.

## Reference(s):

- [ClawHub rapid ocr release](https://clawhub.ai/gaojiren/skills/rapid-ocr)
- [OpenClaw Rapid OCR documentation](https://docs.openclaw.ai/skills/rapid-ocr)
- [PaddleOCR model source](https://github.com/PaddlePaddle/PaddleOCR)

## Skill Output:

**Output Type(s):** [text, structured data, shell commands, guidance]

**Output Format:** [Markdown or terminal text with OCR text and Python dictionary-style structured fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR results may include confidence values, elapsed time, and extracted invoice or train-ticket fields.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
