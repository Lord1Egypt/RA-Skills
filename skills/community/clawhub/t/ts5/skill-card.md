## Description:

TS5 namespace for Netsnek e.U. TypeScript full-stack starter kit. Monorepo template with shared types, CI/CD pipelines, and one-click deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to bootstrap and manage a TypeScript full-stack monorepo with shared types, frontend, backend, CI/CD, and deployment commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to run a local shell script, and its deploy command is documented more broadly than the current stub implementation.

Mitigation: Review proposed shell commands before execution and confirm deployment targets if a future version adds real deployment behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose running the included local shell script for monorepo setup, package checks, or deployment.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
