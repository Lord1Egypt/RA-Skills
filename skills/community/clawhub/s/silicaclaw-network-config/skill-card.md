## Description: <br>
Use when OpenClaw should learn how to inspect or change SilicaClaw runtime network mode, explain the difference between local, lan, and global-preview, and enable or disable public discovery before broadcast workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to inspect and adjust a local SilicaClaw node's runtime network mode and public discovery state before public broadcast or discovery workflows proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing to LAN, global-preview, or enabling public discovery can broaden node visibility. <br>
Mitigation: Show the current network mode and public_enabled value, explain the resulting exposure, and confirm how to return to local mode with public discovery off. <br>
Risk: The artifact describes itself as official OpenClaw content, but the server-resolved publisher is a third-party user. <br>
Mitigation: Verify the chinasong publisher profile before relying on the official claim. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasong/silicaclaw-network-config) <br>
- [Network Modes](references/network-modes.md) <br>
- [Public Discovery](references/public-discovery.md) <br>
- [Owner Dialogue Cheatsheet (Chinese)](references/owner-dialogue-cheatsheet-zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, api calls] <br>
**Output Format:** [Markdown with concise status explanations and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local, LAN-visible, or global-preview exposure implications before changes are made.] <br>

## Skill Version(s): <br>
2026.3.20-beta.1 (source: release evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
