## Description: <br>
World Model - Environment understanding, causal reasoning, and prediction for AGI <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobisamaa](https://clawhub.ai/user/tobisamaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to model environment state, reason over cause-effect chains, predict action outcomes, and run what-if or risk simulations for AGI-oriented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package appears incomplete and may rely on a missing or later-added world_model.py implementation. <br>
Mitigation: Review the installed files before use and verify or remove any world_model.py implementation that is added outside the reviewed artifact. <br>
Risk: The skill asks for broad local state and prediction logs about user intent, agent goals, environment, and business context without clear privacy limits. <br>
Mitigation: Limit stored context to the minimum needed, inspect world-state and prediction-log files, and remove sensitive or unnecessary entries before operational use. <br>
Risk: The skill provides decision-support predictions and simulations that may be incomplete or misleading. <br>
Mitigation: Treat predictions, causal chains, and risk scores as advisory inputs and require human review before acting on consequential recommendations. <br>


## Reference(s): <br>
- [World Model on ClawHub](https://clawhub.ai/tobisamaa/world-model) <br>
- [Publisher profile: tobisamaa](https://clawhub.ai/user/tobisamaa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell examples, JSON state and model files, and Python wrapper code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or maintain local world-state, causal-model, and prediction-log JSON artifacts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
