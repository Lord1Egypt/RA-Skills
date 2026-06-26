## Description: <br>
Task Watchdog manages external task lock files and timeout monitoring for OpenClaw agents, keeping task status outside the agent context and using heartbeat and grace-period checks rather than immediate alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, update, inspect, archive, and report OpenClaw task locks so interrupted or stalled tasks can be identified and resumed or cleaned up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell scripts can reassign, update, archive, or delete local task records with weak ownership checks. <br>
Mitigation: Review scripts before installation, use the skill only in trusted local environments, and add explicit caller identity checks before enabling shared or automated use. <br>
Risk: Heartbeat and cleanup automation can change task state without interactive review. <br>
Mitigation: Run scheduled scans conservatively, consider dry-run cleanup, and verify grace-period behavior before enabling cron automation. <br>
Risk: Agent and task identifiers are used in local file paths and task records. <br>
Mitigation: Apply stricter agent and task ID validation and atomic locking before using the scripts in a shared multi-agent workspace. <br>


## Reference(s): <br>
- [Task Watchdog detailed specification](references/spec.md) <br>
- [ClawHub release page](https://clawhub.ai/axelhu/task-watchdog-axel) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON lock-file records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local task lock files under the OpenClaw agent state directory and can be scheduled with cron.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
