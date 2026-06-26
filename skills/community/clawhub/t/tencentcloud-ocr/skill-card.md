## Description: <br>
TencentCloud OCR calls Tencent Cloud GeneralAccurateOCR to extract text from images, image URLs, and single-page PDFs, with optional word-level data and resume parsing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to OCR uploaded images, image URLs, screenshots, and PDF pages, then return extracted text as JSON. It also provides guidance for converting OCR text from multilingual resumes into readable Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, PDFs, image URLs, and resume contents may be sent to Tencent Cloud for OCR processing. <br>
Mitigation: Install only when that processing path is acceptable, require confirmation for sensitive documents, and avoid processing IDs, legal files, resumes, or screenshots without user approval. <br>
Risk: Tencent Cloud API credentials are required for operation. <br>
Mitigation: Use a dedicated least-privilege Tencent Cloud API key, keep credentials in environment variables, avoid logging or committing secrets, and monitor quota and billing. <br>


## Reference(s): <br>
- [Tencent Cloud GeneralAccurateOCR API documentation](https://cloud.tencent.com/document/api/866/37831) <br>
- [Multilingual resume parsing guidance](references/resume-parsing.md) <br>
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/tencentcloud-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [JSON OCR results and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials in environment variables; image inputs are capped at 10MB and PDF OCR is single-page.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
