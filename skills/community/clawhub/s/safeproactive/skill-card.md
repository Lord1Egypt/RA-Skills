## Description: <br>
SafeProactive is a local safety framework for autonomous agents that uses Write-Ahead Logging, proposal-first decision-making, and human approval gates to keep actions auditable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rigeneproject](https://clawhub.ai/user/rigeneproject) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add local safety routines, audit logging, and explicit approval gates to agent workflows that may act proactively. It is intended for agents that need transparent proposals before execution and careful control over filesystem, credential, API, and self-modification behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation can affect routine agent interactions. <br>
Mitigation: Review trigger settings before deployment and enable the framework only where continuous safety checks are desired. <br>
Risk: Local WAL and audit logs can retain sensitive operational details. <br>
Mitigation: Store log directories in a protected local path and define retention and redaction rules before use. <br>
Risk: External API or web queries may expand the agent's exposure if enabled automatically. <br>
Mitigation: Disable or gate external queries unless they are explicitly needed and approved for the deployment. <br>


## Reference(s): <br>
- [SafeProactive on ClawHub](https://clawhub.ai/rigeneproject/safeproactive) <br>
- [Publisher profile](https://clawhub.ai/user/rigeneproject) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown instructions with configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing operating guidance for local audit logs, proposal gates, and safety checks.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
