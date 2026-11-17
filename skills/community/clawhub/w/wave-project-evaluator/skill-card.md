## Description:

Evaluates project delivery quality with a structured nine-dimension rubric, identifies concrete improvements, supports validation, and produces a project evaluation report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youxiyin](https://clawhub.ai/user/youxiyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project owners use this skill to assess project readiness, identify the lowest-scoring quality dimensions, plan one concrete improvement at a time, and generate a structured evaluation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may inspect a repository and propose or apply edits, create commits, revert changes, and save evaluation reports.

Mitigation: Use it only on repositories where those actions are acceptable, and require a clear preview before any write, commit, revert, or saved report.

## Reference(s):

- [Wave Project Evaluator release page](https://clawhub.ai/youxiyin/skills/wave-project-evaluator)
- [AgentLens methodology (arXiv:2605.12925)](https://arxiv.org/abs/2605.12925)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with scoring tables, improvement plans, validation notes, and optional shell commands or file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save project evaluation reports when the user approves that workflow.]

## Skill Version(s):

0.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
