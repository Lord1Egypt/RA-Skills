## Description: <br>
Windows desktop automation skills for screenshot capture, OCR text extraction, and image-based UI element location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[civen-cn](https://clawhub.ai/user/civen-cn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to capture Windows screen content, extract text from images, and locate UI elements by image matching for desktop automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots and OCR may expose sensitive content visible on the user's desktop. <br>
Mitigation: Close or hide sensitive windows before capture, prefer region or window captures over full-screen captures, and choose screenshot output paths deliberately. <br>
Risk: Image-based UI matching may identify the wrong target and lead to unintended desktop actions when paired with clicks or automation. <br>
Mitigation: Confirm target matches, use confidence thresholds appropriate for the workflow, and review coordinates before any click or state-changing action. <br>


## Reference(s): <br>
- [Tesseract OCR Windows installer documentation](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may save screenshot image files and return OCR text or screen coordinates when used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
