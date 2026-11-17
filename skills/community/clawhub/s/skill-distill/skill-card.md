## Description:

Skill Distill helps agents consolidate multiple overlapping skills into one distilled skill while preserving source traceability and requiring user confirmation for conflicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to merge overlapping skills, reduce routing ambiguity, and lower repeated context overhead. It guides collection, cross-analysis, conflict confirmation, generation, and validation of a distilled replacement skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phase 4 validation depends on external local Python tools from other installed skills.

Mitigation: Inspect and trust the referenced improvement-learner, improvement-orchestrator, and improvement-evaluator skill scripts before running their commands.

Risk: Generated distillation actions may replace, downgrade, or otherwise change installed skills without strong integrity checks.

Mitigation: Require explicit review and approval before applying generated files or any delete, replace, or downgrade operation.

## Reference(s):

- [Skill Distill release page](https://clawhub.ai/lanyasheng/skills/skill-distill)
- [README](artifact/README.md)
- [Distillation Decision and Checklist](artifact/references/distillation-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown plans, generated skill files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before generation and relies on local improvement pipeline tools for validation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
