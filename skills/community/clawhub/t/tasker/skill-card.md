## Description:

Tasker provides a general workflow layer for task execution, debugging, implementation, analysis, review, planning, and user dissatisfaction handling in agent interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tealun](https://clawhub.ai/user/tealun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, analysts, and writing or review agents use Tasker to structure requests into goals, constraints, execution paths, confirmation gates, verification checks, and concise close-out reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad workflow guidance may activate for many request types and influence task planning, execution, review, and escalation behavior.

Mitigation: Review whether the broad auto-discovery scope fits the target agent and rely on Tasker's confirmation gates before file changes, operations actions, multi-agent handoff, or scheduled-task delegation.

Risk: The skill can propose shell commands, code changes, configuration edits, and handoff files that may affect external state when followed by an agent.

Mitigation: Require explicit confirmation for side-effecting work and verify resulting artifacts with post-tool checks before treating work as complete.

## Reference(s):

- [Tasker ClawHub listing](https://clawhub.ai/tealun/skills/tasker)
- [Optional PUA project](https://github.com/tanweai/pua)
- [SkillHub Tasker listing](https://skillhub.cloud.tencent.com/skills/tasker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or concise text, often with code blocks, command snippets, checklists, and artifact summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only workflow guidance with confirmation gates, retry limits, verification expectations, and risk disclosure.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
