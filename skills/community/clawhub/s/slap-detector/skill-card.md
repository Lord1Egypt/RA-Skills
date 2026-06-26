## Description: <br>
React to physical slaps and shakes detected on an Apple Silicon MacBook accelerometer. Use when the slap-your-openclaw MCP server is connected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinhong2011](https://clawhub.ai/user/sinhong2011) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to a local slap/shake detector, monitor physical impact events, review event history, and tune detector sensitivity on an Apple Silicon MacBook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required local MCP server is configured to run through sudo, giving the separate slap-your-openclaw process root privileges. <br>
Mitigation: Review and verify the slap-your-openclaw server before installation, install only from a trusted source, and confirm root access is necessary for the accelerometer integration. <br>
Risk: Low-severity ambient vibration or typing could be mistaken for intentional slap or shake events. <br>
Mitigation: Keep the default min_level at 4 for normal use and do not lower sensitivity below 3 unless the user explicitly asks. <br>
Risk: Long waits or repeated polling can make the agent appear stuck when the detector is warming up or arming. <br>
Mitigation: Use bounded waits of no more than 120 seconds and tell the user to wait when the detector reports Warmup or Arming. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sinhong2011/slap-detector) <br>
- [Publisher profile](https://clawhub.ai/user/sinhong2011) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown text with MCP tool calls and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses slap detector tool calls with bounded wait timeouts and a default minimum event level of 4.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
