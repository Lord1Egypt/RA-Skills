## Description: <br>
Evaluates OpenClaw trigger rules against the current database state, especially stale mission detection backed by public.openclaw_* tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EcosincronIA](https://clawhub.ai/user/EcosincronIA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw workflows use this skill to evaluate the stale_missions_alert trigger and inspect the corresponding trigger rule row against current database state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a hard-coded local OpenClaw engine script that is outside the packaged artifact. <br>
Mitigation: Install only in a controlled OpenClaw workspace and review stale_missions_engine.sh at the configured path before execution. <br>
Risk: The inspection command queries a local PostgreSQL container and can expose current trigger rule state. <br>
Mitigation: Use backed-up or non-critical data first and prefer narrowly scoped database credentials for inspection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EcosincronIA/trigger-evaluator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports evaluate and inspect commands for stale_missions_alert only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
