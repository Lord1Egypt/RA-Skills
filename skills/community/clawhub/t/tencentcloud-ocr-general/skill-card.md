## Description: <br>
TencentCloud General OCR calls Tencent Cloud's AdvertiseOCR API to recognize text from image URLs or base64 image inputs and return detected text, confidence, and bounding coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need to extract text and text-box coordinates from images through Tencent Cloud OCR. It supports URL and base64 image inputs and is suited for workflows that can send image content to Tencent Cloud for processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR inputs, including image contents or image URLs, are processed by Tencent Cloud and may contain sensitive personal, customer, financial, medical, or confidential business information. <br>
Mitigation: Use only with appropriate consent and review Tencent Cloud privacy, retention, and compliance requirements before processing sensitive images. <br>


## Reference(s): <br>
- [Tencent Cloud AdvertiseOCR API documentation](https://cloud.tencent.com/document/api/866/49524) <br>
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/tencentcloud-ocr-general) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON response with recognized text, confidence scores, bounding polygons, image size, and request ID; setup and usage guidance are Markdown with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials and sends image URLs or image content to Tencent Cloud OCR.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
