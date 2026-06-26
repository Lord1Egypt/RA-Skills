## Description: <br>
Extracts plain text with word-level bounding box coordinates from images and scanned documents using the Upstage OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upstage-deployment](https://clawhub.ai/user/upstage-deployment) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they need an agent to OCR images or scanned documents, return extracted text, and preserve word-level coordinate data. It is not intended for layout-aware document parsing or schema-driven field extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents selected for OCR are sent to Upstage's external OCR service for processing. <br>
Mitigation: Avoid highly sensitive IDs, legal, medical, financial, or confidential business documents unless the user has reviewed and accepted Upstage's data handling terms. <br>
Risk: The skill requires an UPSTAGE_API_KEY credential. <br>
Mitigation: Read the key from the environment and do not paste, print, or store the secret in generated code or output files. <br>


## Reference(s): <br>
- [Upstage OCR documentation](https://console.upstage.ai/api/document-digitization/ocr) <br>
- [ClawHub skill page](https://clawhub.ai/upstage-deployment/upstage-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and curl examples; OCR results are JSON files when implemented by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload user-selected documents to Upstage for OCR processing; agents should print the resolved absolute output path when writing OCR JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
