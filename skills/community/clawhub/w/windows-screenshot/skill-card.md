## Description: <br>
Pure PowerShell GDI+ screenshot tool for Windows that captures the primary screen to a PNG file with automatic scaling and no external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vvxer](https://clawhub.ai/user/vvxer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture a local Windows desktop screenshot, save it as a PNG, and return the saved media path for follow-on workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots may capture sensitive information visible on the Windows desktop. <br>
Mitigation: Hide sensitive windows before running the skill, then review and delete saved PNG files from the configured media directory when they are no longer needed. <br>
Risk: A captured screenshot can be sent outside the local system if the user intentionally combines it with a messaging workflow. <br>
Mitigation: Use external sharing examples only with the intended recipient and credentials, and confirm the image contents before sending. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vvxer/windows-screenshot) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, files, guidance] <br>
**Output Format:** [PowerShell command guidance, MEDIA-prefixed text output, and PNG screenshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves screenshots under OPENCLAW_MEDIA_DIR when set, otherwise under the user's .openclaw media directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
