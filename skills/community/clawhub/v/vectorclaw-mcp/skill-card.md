## Description: <br>
MCP tools for Anki Vector: speech, motion, camera, sensors, and automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danmartinez78](https://clawhub.ai/user/danmartinez78) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw-compatible agents to an Anki or Digital Dream Labs Vector robot for speech, movement, camera capture, sensor reads, and automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent move and operate a physical Vector robot. <br>
Mitigation: Install it only for intentional robot-control use, keep the robot in a safe non-private area, and require explicit confirmation before movement or speech. <br>
Risk: Camera tools can capture images from the robot's environment. <br>
Mitigation: Use camera capture only with consent in appropriate spaces and require explicit confirmation before camera access. <br>
Risk: Robot serial and SDK certificate files are sensitive operational credentials. <br>
Mitigation: Protect VECTOR_SERIAL and SDK certificate files, and verify the external Python package before enabling the MCP server. <br>


## Reference(s): <br>
- [VectorClaw MCP on ClawHub](https://clawhub.ai/danmartinez78/vectorclaw-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Vector robot, Wire-Pod, the Vector SDK config file, and VECTOR_SERIAL.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
