## Description: <br>
Session Resume helps OpenClaw agents recover interrupted long-running tasks by reading a local checkpoint file, reporting saved progress, and waiting for user confirmation before continuing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill to preserve progress for multi-step tasks across gateway restarts, session interruptions, compaction, or network disconnects. The skill is intended to restore only explicitly saved task state and report pending work before execution resumes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The checkpoint file can contain sensitive task context such as API keys, passwords, private keys, customer data, or deployment details. <br>
Mitigation: Avoid writing secrets or sensitive deployment information to ~/.openclaw/workspace-main/.task-state.json, and review or delete the file after sensitive work, especially on shared machines. <br>
Risk: A stale checkpoint could cause the agent to resume work the user no longer wants. <br>
Mitigation: Report the saved task state first and wait for explicit user confirmation before continuing, then delete the checkpoint when the task is complete or abandoned. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wavmson/session-resume) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown recovery reports and JSON checkpoint state guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local .task-state.json checkpoint file and waits for user confirmation before resuming work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
