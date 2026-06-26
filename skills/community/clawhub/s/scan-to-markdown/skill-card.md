## Description: <br>
Extracts text from scanned documents, photographed pages, handwritten notes, and images using OCR through the MinerU Open API CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract text from scanned PDFs, photographed documents, image files, and document URLs. It is suited for OCR workflows where the agent should propose or run MinerU CLI commands and return extracted text or Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents are uploaded to MinerU's cloud OCR service for processing. <br>
Mitigation: Avoid processing confidential legal, medical, financial, or business documents unless MinerU's privacy and retention practices meet the user's needs. <br>
Risk: The skill can process local file paths and URLs selected by the user. <br>
Mitigation: Confirm the exact file or URL before uploading it for OCR. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tanis90/scan-to-markdown) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU CLI download](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and extracted OCR text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process local files or document URLs through MinerU's cloud OCR service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
