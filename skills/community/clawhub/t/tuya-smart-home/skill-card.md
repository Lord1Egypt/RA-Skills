## Description: <br>
Control Tuya/Smart Life smart home devices including pet feeders, lights, plugs, curtains via cloud API or local network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachelchoo1212](https://clawhub.ai/user/rachelchoo1212) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and smart-home operators use this skill to discover, query, and control Tuya or Smart Life devices through Tuya cloud APIs or local network commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change the state of real smart-home devices, including feeders, plugs, lights, curtains, and similar equipment. <br>
Mitigation: Require explicit user confirmation before any command that changes device state, especially feeding, plug switching, curtain movement, or reset-like actions. <br>
Risk: Tuya access secrets and local keys are sensitive credentials. <br>
Mitigation: Keep credentials out of chat logs, shell history, and shared files; pass them only through secure runtime inputs. <br>
Risk: Local scanning can reveal devices on a network. <br>
Mitigation: Run local scans only on networks the user owns or is authorized to administer. <br>


## Reference(s): <br>
- [Tuya Smart Home API Reference](references/tuya_api.md) <br>
- [Tuya IoT Platform](https://iot.tuya.com) <br>
- [ClawHub Release Page](https://clawhub.ai/rachelchoo1212/tuya-smart-home) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; scripts emit text or JSON status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform Tuya cloud API calls or local-network device commands when the user supplies credentials and device identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
