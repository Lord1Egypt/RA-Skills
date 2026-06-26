## Description: <br>
Enforces task completion with explicit Goal/Progress/Next state, anti-stall rules, and evidence-based completion proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to keep multi-step tasks moving by recording goal, progress, next action, and completion evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Completion evidence or task logs may include secrets, sensitive paths, or private data if copied directly from a workspace. <br>
Mitigation: Keep evidence summaries free of secrets and use relative or workspace paths; run the privacy checklist before sharing artifacts. <br>
Risk: A completion process can encourage action on destructive, public, account-changing, or irreversible tasks without enough review. <br>
Mitigation: Require explicit user approval before those actions and record the approval as part of the task evidence. <br>


## Reference(s): <br>
- [Task Finish Contract on ClawHub](https://clawhub.ai/Dalomeve/task-finish-contract) <br>
- [Privacy Checklist](artifact/references/privacy-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with checklist blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes explicit task state, completion evidence, and follow-up actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
