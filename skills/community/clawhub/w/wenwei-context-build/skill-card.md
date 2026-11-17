## Description:

This skill helps agents trace code recursively from a selected entry file and produce structured, implementation-focused code knowledge base documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wed840313](https://clawhub.ai/user/wed840313)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze frontend, backend, or full-stack modules from an entry file and generate structured implementation notes for AI-assisted code understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated documentation may expose source implementation details.

Mitigation: Use the skill only on repositories where code inspection and summarization are acceptable, and review generated Markdown before sharing it outside the team.

Risk: Cross-workspace dependencies can be incomplete or unavailable during analysis.

Mitigation: Pause for user confirmation when related code is outside the current workspace and clearly mark unavailable links instead of inventing missing code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wed840313/skills/wenwei-context-build)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with tables and fenced code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes precise file paths, function names or line numbers, call chains, and concise code snippets; writes a .md file only when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
