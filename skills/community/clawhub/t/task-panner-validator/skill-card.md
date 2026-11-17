## Description:

Provides Python-native task planning, validation, approval, dry-run execution, persistence, and execution summaries for AI agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cerbug45](https://clawhub.ai/user/cerbug45)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to define multi-step workflows, validate plan structure and risky actions, require approval or dry-run checks, and execute steps through their own executor functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The approval, rollback, and integrity features can give false confidence if treated as a security boundary.

Mitigation: Treat the skill as a lightweight planning helper, keep auto_approve disabled for real operations, run dry_run first, and require executor-level allowlists and confirmations.

Risk: Loaded plans may preserve approval state and should not be trusted solely because their checksum verifies.

Mitigation: Revalidate loaded plans, require fresh approval for sensitive workflows, and avoid relying on persisted approval for destructive actions.

Risk: Rollback checkpoints record planner state but do not undo external side effects by themselves.

Mitigation: Use idempotent executors or explicit compensating actions, and do not rely on built-in rollback behavior for destructive work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cerbug45/skills/task-panner-validator)
- [README](artifact/README.md)
- [Quick Start Guide](artifact/QUICKSTART.md)
- [API Reference](artifact/API.md)
- [Examples](artifact/examples.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON plan data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure Python standard-library implementation; caller-provided executor functions perform real actions.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
