## Description: <br>
Control Anki Vector robot via wire-pod. Speak through Vector, see through its camera, move head/lift/wheels, change eye colors, trigger animations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bogorman](https://clawhub.ai/user/bogorman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and robot operators use this skill to control an Anki Vector robot through wire-pod for speech, camera snapshots, movement, settings, animations, and optional OpenClaw voice input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts include unsafe input handling when speech text is passed from untrusted sources. <br>
Mitigation: Review and patch vector-say.sh before passing untrusted text. <br>
Risk: The local proxy is unauthenticated and the optional LaunchAgent can keep it running persistently. <br>
Mitigation: Avoid the LaunchAgent unless an always-on proxy is required, bind the proxy to localhost, and add authentication before broader exposure. <br>
Risk: Proxy request and response files, logs, and camera snapshots can contain private data. <br>
Mitigation: Treat request.json, response.json, proxy logs, and camera snapshots as private data and clean them up when no longer needed. <br>
Risk: Robot behavior control disables cliff sensors during movement. <br>
Mitigation: Supervise wheel movement and keep the robot away from edges or unsafe surfaces. <br>


## Reference(s): <br>
- [wire-pod SDK API Reference](references/api.md) <br>
- [wire-pod](https://github.com/kercre123/wire-pod) <br>
- [Vector-Robot on ClawHub](https://clawhub.ai/bogorman/vector-robot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local request, response, log, and camera snapshot files when the proxy or helper scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
