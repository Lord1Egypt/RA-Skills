## Description: <br>
Calls Tencent Cloud OCR's ExtractDocAgent API to extract user-defined structured fields from images or single-page PDFs for documents such as contracts, invoices, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to call Tencent Cloud OCR for structured extraction from document images or PDFs when fields, field types, and prompts are supplied by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents, document URLs, and extracted OCR results are sent to Tencent Cloud OCR. <br>
Mitigation: Use the skill only for documents approved for Tencent Cloud processing and review data-handling requirements for sensitive contracts, invoices, or regulated content. <br>
Risk: Tencent Cloud credentials are required for API calls. <br>
Mitigation: Use a least-privilege Tencent Cloud key stored in environment variables and rotate it according to the deployment's credential policy. <br>
Risk: OCR calls may create billing exposure or dependency drift in controlled environments. <br>
Mitigation: Review Tencent Cloud billing rules before use and pin the Tencent Cloud SDK version where reproducibility is required. <br>


## Reference(s): <br>
- [Tencent Cloud ExtractDocAgent API documentation](https://cloud.tencent.com/document/api/866/126442) <br>
- [ClawHub release page](https://clawhub.ai/zt1314p-design/tencentcloud-ocr-extractdocagent) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [JSON results with optional raw Tencent Cloud OCR response and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials; accepts an image URL or Base64/file input, item definitions, optional PDF page number, region, raw output flag, and user-agent value.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
