## Description: <br>
Smart PDF OCR helps agents extract text from scanned, image-based, and photographed PDFs using the mineru-open-api CLI, including quick OCR and advanced OCR for complex layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veeicwgy](https://clawhub.ai/user/veeicwgy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to OCR scanned PDFs and photographed documents, select an appropriate MinerU extraction mode, and produce searchable text or extracted document files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs may contain confidential, regulated, identity, medical, legal, or financial information that would be processed by the MinerU provider. <br>
Mitigation: Avoid those documents unless the user is comfortable with that provider processing them; confirm before OCR when the request is vague. <br>
Risk: The skill depends on the third-party mineru-open-api package and MinerU service. <br>
Mitigation: Install and use it only when the package and service are trusted, and review the generated command before running OCR. <br>
Risk: OCR quality can vary for complex layouts, tables, formulas, or multilingual documents. <br>
Mitigation: Use the advanced OCR, VLM, language, or pipeline options when appropriate and review extracted text before relying on it. <br>


## Reference(s): <br>
- [Smart PDF OCR on ClawHub](https://clawhub.ai/veeicwgy/smart-pdf-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and OCR output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mineru-open-api; flash-extract is intended for PDFs up to 10MB or 20 pages.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
