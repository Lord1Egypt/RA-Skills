## Description: <br>
Remove password protection from encrypted PDFs via the PDFAPIHub cloud API. Your PDF and password are sent to pdfapihub.com for decryption. Requires a CLIENT-API-KEY header. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to unlock password-protected PDFs they own or are authorized to process before downstream workflows such as printing, OCR, extraction, merging, or parsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF files, document passwords, and the API key are sent to PDFAPIHub for cloud processing. <br>
Mitigation: Use the skill only when third-party processing is acceptable, avoid highly sensitive documents, and follow the PDFAPIHub handling and retention terms. <br>
Risk: Passwords or API keys could be exposed if copied into configs, logs, prompts, or source control. <br>
Mitigation: Treat example credentials as placeholders, keep real secrets out of persisted files and logs, and rotate any credential that may have been exposed. <br>
Risk: The skill can remove protection from PDFs, which may be inappropriate without document ownership or authorization. <br>
Mitigation: Use it only for PDFs the user owns or has explicit permission to unlock. <br>


## Reference(s): <br>
- [PDFAPIHub documentation](https://pdfapihub.com/docs) <br>
- [PDFAPIHub](https://pdfapihub.com) <br>
- [Unlock PDF on ClawHub](https://clawhub.ai/rishabhdugar/unlock-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The PDFAPIHub response can return an unlocked PDF as a file, URL, or base64 payload depending on the requested output mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
