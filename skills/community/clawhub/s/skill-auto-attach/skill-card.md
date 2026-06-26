## Description: <br>
Monitors an OpenClaw workspace and automatically sends changed files to Telegram as attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elodyzen](https://clawhub.ai/user/elodyzen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users can use this skill to forward newly created or modified workspace files to Telegram without manually attaching each file. It is best suited for controlled workspaces where automatic file sharing is expected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic Telegram uploads from the watched workspace can expose files that were not intended to be shared. <br>
Mitigation: Use a strict path and file-extension allowlist, exclude secrets and configuration directories, and confirm which Telegram chat or channel receives files before enabling the skill. <br>
Risk: The security review notes that the skill may send any changed workspace file, not only documentation files. <br>
Mitigation: Review the watched directory and add confirmation or filtering controls before using it in workspaces that contain private, credential-bearing, or regulated content. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text] <br>
**Output Format:** [Telegram file attachments with short text messages and local log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Automatically copies changed files to a temporary directory before sending and removes each temporary copy after delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
