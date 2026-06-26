## Description: <br>
Sets one-time temporary heartbeat tasks that execute reminders, checks, or actions at a specified time and are deleted after completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to schedule one-time reminders, checks, or low-impact tasks, then list or cancel pending temporary heartbeats without creating permanent HEARTBEAT.md entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Free-form scheduled task text may later trigger actions without fresh user confirmation. <br>
Mitigation: Use the skill for reminders or low-impact read-only checks, and require fresh confirmation before any destructive, public, financial, or account-changing action runs. <br>
Risk: Temporary task records can contain sensitive personal details or secrets. <br>
Mitigation: Avoid placing secrets, credentials, or sensitive personal information in scheduled task content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rfdiosuao/temp-heartbeat) <br>
- [Publisher Profile](https://clawhub.ai/user/rfdiosuao) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown task confirmations, lists, cancellation messages, and execution result summaries with inline command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and delete temporary task files under memory/temp-heartbeat-*.md when followed by an agent with file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
