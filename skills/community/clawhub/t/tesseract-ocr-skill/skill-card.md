## Description:

基于Tesseract引擎的OCR文字识别技能，支持中文、英文、中英混合三种模式，输出text/structured/question_answer三种格式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tom859174-sketch](https://clawhub.ai/user/tom859174-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to extract Chinese, English, or mixed-language text from local images with Tesseract OCR and return plain text, structured text, or question-and-answer style output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local image paths and can write OCR results to a user-provided output path.

Mitigation: Run it only on images and output locations you intentionally choose, and review output paths before execution.

Risk: Server security guidance notes import and missing-dependency bugs that may prevent reliable execution.

Mitigation: Validate the skill in a controlled environment with Tesseract OCR, pytesseract, and Pillow installed, and fix dependency or import issues before relying on production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tom859174-sketch/skills/tesseract-ocr-skill)
- [Tesseract Windows Installer Wiki](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [text, structured data, files]

**Output Format:** [JSON or console text containing OCR status, extracted text, processed text, and optional structure fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports language selection for Simplified Chinese, English, or mixed Chinese-English OCR, plus text, structured, and question_answer output modes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
