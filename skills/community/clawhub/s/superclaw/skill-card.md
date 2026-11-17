## Description:

Complete software development workflow enforcing design → plan → execution with checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brothaakhee](https://clawhub.ai/user/brothaakhee)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use Superclaw to structure software work into design approval, implementation planning, and checkpointed execution. It is intended to slow direct coding when a task needs requirements clarification, plans, persistent progress notes, or batch review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delay direct coding by enforcing a strict design, planning, and checkpoint workflow.

Mitigation: Install it only for workspaces where that disciplined workflow is desired, and narrow activation if fast direct edits are expected.

Risk: The skill reads agent memory and profile files for context.

Mitigation: Review memory access expectations before use in workspaces with sensitive context.

Risk: The skill can spawn subagents and write persistent planning or progress logs.

Mitigation: Use a pinned, reviewed installer version and review generated plans, logs, and subagent activity before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brothaakhee/skills/superclaw)
- [Original Superpowers Framework](https://github.com/obra/superpowers)
- [OpenClaw Docs](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands and structured plan or progress documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce design documents, implementation plans, checkpoint summaries, and progress log entries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
