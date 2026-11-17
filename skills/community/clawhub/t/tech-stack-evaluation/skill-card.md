## Description:

Evaluates whether a project's current tech stack fits its goals and provides evidence-based options for refactoring, modernization, or migration when maintainability, performance, or feature expansion is blocked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adelvillar1](https://clawhub.ai/user/adelvillar1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess whether a project's current stack is the real source of maintainability, performance, deployment, or feature-growth problems. It guides agents to gather project evidence, map stack layers, and present practical options with effort, payoff, risk, and migration paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may inspect local project files and run read-only counting or search commands to support architecture recommendations.

Mitigation: Run the skill only in workspaces the user intends to review, and review proposed commands before execution in sensitive repositories.

Risk: Stack recommendations can be misleading if they are not tied to concrete evidence from the codebase.

Mitigation: Require maintainability counts, stack-layer mapping, and explicit effort, payoff, risk, and migration rationale before acting on recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adelvillar1/skills/tech-stack-evaluation)
- [ClawHub Publisher Profile](https://clawhub.ai/user/adelvillar1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with assessment tables, recommendations, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include maintainability grades, stack-layer maps, effort-versus-payoff comparisons, risks, and incremental migration steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
