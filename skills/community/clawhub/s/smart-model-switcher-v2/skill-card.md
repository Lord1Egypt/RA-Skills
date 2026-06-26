## Description: <br>
Smart Model Switcher V2 helps an agent classify multimodal, coding, reasoning, Office, and general tasks and choose an appropriate model for the active main session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route main-session tasks to suitable models based on attachments, task keywords, and Office-mode requests while leaving subagent sessions on preset models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic model selection can silently route prompts or attachments to a different provider. <br>
Mitigation: Enable the skill only when session-level provider switching is intentional, and review provider, privacy, cost, and data-handling expectations before use. <br>
Risk: Broad keyword triggers can select a model that does not match the user's intent. <br>
Mitigation: Review model-switch decisions in sensitive workflows and adjust or disable trigger-based switching when precision is required. <br>
Risk: The monitor script presents service-style status output that may overstate its operational behavior. <br>
Mitigation: Treat the bundled monitor script as a demo/status helper unless its runtime behavior has been independently verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/smart-model-switcher-v2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend session-level model/provider changes based on broad task triggers.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
