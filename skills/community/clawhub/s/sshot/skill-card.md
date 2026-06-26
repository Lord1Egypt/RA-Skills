## Description: <br>
Take full screen screenshot using PowerShell. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alenzhu72](https://clawhub.ai/user/alenzhu72) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to trigger a full-screen screenshot on a controlled Windows node and receive the captured screenshot file path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill captures the full screen and may expose sensitive windows or information. <br>
Mitigation: Run it only on a Windows node you control and close or hide sensitive windows before using /sshot. <br>
Risk: The skill executes an unbundled local PowerShell script with ExecutionPolicy Bypass. <br>
Mitigation: Inspect the referenced sshot.ps1 file before installing or running the skill, and prefer a bundled script or a version that avoids ExecutionPolicy Bypass where possible. <br>
Risk: The skill provides little user control before full-screen capture. <br>
Mitigation: Use a version that asks for confirmation before capture when operating in shared or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alenzhu72/sshot) <br>
- [Publisher profile](https://clawhub.ai/user/alenzhu72) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text file path returned by stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on Windows and depends on a local PowerShell screenshot script outside the bundled artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
