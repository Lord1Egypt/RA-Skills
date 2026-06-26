## Description: <br>
Switch between AI models dynamically to optimize costs and performance. Use when the user says mode commands like "eco mode", "balanced mode", "smart mode", or "max mode", or when they want to check their current mode with "/modes status" or configure modes with "/modes setup". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[serudda](https://clawhub.ai/user/serudda) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to set up, check, and switch among named model modes so they can choose lower-cost or higher-capability models for different tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change OpenClaw's default model, which may affect later sessions, behavior, and cost. <br>
Mitigation: Use explicit mode phrases, check the active mode with /modes status after switching, and review the configured model before high-cost SMART or MAX usage. <br>
Risk: Short standalone words such as eco, smart, or max may be interpreted as mode switch requests. <br>
Mitigation: Confirm ambiguous standalone requests before editing configuration, especially when the requested mode would increase cost or capability. <br>
Risk: Invalid or unavailable model IDs can prevent the intended mode from working. <br>
Mitigation: Run /modes setup, verify model IDs and provider access, and preserve existing OpenClaw settings when updating only the model field. <br>


## Reference(s): <br>
- [Switch Modes Reference Guide](REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local OpenClaw model configuration when the agent executes the skill instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
