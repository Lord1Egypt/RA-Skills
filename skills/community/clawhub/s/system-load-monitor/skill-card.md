## Description: <br>
System Load Monitor helps agents check local CPU and memory usage, pause work when configured thresholds are exceeded, and resume after load recovers on constrained servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hifengzy](https://clawhub.ai/user/hifengzy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check local CPU and memory pressure before or during resource-intensive work, then pause, batch, or resume tasks based on the reported status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JSON status output may expose local process usernames and command lines. <br>
Mitigation: Keep checker output within the local environment unless the operator is comfortable sharing those process details. <br>
Risk: Alerting through Feishu or another external service can send operational details outside the environment. <br>
Mitigation: Require explicit approval before sending alerts to external services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hifengzy/system-load-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python code patterns, and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled checker can emit process usernames and command lines in JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
