## Description:

将PDF中包含 显示日期 的页面切割成单独的文件，新文件以原文件名_页数命名。当用户需要从PDF中提取包含特定日期标识的页面时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanw2039](https://clawhub.ai/user/hanw2039)

### License/Terms of Use:

MIT-0

## Use Case:

External users and document-processing teams use this skill to generate Python code and command-line guidance for extracting PDF pages that contain the keyword "显示日期". It supports single-file and directory batch workflows, with optional OCR for scanned PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts install and use PDF/OCR dependencies.

Mitigation: Install dependencies only from trusted package sources, preferably inside a virtual environment.

Risk: Generated scripts process local PDFs and may write sensitive document pages to an output directory.

Mitigation: Run the script only on PDFs and directories you choose, and use a private output folder for sensitive documents.

Risk: Output files can overwrite existing files with the same generated names.

Mitigation: Check the output directory before running the script or choose a fresh destination folder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanw2039/skills/split-pdf-by-pages)
- [UB Mannheim Tesseract OCR installer wiki](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PDF-processing implementation guidance; generated scripts may write output PDF files and can overwrite existing files with matching names.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
