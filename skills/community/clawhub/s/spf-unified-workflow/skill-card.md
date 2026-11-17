## Description:

Unified AI workflow with persistent memory, TDD execution, and 15 productivity skills. Use when starting any coding project or when you need planning, execution, debugging, or code review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mok888](https://clawhub.ai/user/mok888)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill bundle to plan, execute, debug, review, and complete coding work through persistent project files, TDD checkpoints, and coordinated subagent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle can strongly steer an agent's coding workflow through broad mandatory activation rules.

Mitigation: Review the workflow instructions before installation and disable or narrow mandatory activation rules for projects that require lighter guidance.

Risk: Session catchup can expose prior IDE conversation history into the current session.

Mitigation: Disable or modify session-catchup before use on sensitive projects, shared machines, or environments with confidential conversation history.

Risk: The workflow can create persistent planning files, run local hooks, spawn subagents where available, and guide code execution.

Mitigation: Install only in trusted workspaces, review generated plans before execution, and keep human approval gates for code changes and shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mok888/skills/spf-unified-workflow)
- [Artifact README](artifact/README.md)
- [Top-level skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local planning files under .superpower-with-files and may invoke local hooks when installed in a supported agent environment.]

## Skill Version(s):

2.20.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
