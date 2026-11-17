## Description:

Use when executing implementation plans with independent tasks - coordinates task execution by dispatching subagents per task with verification checkpoints, adapted for OpenClaw's isolated session model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to execute implementation plans by dispatching one-shot subagents for independent tasks, then applying specification and code-quality review checkpoints before moving on.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegating implementation work to subagents may result in code changes, tests, and commits being proposed or made during a workflow.

Mitigation: Review the implementation plan, branch state, subagent outputs, tests, and commits before accepting or releasing changes.

Risk: The primary workflow instructions are written in Chinese and include OpenClaw-specific terminology.

Mitigation: Use with agents or operators who can accurately follow the Chinese-language workflow and confirm OpenClaw session behavior before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/superpowers-subagent-dev)

## Skill Output:

**Output Type(s):** [guidance, text, shell commands, code]

**Output Format:** [Markdown guidance with inline command examples and review checkpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in code changes, tests, and commits when followed by an agent.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
