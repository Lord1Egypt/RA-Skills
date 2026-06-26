## Description: <br>
Sts2 Vision monitors Slay the Spire 2 combat by capturing the game window, using OCR to read combat values, tracking damage and DPS, and exporting combat reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ErebusCry](https://clawhub.ai/user/ErebusCry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and tool builders use this skill to monitor local Slay the Spire 2 gameplay, calibrate regions of interest, recognize HP and damage values, calculate DPS, and produce JSON combat reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill captures the local game window and may save screenshots or reports that include visible gameplay data. <br>
Mitigation: Run it only with the intended game window visible, keep sensitive windows or notifications out of the capture area, and review saved screenshots and reports before sharing. <br>
Risk: Some monitor modes collect mouse-click telemetry that is not clearly disclosed in the skill description. <br>
Mitigation: Prefer the main, simple, or local monitor modes unless click-based attribution is specifically needed. <br>
Risk: OCR and ROI calibration can produce incorrect combat values or DPS statistics. <br>
Mitigation: Use calibration mode and review generated reports before relying on the statistics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ErebusCry/sts2-vision) <br>
- [Publisher profile](https://clawhub.ai/user/ErebusCry) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Console status text, JSON combat reports, screenshot/image files for calibration, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are produced locally from captured game-window regions and ROI configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
