## Description: <br>
Complete software development workflow enforcing design → plan → execution with checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brothaakhee](https://clawhub.ai/user/brothaakhee) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use Superclaw to slow coding work into an explicit design, implementation plan, and checkpointed execution workflow. It is intended for software-building tasks where reviewable plans, workspace memory, and batch checkpoints reduce rushed or untracked changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read workspace memory and context while preparing software designs and plans. <br>
Mitigation: Install it only in workspaces where that context access is acceptable, and review generated designs before approval. <br>
Risk: The skill can write design, plan, and progress files and modify project files during implementation batches. <br>
Mitigation: Review checkpoint summaries and workspace diffs before continuing to later batches. <br>
Risk: The skill can spawn task agents for isolated implementation work. <br>
Mitigation: Use its batching and checkpoint process to inspect spawned-agent outputs before approving further execution. <br>


## Reference(s): <br>
- [Superclaw on ClawHub](https://clawhub.ai/brothaakhee/superclaw) <br>
- [Publisher Profile](https://clawhub.ai/user/brothaakhee) <br>
- [Superpowers methodology](https://github.com/obra/superpowers) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with saved design, plan, progress, code, command, and configuration artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workspace design and plan files, update progress logs, and propose or execute code changes through checkpointed batches.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
