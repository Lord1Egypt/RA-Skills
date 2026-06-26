## Description: <br>
TencentCloud IDCard OCR calls Tencent Cloud's IDCardOCR API to extract fields from mainland China resident identity card images using Base64 or image URL input, with optional cropping and warning detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send authorized Chinese ID card images to Tencent Cloud OCR and receive structured identity fields, crop outputs, and warning indicators for document-processing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive government identity document images and extracted identity fields through Tencent Cloud OCR. <br>
Mitigation: Use only with consent and a legal basis, avoid public image URLs when possible, protect OCR results from logs and shared chats, and follow the server security guidance. <br>
Risk: Tencent Cloud API credentials are required to run the skill. <br>
Mitigation: Use a dedicated least-privilege Tencent Cloud key and keep TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY out of source files, logs, and prompts. <br>


## Reference(s): <br>
- [Tencent Cloud IDCardOCR API documentation](https://cloud.tencent.com/document/api/866/33524) <br>
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/tencentcloud-ocr-idcard) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON] <br>
**Output Format:** [JSON response from Tencent Cloud OCR, with command-line usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials and either an image URL or Base64 image input.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
