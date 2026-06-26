## Description: <br>
Provides cross-platform desktop automation for mouse and keyboard control, screenshots, image utilities, overlay markers, OCR/template-based element locating, clipboard actions, and cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ikaros-521](https://clawhub.ai/user/Ikaros-521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect the screen, locate UI elements, annotate screenshots, and execute local desktop automation tasks through bundled Python scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Desktop automation can click, type, paste, or invoke hotkeys in the wrong active window. <br>
Mitigation: Confirm the target window and coordinates before running actions, use coordinate markers or screenshots first, and keep PyAutoGUI failsafe available. <br>
Risk: Screenshots, OCR, and clipboard operations can expose sensitive information. <br>
Mitigation: Avoid using screenshot, OCR, copy, paste, or copy_paste commands around secrets, and prefer region screenshots when full-screen capture is unnecessary. <br>
Risk: Cleanup commands can delete generated files when execution mode is enabled. <br>
Mitigation: Run cleanup in preview mode first and use --execute only after reviewing the files selected for deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ikaros-521/pyautogui) <br>
- [README.md](README.md) <br>
- [requirements.txt](references/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with Python command snippets, terminal text, JSON image metadata, and generated image or screenshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can affect the local desktop, clipboard, screenshots, OCR output, and cleanup of generated files.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
