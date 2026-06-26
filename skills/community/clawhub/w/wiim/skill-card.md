## Description: <br>
Control WiiM audio devices (play, pause, stop, next, prev, volume, mute, play URLs, presets). Use when the user wants to control music playback, adjust volume, discover WiiM/LinkPlay speakers on the network, or play audio from a URL on a WiiM device. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geodeterra](https://clawhub.ai/user/geodeterra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and audio-device users use this skill to discover and control WiiM or LinkPlay speakers on a local network through the wiim-cli command-line tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the external wiim-cli package for device control. <br>
Mitigation: Install the package only from a source the user trusts before following the generated commands. <br>
Risk: On networks with more than one WiiM or LinkPlay device, commands may target an unintended speaker if discovery chooses the wrong device. <br>
Mitigation: Use the --host option when the user wants to control a specific speaker. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is oriented around local-network device control using the external wiim-cli package.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
