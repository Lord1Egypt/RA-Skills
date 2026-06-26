## Description: <br>
Converts architecture diagrams into infrastructure as code or component code when the user provides a recognizable diagram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert architecture, flowchart, component, and network diagrams into Terraform, Kubernetes YAML, CloudFormation, workflow scripts, component code, or deployment configuration. The skill also returns a mapping from diagram nodes to generated resources and states assumptions for ambiguous input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated infrastructure or component code can include incorrect defaults or unsafe assumptions when a diagram omits security, scaling, networking, or dependency details. <br>
Mitigation: Review generated code and the diagram-to-resource mapping before deployment, and require explicit confirmation for security-sensitive settings. <br>
Risk: The skill may rely on sensitive credentials such as an API key for service configuration. <br>
Mitigation: Provide credentials only through environment variables or approved secret stores, and scope access to the task the user requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/wangjipeng-diagram-to-code) <br>
- [references/index.md](references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with fenced code blocks and diagram-to-code mapping] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated outputs should identify assumptions, validate the selected target format, and avoid hardcoded credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
