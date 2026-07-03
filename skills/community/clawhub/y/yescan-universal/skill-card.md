## Description: <br>
This skill helps agents use the yescan CLI and Quark Scan service to process user-provided images for OCR, image translation, image enhancement, document conversion to Word, Excel, or PDF, and ID photo generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yescan-ai](https://clawhub.ai/user/yescan-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to process a user-selected image or image URL through Quark Scan for OCR, translation, cleanup, document conversion, or ID photo generation. It is not intended for video processing, pure text editing, or inputs that are not images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-selected images or image URLs and the SCAN_WEBSERVICE_KEY are sent to Quark Scan for processing. <br>
Mitigation: Use the skill only with authorization for the submitted documents, avoid regulated or confidential material unless permitted, and protect and rotate the API key as needed. <br>
Risk: Processed images or converted documents may remain in temporary output directories after execution. <br>
Mitigation: Use an explicit output directory when appropriate and clean up temporary files after processing sensitive material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yescan-ai/skills/yescan-universal) <br>
- [Quark Scan Open Platform](https://scan.quark.cn/business) <br>
- [Security Policy](SECURITY.md) <br>
- [Privacy, data flow, and key security](references/privacy.md) <br>
- [Implementation details](references/implementation.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance, CLI commands, JSON responses, OCR text, and local output file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write processed images or documents to a temporary directory or caller-specified output directory.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
