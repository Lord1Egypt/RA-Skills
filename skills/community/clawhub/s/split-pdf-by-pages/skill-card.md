## Description: <br>
将 PDF 中包含“显示日期”的页面切割成单独文件，并按原文件名与页码命名。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanw2039](https://clawhub.ai/user/hanw2039) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and developers can use this skill to generate Python code and command-line guidance for extracting PDF pages that contain the keyword “显示日期”. It supports single-file and batch workflows, with optional OCR guidance for scanned PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch mode processes every PDF in the selected directory and generated output names may overwrite existing files. <br>
Mitigation: Run the workflow on copies of important PDFs and choose an empty or dedicated output directory before batch processing. <br>
Risk: OCR support depends on locally installed OCR dependencies and may miss or misread scanned text. <br>
Mitigation: Install dependencies from trusted package managers and review extracted pages before relying on the results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hanw2039/split-pdf-by-pages) <br>
- [Tesseract OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local PDF files when the generated Python workflow is run by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
