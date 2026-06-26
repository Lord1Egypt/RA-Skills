## Description: <br>
Use a lightweight spec + steering workflow for long, interruptible, multi-phase tasks that need checkpointed progress, recoverable state, and multi-session continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whisper1952717](https://clawhub.ai/user/whisper1952717) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage long-running, interruptible work through file-based specs, steering notes, checkpoints, and resumable handoffs across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps persistent task state and handoff notes in workspace files. <br>
Mitigation: Install it only when persistent planning state is desired, and review specs/active, specs/archive, and steering files for retained task context. <br>


## Reference(s): <br>
- [Skill Page](https://clawhub.ai/whisper1952717/spec-steering-workflow) <br>
- [ClawHub Homepage](https://clawhub.ai/skills?sort=downloads) <br>
- [Workflow Rules](references/workflow-rules.md) <br>
- [Checkpoint Rules](references/checkpoint-rules.md) <br>
- [Recovery Rules](references/recovery-rules.md) <br>
- [Integration Rules](references/integration-rules.md) <br>
- [Template Contracts](references/template-contracts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON workspace files with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates specs/active, specs/archive, and steering files when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
