## Description: <br>
Use when you have a written implementation plan to execute in a separate session with review checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mok888](https://clawhub.ai/user/mok888) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to execute a written implementation plan in batches, run specified verifications, report progress at review checkpoints, and stop when blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive local code changes and workflow-state edits while executing implementation plans. <br>
Mitigation: Use a clean branch or worktree, review the plan and referenced workflow skills before execution, and inspect generated code and local state-file updates before relying on them. <br>
Risk: Parallel delegation or checkpoint updates could proceed beyond the user's intended scope if not reviewed. <br>
Mitigation: Require explicit approval before sub-agent delegation and review progress, findings, and handoff files at each checkpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mok888/spf-exec-plan) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown guidance with task status updates, verification notes, and implementation outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local workflow files such as progress, findings, and handoff notes when following the skill workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
