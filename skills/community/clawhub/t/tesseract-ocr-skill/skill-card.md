## Description: <br>
基于Tesseract引擎的OCR文字识别技能，支持中文、英文、中英混合三种模式，输出text/structured/question_answer三种格式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tom859174-sketch](https://clawhub.ai/user/tom859174-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run local OCR on image files, especially Chinese, English, and mixed Chinese-English text. It can return plain extracted text, structured question/option/answer output, or question-answer pairs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local image files supplied by the user. <br>
Mitigation: Run it only on images intended for OCR processing and avoid pointing it at sensitive files. <br>
Risk: The optional output path can write OCR results to disk. <br>
Mitigation: Choose output paths deliberately and avoid paths that could overwrite important files. <br>
Risk: The skill depends on local OCR components and Python packages. <br>
Mitigation: Install pytesseract, Pillow, and Tesseract OCR from trusted sources before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tom859174-sketch/tesseract-ocr-skill) <br>
- [Tesseract OCR Windows installer wiki](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files] <br>
**Output Format:** [JSON or console text from a Python command-line helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text, structured, and question_answer output formats for OCR results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
