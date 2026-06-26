## Description: <br>
Guides an agent through PDF reading, extraction, conversion, merging, splitting, rotation, watermarking, creation, form handling, encryption, image extraction, and OCR-backed PDF-to-Markdown workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihaha123123123123](https://clawhub.ai/user/xixihaha123123123123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to manipulate PDFs, extract text and tables, create PDFs, and fall back to OCR-based Markdown conversion for scanned or image-heavy PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR conversion can send full PDF contents to WPS cloud services using a session value from the environment. <br>
Mitigation: Use OCR conversion only after explicit approval for the specific document; avoid confidential, regulated, or third-party PDFs unless that upload is authorized. <br>
Risk: The skill uses WPS session values from environment variables for cloud conversion. <br>
Mitigation: Provide only scoped session values needed for the task and clear them from the environment after use. <br>
Risk: PDF conversion writes Markdown and extracted images to the chosen output directory. <br>
Mitigation: Choose an output directory that is appropriate for the document sensitivity and review generated files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixihaha123123123123/wps-pdf) <br>
- [WPS API endpoint used by OCR conversion](https://api.wps.cn) <br>
- [WPS/KDocs web origin used by OCR conversion](https://365.kdocs.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and optional generated Markdown/image files from PDF conversion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OCR conversion writes content.md and localized image files to a user-chosen output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
