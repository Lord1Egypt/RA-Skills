## Description:

Engineering discipline for AI coding agents that helps agents make maintainable trade-off calls, respect hard safety limits, and verify implementation details before changing code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill while writing, refactoring, or reviewing maintainable code. It emphasizes bounded scope, contract awareness, verification, security basics, and test-backed delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to read task-relevant project files while performing coding work.

Mitigation: Install it only in intended workspaces and continue reviewing proposed file reads, edits, and command execution.

Risk: Quality guidance can still influence production code changes even though the artifact contains no executable components.

Mitigation: Keep normal code review, security scanning, and test gates in place before accepting generated changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wujiaming88/skills/sed-probe-delete-me-0707)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Natural-language guidance and Markdown checklists, with code or shell snippets when the coding task requires them.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable artifact is bundled; outputs depend on the active coding task.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
