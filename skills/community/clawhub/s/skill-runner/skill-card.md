## Description: <br>
Skill Runner invokes another installed OpenClaw skill from scheduled or indirect agentTurn messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xpneuma](https://clawhub.ai/user/xpneuma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to trigger a named installed skill from cron-style agentTurn messages when automation needs delegated skill execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates broad authority to another installed skill. <br>
Mitigation: Restrict the set of skills it can run and validate target skill names and paths before execution. <br>
Risk: Cron-style messages can trigger unintended skill execution if jobs are misconfigured. <br>
Mitigation: Review every cron job that invokes this skill and require the expected message format. <br>
Risk: The selected target skill receives the runner's available tools and session context. <br>
Mitigation: Run it in an isolated context with only the tools and session access required for the scheduled task. <br>


## Reference(s): <br>
- [Skill Runner on ClawHub](https://clawhub.ai/xpneuma/skill-runner) <br>
- [Publisher profile](https://clawhub.ai/user/xpneuma) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Delegated target skill output with a status object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output depends on the selected target skill; failures return status and reason fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
