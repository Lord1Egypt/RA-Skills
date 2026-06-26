## Description: <br>
Seamless Restart defines an OpenClaw gateway restart protocol that saves current state, notifies the user, schedules recovery, and resumes work after intentional restarts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zihaofeng2001](https://clawhub.ai/user/zihaofeng2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent must intentionally restart or reconfigure the OpenClaw gateway while preserving task context and notifying the user when service resumes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to restart or reconfigure the OpenClaw gateway with broad authority. <br>
Mitigation: Require explicit user approval before every gateway restart or config.patch action, and review configuration changes before applying them. <br>
Risk: NOW.md may contain stale, excessive, or untrusted recovery notes after a restart. <br>
Mitigation: Keep NOW.md minimal, clear post-restart actions after recovery, and treat the file as recovery context rather than authoritative instructions. <br>
Risk: Adding the suggested persistent rule may cause future agents to enforce this workflow automatically. <br>
Mitigation: Add the AGENTS.md or User Rules entry only when the workspace owner wants this restart workflow enforced for future sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zihaofeng2001/seamless-restart) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline command examples and a NOW.md state snapshot template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces restart steps, notification and cron command examples, and recovery notes; it does not execute the restart by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
