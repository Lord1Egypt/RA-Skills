## Description: <br>
Bounded recursive orchestration for complex tasks that are too large for one agent turn but cleanly decompose into a few independent subproblems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to plan, run, and merge bounded multi-agent work for complex research, audits, mixed research and synthesis, or coding projects that decompose into a few independent subproblems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local run folders, logs, notes, result files, and task-tree state that may contain sensitive task data. <br>
Mitigation: Use a dedicated run directory, review generated files before sharing them, and avoid processing private or third-party communications without authorization. <br>
Risk: Coding, worktree, external-message, installation, configuration-change, or destructive nodes can affect the user's workspace or external systems. <br>
Mitigation: Require human review and approval before those nodes proceed, and keep destructive or approval-sensitive work marked as waiting for approval. <br>
Risk: Recursive decomposition can create unnecessary child work or produce conflicting child results. <br>
Mitigation: Keep recursion bounded, use modest concurrency, and merge child outputs through an explicit synthesis or review step that surfaces disagreements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/plgonzalezrx8/recursive-swarm) <br>
- [Example run](references/example-run.md) <br>
- [Quiet child execution pattern](references/quiet-mode.md) <br>
- [Recursive swarm run tree schema](references/tree-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON run-state files and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local run folders, node specs, notes, result files, summaries, and append-only audit logs.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
