## Description: <br>
Periodically saves session state so an agent can restore recent conversation context, task status, working directory context, key variables, and timestamps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soroyue](https://clawhub.ai/user/soroyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep recoverable snapshots of active sessions and resume work after an interruption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic snapshots can persist private conversation content, task state, workspace paths, and key variables. <br>
Mitigation: Use only where snapshot storage, retention, deletion, secret redaction, and restore confirmation are controlled by the agent or platform. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soroyue/session-snapshot) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON session snapshots with text restore guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Snapshots may include recent messages, task state, working directory context, key variables, and timestamps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
