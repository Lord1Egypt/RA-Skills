## Description: <br>
Detects elder falls and apnea using privacy-safe 60/77 GHz mmWave radar with real-time micro-Doppler STFT analysis for emergency alerts and response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Care technology developers and integrators use this skill to evaluate privacy-preserving elder fall monitoring with mmWave DSP and optional Home Assistant emergency routing. It is intended for environments where safety controls and independent validation are applied before any physical actuation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enabling real actuation can automatically control smart-home devices, including door unlocking, without enough scoping or confirmation. <br>
Mitigation: Keep dry-run mode enabled for testing; before enabling real actuation, restrict the Home Assistant token, verify the base URL is a trusted local endpoint, and add human confirmation or remove automatic door unlocking. <br>
Risk: Life-safety decisions based on simulated DSP behavior may be unreliable without independent validation. <br>
Mitigation: Treat the skill as a prototype until validated with the target radar hardware, deployment environment, and emergency response workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-eldercare-mmwave-monitor) <br>
- [Project homepage](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and runtime console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python dependencies and optional Home Assistant environment variables for real actuation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
