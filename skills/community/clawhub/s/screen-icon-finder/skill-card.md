## Description: <br>
Finds target icons or small images in screenshots or pictures using multi-scale OpenCV template matching with deduplication, then reports, marks, or clicks matched locations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lieyingthh](https://clawhub.ai/user/lieyingthh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation agents use this skill to locate a user-provided icon or UI image in a screenshot, label the matches with coordinates and confidence scores, and optionally click a detected target. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full-screen capture can expose secrets, private messages, or sensitive application state visible on the desktop. <br>
Mitigation: Use the skill in a clean desktop session and keep secrets, sensitive chats, and unrelated applications off screen before allowing screenshot capture. <br>
Risk: Automated clicking may activate the wrong UI element if template matching is uncertain or the screen changes after detection. <br>
Mitigation: Review the marked output and confidence scores first, then require explicit approval before any click action. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples; the script returns console text and can write marked image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screen coordinates, confidence scores, annotated screenshots, and optional click actions.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
