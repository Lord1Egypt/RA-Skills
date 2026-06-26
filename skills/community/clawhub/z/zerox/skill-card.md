## Description: <br>
Convert documents (PDF, DOCX, PPTX, images, etc.) to Markdown using the zerox library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otacu](https://clawhub.ai/user/otacu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other document-processing users use this skill to convert PDFs, DOCX, PPTX, and image files into Markdown, including scanned documents that require OCR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background mode has an unsafe macOS notification path that could execute unintended AppleScript from a crafted filename. <br>
Mitigation: Use foreground conversion where possible, and avoid background mode for untrusted or unusual filenames until the notification handling is fixed. <br>
Risk: Document contents are sent to the configured AI/APIYI provider during conversion. <br>
Mitigation: Convert only documents that are approved for that provider, and use a scoped API key if available. <br>
Risk: The README describes manually patching the installed zerox endpoint in node_modules. <br>
Mitigation: Review the endpoint change before installation and keep dependency changes auditable. <br>


## Reference(s): <br>
- [Zerox Skill on ClawHub](https://clawhub.ai/otacu/zerox) <br>
- [zerox library homepage](https://github.com/getomni-ai/zerox) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance, Files] <br>
**Output Format:** [Markdown files with terminal status and log text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and APIYI_API_KEY; accepts an input document path and optional Markdown output path; background mode writes a conversion log.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
