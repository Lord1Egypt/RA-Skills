## Description: <br>
Control a Vector robot via Wirepod's local HTTP API on the same network for movement, head and lift control, speech, camera snapshots, audio playback, and patrol or explore routines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbeadle1](https://clawhub.ai/user/dbeadle1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to control a local Vector robot through Wirepod from the Pi or Wirepod host. It helps an agent issue movement, speech, camera, audio, patrol, and exploration commands while keeping control actions short and supervised. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move a physical Vector robot. <br>
Mitigation: Use short timed moves, supervise movement and patrol or explore routines, and release behavior control when a human needs manual control. <br>
Risk: The skill can save camera snapshots from the robot. <br>
Mitigation: Use camera capture only in trusted environments and handle saved image files according to the user's privacy expectations. <br>
Risk: The skill can play selected audio and process media files for playback. <br>
Mitigation: Avoid untrusted media files and keep Wirepod bound to localhost or a trusted private network. <br>


## Reference(s): <br>
- [Wirepod HTTP API](references/wirepod-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local camera snapshot files and audio conversion commands when the user requests those workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
