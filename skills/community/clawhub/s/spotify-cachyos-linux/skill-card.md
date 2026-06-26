## Description: <br>
Control the Spotify Linux desktop client via MPRIS DBus for playback, launching, volume, track information, and opening Spotify URIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxp731](https://clawhub.ai/user/lxp731) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Linux desktop users and agents use this skill to launch and control the Spotify desktop client through DBus, including playback, volume, track metadata, and Spotify URI playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start Spotify playback immediately, change playback state, and adjust volume on the user's Linux desktop. <br>
Mitigation: Use it only on a desktop session where Spotify control is intended, confirm Spotify URIs and volume changes before execution, and pause playback when the task is complete. <br>
Risk: Spotify may remain running after the agent task ends because the launch workflow detaches the Spotify process. <br>
Mitigation: Close Spotify manually or stop the Spotify process after use when persistent playback or a background app is not desired. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target the local Linux desktop session and Spotify MPRIS DBus interface.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
