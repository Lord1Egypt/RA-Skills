## Description: <br>
S2-SP-OS Spectrum Radar provides passive spatial perception from GPIO or UART mmWave modules with explicit consent and quantized biometric status output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and home-automation agents use this skill to read room occupancy, motion, distance, and quantized heart or breathing status from an S2-compatible mmWave radar sensor. The skill is intended to provide passive perception data for an agent to interpret, not to trigger devices or emergency workflows by itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes room occupancy and quantized heart or breathing status to a local agent. <br>
Mitigation: Install only with explicit consent, limit access to the generated sensor output, and avoid retaining more data than the agent needs. <br>
Risk: Examples describe follow-up actions involving lights, microphones, and emergency routines. <br>
Mitigation: Require human approval, clear consent, and false-positive handling before any agent uses radar output to trigger another device or workflow. <br>
Risk: Security evidence says the uploaded Python does not currently compile and appears simulated. <br>
Mitigation: Treat the release as a prototype until the Python client is fixed, reviewed, and tested against the intended hardware. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-spectrum-perception) <br>
- [S2-SP-OS homepage](https://space2.world/s2-sp-os) <br>
- [S2 Memzero Protocol](artifact/S2-MEMZERO-PROTOCOL.md) <br>
- [Edge Hardware Setup Guide](artifact/edge-setup-guide.md) <br>
- [Agent Reasoning Examples](artifact/AGENT-EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON sensor output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, pyserial, and S2_PRIVACY_CONSENT=1 before execution; UART mode also requires a serial port.] <br>

## Skill Version(s): <br>
2.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
