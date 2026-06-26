## Description: <br>
Build, modify, or troubleshoot Sentio projects across processors, Sentio SQL in Data Studio, alerting, and dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sentioxyz](https://clawhub.ai/user/sentioxyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage Sentio projects, run SQL and data queries, configure alerts and endpoints, work with dashboards, inspect processors, retrieve price data, and run transaction simulations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on real Sentio projects using account credentials. <br>
Mitigation: Use a least-privilege Sentio credential and avoid pasting secrets into chat or shared terminals. <br>
Risk: Generated commands may delete, import, pause, stop, or otherwise change Sentio resources. <br>
Mitigation: Require explicit user confirmation before destructive or state-changing operations, imports, simulations, account linking, or AI-generated query execution. <br>
Risk: Using the latest CLI version can change behavior over time. <br>
Mitigation: Pin the Sentio CLI version for sensitive or repeatable workflows. <br>


## Reference(s): <br>
- [Sentio API OpenAPI specification](references/openapi.swagger.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Sentio CLI commands and JSON or YAML payloads for project, alert, endpoint, dashboard, processor, price, and simulation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
