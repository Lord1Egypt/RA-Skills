## Description: <br>
从屏幕截图中提取文字，支持纯文本、结构化及问答分离格式，适合中医考试题识别。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tom859174-sketch](https://clawhub.ai/user/tom859174-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert screenshot images into OCR text or structured question-and-answer output, especially for Chinese medicine exam screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots may contain sensitive personal, account, or confidential information. <br>
Mitigation: Avoid processing sensitive screenshots unless necessary and review extracted text before sharing or storing it. <br>
Risk: OCR output may be incomplete or incorrect, especially for exam questions and answers. <br>
Mitigation: Verify OCR results against the original screenshot before relying on the extracted content. <br>
Risk: The skill depends on local OCR libraries and image-processing dependencies. <br>
Mitigation: Install OCR dependencies from trusted sources and keep the local environment maintained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tom859174-sketch/screenshot-ocr-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON containing status, original text, processed text, and optional structured OCR data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text, structured, and question_answer output formats.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
