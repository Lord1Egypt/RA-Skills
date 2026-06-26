## Description: <br>
PDF and image OCR that converts a single PDF or image into Markdown through the WiseDiag cloud API, including text extraction, table recognition, and multi-column layout support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wisediag](https://clawhub.ai/user/wisediag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users can use WiseOCR to convert one PDF or image at a time into a Markdown file when cloud OCR processing by WiseDiag is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are sent to WiseDiag's cloud service for OCR processing. <br>
Mitigation: Use the skill only for documents whose contents may be processed by WiseDiag; avoid confidential, regulated, identity, financial, credential, biometric, or minor-related documents unless WiseDiag's terms are acceptable. <br>
Risk: The skill requires a WiseDiag API key through WISEDIAG_API_KEY. <br>
Mitigation: Store the API key in a temporary environment variable or secret manager and avoid committing or sharing it. <br>
Risk: Cloud OCR output can be incomplete or inaccurate for difficult scans, tables, or layouts. <br>
Mitigation: Review the generated Markdown before relying on it for downstream decisions or records. <br>


## Reference(s): <br>
- [WiseOCR ClawHub release](https://clawhub.ai/wisediag/wiseocr) <br>
- [WiseDiag API key management](https://console.wisediag.com/apiKeyManage) <br>
- [WiseOCR registry homepage](https://github.com/wisediag/WiseOCR) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown file written to disk with CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes a single PDF or supported image per command and saves the result to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.28 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
