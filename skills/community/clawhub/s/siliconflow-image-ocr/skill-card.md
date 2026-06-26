## Description: <br>
SiliconFlow OCR extracts text from screenshots, receipts, forms, and tables with mixed Chinese and English content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangziiiiii](https://clawhub.ai/user/wangziiiiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract text from screenshots, scans, receipts, invoices, forms, tables, and other document images. It is intended for OCR-focused workflows, including mixed Chinese and English text extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts and images are sent to the remote SiliconFlow OCR provider. <br>
Mitigation: Avoid processing IDs, financial records, confidential screenshots, or other sensitive images unless that transfer is acceptable for the user's workflow. <br>
Risk: Changing the API base URL can redirect prompts, images, and credentials to another endpoint. <br>
Mitigation: Leave the base URL at the documented SiliconFlow default unless the user intentionally trusts the alternate endpoint. <br>
Risk: The skill requires a private SiliconFlow API key. <br>
Mitigation: Keep the key in the SILICONFLOW_API_KEY environment variable or the documented local secrets file and do not include it in prompts, images, logs, or shared outputs. <br>


## Reference(s): <br>
- [Image Ocr on ClawHub](https://clawhub.ai/wangziiiiii/siliconflow-image-ocr) <br>
- [SiliconFlow Console](https://siliconflow.cn) <br>
- [SiliconFlow API Base URL](https://api.siliconflow.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Raw JSON from the SiliconFlow chat completions API, plus command-line status and error text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports prompt-only connectivity checks and OCR requests using a local image path or remote image URL; default max output is 512 tokens.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
