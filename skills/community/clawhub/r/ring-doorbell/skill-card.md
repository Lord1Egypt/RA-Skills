## Description: <br>
Control and monitor Ring doorbells and cameras by listing devices, capturing snapshots, and viewing recent doorbell or motion events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlmoment](https://clawhub.ai/user/zlmoment) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an assistant authenticate with their Ring account, list Ring devices, inspect recent motion or doorbell events, and capture camera snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Ring credentials and authentication tokens. <br>
Mitigation: Install and run it only on a trusted machine, protect ~/.openclaw/ring_token.json, and delete the token file when access is no longer needed. <br>
Risk: Camera snapshots and event-derived images can contain private household or visitor information. <br>
Mitigation: Review who can access ~/.openclaw/media/ring/ and periodically remove images that are no longer needed. <br>
Risk: The authentication flow asks for Ring credentials and 2FA codes. <br>
Mitigation: Use the auth command only when you intentionally want the assistant environment to access Ring devices and event history. <br>


## Reference(s): <br>
- [Ring Doorbell & Camera on ClawHub](https://clawhub.ai/zlmoment/ring-doorbell) <br>
- [python-ring-doorbell library](https://github.com/tchellomello/python-ring-doorbell) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command output, and saved image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save Ring authentication tokens under ~/.openclaw/ring_token.json and camera images under ~/.openclaw/media/ring/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
