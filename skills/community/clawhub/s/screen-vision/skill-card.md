## Description: <br>
macOS screen OCR and click automation via Apple Vision and ScreenCaptureKit, enabling an agent to capture windows or screen regions, extract text with coordinates, find text, and click visible text from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyun1024](https://clawhub.ai/user/jackyun1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use Screen Vision to inspect visible macOS screen text, wait for UI states, and click visible text during terminal-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can install remote tools before the skill runs. <br>
Mitigation: Install only from a trusted publisher and review or run setup manually before enabling the skill. <br>
Risk: The skill can read visible screen text, including sensitive information shown on screen. <br>
Mitigation: Prefer app or region filters instead of full-screen OCR and avoid using it while sensitive content is visible. <br>
Risk: The tap command can click UI elements that submit, purchase, delete, or change data. <br>
Mitigation: Manually approve tap actions that could have external, destructive, or account-changing effects. <br>


## Reference(s): <br>
- [Screen Vision homepage](https://github.com/jackyun1024/mac-screen-vision) <br>
- [ClawHub skill page](https://clawhub.ai/jackyun1024/screen-vision) <br>
- [Publisher profile](https://clawhub.ai/user/jackyun1024) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; command results may be JSON or human-readable text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS 14.0 or newer and Screen Recording permission for OCR and click automation.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
