## Description: <br>
skelm helps developers author, run, and operate typed TypeScript pipelines that combine deterministic code, LLM calls, and agent loops under a default-deny permission model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottgl9](https://clawhub.ai/user/scottgl9) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold, author, inspect, schedule, debug, and operate skelm workflow pipelines. It is also useful when configuring agent permissions, MCP wiring, backend setup, gateway operation, and migrations from other workflow tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: skelm workflows and agent steps may require sensitive credentials or inherited environment variables. <br>
Mitigation: Install only for intended skelm workflow use, avoid broad secrets in inherited environments, and grant only the specific secrets each workflow or agent step needs. <br>
Risk: Gateway exposure can broaden access to workflow execution, scheduling, approvals, audit data, and agent capabilities. <br>
Mitigation: Keep the gateway bound to localhost unless bearer authentication and network controls are configured. <br>
Risk: Agent filesystem, command, MCP, network, and secret permissions can enable privileged actions when configured too broadly. <br>
Mitigation: Use least-privilege permissions for each workflow, profile, and agent step, and review generated pipeline changes before running them. <br>


## Reference(s): <br>
- [skelm documentation](https://scottgl9.github.io/skelm/) <br>
- [skelm npm package](https://www.npmjs.com/package/skelm) <br>
- [ClawHub skill page](https://clawhub.ai/scottgl9/skelm) <br>
- [Pipeline Authoring Reference](artifact/references/pipeline-authoring.md) <br>
- [Agent step reference](artifact/references/agent-step.md) <br>
- [Permissions Reference](artifact/references/permissions.md) <br>
- [Config reference](artifact/references/config.md) <br>
- [Gateway Reference](artifact/references/gateway.md) <br>
- [CLI Reference](artifact/references/cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May scaffold TypeScript pipeline files and skelm configuration from bundled templates when requested.] <br>

## Skill Version(s): <br>
0.4.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
