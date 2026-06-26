## Description: <br>
Routes agent tasks through a dual-system ReAct orchestrator that switches between fast execution and deeper Reflexion-based reasoning while managing registered tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add ReAct-style task routing, tool selection, execution history, and optional human approval or code-mode flows to JavaScript agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Code Mode can execute generated JavaScript or PowerShell with broad local access. <br>
Mitigation: Keep Code Mode disabled or limited to trusted templates unless sandboxing, allowlists, path restrictions, environment filtering, logging, and explicit user approval are configured. <br>
Risk: Registered file, shell, network, credential-using, or PowerShell tools can perform sensitive actions if exposed to autonomous planning. <br>
Mitigation: Register only least-privilege tools, require human approval for high-impact operations, and enforce timeouts and audit logging. <br>
Risk: Reasoning and parameter extraction are partly heuristic in the current artifact, so tool choice or arguments can be wrong. <br>
Mitigation: Validate generated actions and parameters before execution, especially for write, network, financial, or operational tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/yuyonghao-react-orchestrator) <br>
- [ReAct paper](https://arxiv.org/abs/2210.03629) <br>
- [Reflexion paper](https://arxiv.org/abs/2303.11366) <br>
- [README.md](artifact/README.md) <br>
- [USAGE-GUIDE.md](artifact/USAGE-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and structured execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces answers, execution history, selected mode, iteration count, duration, and optional approval or code execution results depending on registered tools.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
