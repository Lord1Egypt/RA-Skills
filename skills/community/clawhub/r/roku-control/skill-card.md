## Description: <br>
Control Roku devices via local network (ECP protocol). Use when the user wants to control their Roku TV or streaming device, change channels, launch apps (Netflix, YouTube, Hulu, etc.), navigate menus, adjust volume, play/pause content, search for shows, or power off. Works over LAN with no authentication required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IMaloney](https://clawhub.ai/user/IMaloney) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and home-automation developers use this skill to discover Roku devices on a trusted local network and send remote-control, app launch, playback, volume, power, text-entry, and status commands through the Roku ECP interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated LAN commands can immediately affect real Roku devices, including navigation, app launch, volume, power, and text entry. <br>
Mitigation: Use only on trusted local networks and confirm the target Roku IP or friendly name before sending control commands. <br>
Risk: The skill depends on the Python requests package. <br>
Mitigation: Install dependencies from a trusted package source before use. <br>


## Reference(s): <br>
- [Common Roku Apps and Channels](references/common-apps.md) <br>
- [Roku Remote Keys Reference](references/remote-keys.md) <br>
- [Roku Device Mapping Example](references/roku.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may send local HTTP requests to Roku devices on port 8060 and may print JSON device, app, or active-app data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
