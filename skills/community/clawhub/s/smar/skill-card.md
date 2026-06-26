## Description: <br>
Extract text from images and scanned documents using PaddleOCR; supports 100+ languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duykhangdangzn1](https://clawhub.ai/user/duykhangdangzn1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to extract text, bounding boxes, and confidence data from images, screenshots, scanned PDFs, and image URLs using PaddleOCR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive documents or image URLs that the user provides. <br>
Mitigation: Process only documents the user is authorized to read, prefer local files or trusted URLs, and review OCR output before sharing it. <br>
Risk: Remote image URLs and Python dependency installation can introduce normal supply-chain or untrusted-source risk. <br>
Mitigation: Use trusted URLs and install PaddleOCR, PaddlePaddle, and related dependencies from trusted package sources. <br>
Risk: OCR output may be inaccurate for handwriting, very small text, complex backgrounds, rotated text, or poor image quality. <br>
Mitigation: Preprocess images, choose the correct language, enable angle classification when needed, filter low-confidence results, and manually review extracted text. <br>


## Reference(s): <br>
- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR) <br>
- [PaddleOCR Model Zoo](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_en/models_list_en.md) <br>
- [PaddleOCR Multi-language Support](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_en/multi_languages_en.md) <br>
- [ClawHub skill listing](https://clawhub.ai/duykhangdangzn1/smar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with OCR text, structured result examples, Python code snippets, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include extracted text, bounding boxes, confidence scores, language choices, and installation commands; OCR quality depends on image quality and configured language.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
