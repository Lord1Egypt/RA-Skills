## Description: <br>
Windows full-screen screenshot capture with automatic mouse-position marking and native OCR text recognition, running locally without network access or API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a770438678](https://clawhub.ai/user/a770438678) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill on Windows 10 or 11 to capture the current screen, mark the mouse position, and extract text from images with the Windows OCR engine. It is useful for local screen analysis and OCR workflows where screenshots and recognized text should remain on disk instead of being uploaded to an external service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The screenshot script captures the full screen and may save sensitive visible content to disk. <br>
Mitigation: Close or hide sensitive windows before use, review the fixed output folder, and delete screenshots that should not be retained. <br>
Risk: OCR results may contain sensitive text extracted from local images. <br>
Mitigation: Review and delete generated OCR text files when they are no longer needed. <br>
Risk: The scripts use fixed Windows paths for screenshot and OCR outputs. <br>
Mitigation: Confirm or edit the configured output paths before running the scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/a770438678/windows-screenshot-ocr) <br>
- [Publisher Profile](https://clawhub.ai/user/a770438678) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime scripts write PNG screenshots and TXT OCR results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Screenshots and OCR output are saved to a fixed local Windows folder unless the user edits the scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
