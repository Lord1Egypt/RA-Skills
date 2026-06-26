## Description: <br>
Rapid OCR helps agents run local OCR on receipts, invoices, train tickets, and general images, returning recognized text and structured fields for common Chinese ticket workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaojiren](https://clawhub.ai/user/gaojiren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, finance teams, travel administrators, and developers use this skill to extract OCR text and structured fields from invoices, transportation tickets, receipts, and scanned images. It is suited for local batch recognition and assisted data entry where important OCR results are reviewed before reliance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The rapidocr-onnxruntime dependency downloads OCR models on first use, which may be unsuitable for locked-down or offline environments. <br>
Mitigation: Install only where PyPI dependency installation and first-run model download are allowed, or pre-download models on a trusted network before offline deployment. <br>
Risk: OCR may misread important fields such as tax IDs, invoice numbers, dates, and monetary amounts. <br>
Mitigation: Manually verify important OCR results before using them for financial, tax, reimbursement, or compliance decisions. <br>
Risk: Unpinned dependencies can change model download behavior or runtime behavior over time. <br>
Mitigation: Pin rapidocr-onnxruntime and validate the expected model cache behavior in controlled environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gaojiren/rapid-ocr) <br>
- [OpenClaw Rapid OCR Documentation](https://docs.openclaw.ai/skills/rapid-ocr) <br>
- [PaddleOCR Model Source](https://github.com/PaddlePaddle/PaddleOCR) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Python dictionaries from the CLI/API, with Markdown guidance and command examples in agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OCR output can include full recognized text, per-line confidence values, elapsed time, and structured invoice or train-ticket fields.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
