## Description: <br>
Capture screenshots from a WSL2 environment by invoking Windows PowerShell to capture the Windows primary screen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxuanyuan](https://clawhub.ai/user/wxuanyuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators working in WSL use this skill to capture the Windows primary screen and optionally attach the resulting PNG in a message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A screenshot can include passwords, private documents, notifications, or other sensitive information visible on the Windows primary screen. <br>
Mitigation: Review each screenshot before sharing or attaching it to a message. <br>
Risk: The screenshot script uses a hard-coded Windows Pictures path for one Windows profile. <br>
Mitigation: Update the configured Windows path before use if the local Windows profile or destination directory differs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wxuanyuan/wsl-screenshot) <br>
- [Screenshot script](artifact/scripts/screenshot.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and filesystem paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces timestamped PNG screenshots under the configured Windows Pictures directory when executed.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
