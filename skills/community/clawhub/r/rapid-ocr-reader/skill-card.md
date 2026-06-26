## Description: <br>
Image Reader extracts text from images, screenshots, photos, and other image files using OCR for Chinese and English text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rendaixue-byte](https://clawhub.ai/user/rendaixue-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to read text from screenshots, document photos, diagrams, receipts, invoices, and other image files. It returns extracted text with line-level confidence, bounding boxes, and image metadata for downstream analysis or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images may contain passwords, financial data, private documents, or confidential screenshots that OCR will extract into text. <br>
Mitigation: Process only images whose text you intend to expose to the agent workflow, and avoid sensitive images unless disclosure is acceptable. <br>
Risk: RapidOCR models may download automatically on first use. <br>
Mitigation: Install and run the skill only in environments where RapidOCR, ONNX Runtime, Pillow, and first-run model downloads are approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rendaixue-byte/rapid-ocr-reader) <br>
- [Publisher Profile](https://clawhub.ai/user/rendaixue-byte) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON containing extracted text, per-line confidence scores, bounding boxes, line count, errors, and image metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on user-provided image files; RapidOCR models may download automatically on first use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
