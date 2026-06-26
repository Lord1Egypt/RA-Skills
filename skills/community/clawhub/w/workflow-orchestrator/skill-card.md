## Description: <br>
Workflow Orchestrator helps build and run multi-agent workflows with DAG execution, branching, parallel execution, retries, fallback handling, and live monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to define, execute, and monitor DAG-based multi-agent workflows with conditional branches, fan-out/fan-in execution, retry behavior, fallbacks, and failure handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow publish or send steps can transmit pipeline outputs to an outbound destination. <br>
Mitigation: Before installing or running such workflows, confirm the destination, avoid sending secrets or sensitive scraped content, and prefer redaction or review before outbound delivery. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and JSON-like workflow status outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflow outputs can include per-step status, result payloads, errors, attempts, and duration fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
