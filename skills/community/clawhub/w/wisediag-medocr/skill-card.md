## Description: <br>
PDF and image OCR that converts a single PDF or image into Markdown via the WiseDiag cloud API with table recognition and multi-column layout support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wisediag](https://clawhub.ai/user/wisediag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to OCR a single PDF or image through WiseDiag and receive the extracted content as a local Markdown file. It is intended for non-sensitive documents unless WiseDiag's terms and data handling meet the user's requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are uploaded to WiseDiag's cloud OCR service for processing. <br>
Mitigation: Use the skill only for documents appropriate for WiseDiag's terms and data handling, and use an offline OCR workflow for confidential medical, financial, legal, credential, or minor-related documents. <br>
Risk: The WiseDiag API key can be exposed if persisted in shell startup files or shared logs. <br>
Mitigation: Prefer a session-only environment export or a secret manager, and avoid adding the API key to ~/.zshrc or ~/.bashrc on shared systems. <br>
Risk: Unpinned dependencies may resolve to different package versions over time. <br>
Mitigation: Install in a locked or otherwise patched environment and review dependency updates before deployment. <br>
Risk: Large or unsupported inputs may fail or produce incomplete OCR results. <br>
Mitigation: Process one supported PDF or image at a time, keep inputs within the documented size and page limits, and lower DPI when server timeouts occur. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wisediag/wisediag-medocr) <br>
- [WiseOCR project homepage](https://github.com/wisediag/WiseOCR) <br>
- [WiseDiag API key management](https://console.wisediag.com/apiKeyManage) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown output file with CLI commands and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes one PDF or image per command and saves one Markdown file locally, under ~/.openclaw/workspace/WiseOCR by default.] <br>

## Skill Version(s): <br>
1.0.26 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
