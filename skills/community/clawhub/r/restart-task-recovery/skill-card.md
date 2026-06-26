## Description: <br>
Preserve and resume in-progress multi-agent work across OpenClaw config patch/apply restarts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SwiftKing100](https://clawhub.ai/user/SwiftKing100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve active task state before OpenClaw restarts, generate concise checkpoint and resume payloads, and recover interrupted sessions with risk-gated manual confirmation for higher-risk actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local checkpoints can contain recent task context from active sessions. <br>
Mitigation: Keep checkpoint content concise, store it locally, and review checkpoint files before sharing or retaining them beyond the recovery window. <br>
Risk: Recovery messages may resume work that publishes, deploys, deletes, transfers, or otherwise modifies external state. <br>
Mitigation: Review generated recovery JSON before sending and require manual confirmation for held high-risk resume actions. <br>
Risk: Retrying an interrupted session can duplicate non-idempotent work. <br>
Mitigation: Verify current state before continuing uncertain work and use the skill's high-risk hold gate for messages that mention retrying or writing. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [ClawHub release page](https://clawhub.ai/SwiftKing100/restart-task-recovery) <br>
- [Publisher profile](https://clawhub.ai/user/SwiftKing100) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline bash commands and JSON recovery payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local checkpoint files, resume-plan JSON, verified recovery JSON, and execution-plan JSON for agent session recovery.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
