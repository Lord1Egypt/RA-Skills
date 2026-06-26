## Description: <br>
Processes mmWave-style boundary scan data into an ego-centric 9-grid topology so embodied-AI agents can report spatial intrusions, material inferences, and collision context after movement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to add advisory boundary-scanning logic to embodied-AI agents, translating simulated or mmWave-derived readings into 9-grid spatial status and collision context after movement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Advisory perception output could be mistaken for a complete robotics safety system. <br>
Mitigation: Keep movement control, actuator authorization, sensor access, and safety interlocks in separate explicit components, as recommended by the security guidance. <br>
Risk: The bundled handler simulates mmWave readings when no hardware port is configured, so outputs may not reflect a real environment. <br>
Mitigation: Treat simulated readings as development data and require validated sensor integration before operational robot use. <br>


## Reference(s): <br>
- [S2-SWM V3 Ego-Centric Prediction Whitepaper](artifact/s2-swm-v3-ego-centric-prediction.md) <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/s2-boundary-scanner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/spacesq) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON tool response plus concise human-facing spatial status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports ego center, step displacement, eight peripheral grid states, material inference, intrusion percentage, and collision warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
