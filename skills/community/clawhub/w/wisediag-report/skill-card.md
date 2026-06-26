## Description: <br>
WiseDiag-Report interprets medical report images or PDFs from local uploads or image URLs using AI-powered OCR, abnormal-indicator detection, and health-advice generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wisediag](https://clawhub.ai/user/wisediag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit medical report images or PDFs to WiseDiag for OCR-backed interpretation, abnormal indicator summaries, and health guidance. It is intended for reference only and not for diagnosis or treatment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical reports, image URLs, and questions are sent to WiseDiag's cloud service for analysis. <br>
Mitigation: Use the skill only when the user accepts that remote processing, remove personal identifiers where possible, and avoid submitting records that should not leave the user's environment. <br>
Risk: Saved Markdown reports may contain sensitive health information. <br>
Mitigation: Treat generated report files as sensitive health records and store, share, or delete them according to the user's privacy requirements. <br>
Risk: The required WiseDiag API key is a sensitive credential. <br>
Mitigation: Set WISEDIAG_API_KEY through a temporary environment variable or secret manager instead of committing it or placing it directly in shared shell startup files. <br>
Risk: The generated interpretation is AI-assisted guidance and may be incomplete or incorrect for medical decisions. <br>
Mitigation: Present results as reference material only and direct users to a qualified healthcare professional for diagnosis or treatment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wisediag/wisediag-report) <br>
- [WiseDiag API key console](https://console.wisediag.com/apiKeyManage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Streaming terminal text plus a saved Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WISEDIAG_API_KEY; accepts up to 5 local files or image URLs per request; saves a .md result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
