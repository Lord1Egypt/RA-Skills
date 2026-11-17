## Description:

Recursive self-improvement engine. Think from first principles, let insights emerge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsssgdtc](https://clawhub.ai/user/hsssgdtc)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to analyze a repository, identify repair or discovery opportunities, and generate first-principles improvement prompts for an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs project-controlled build, test, lint, git, grep, python, and pytest commands under the user's account.

Mitigation: Use it only on trusted repositories or inside a sandbox where command execution and filesystem writes are acceptable.

Risk: Repository text is turned into agent-facing improvement prompts, which can carry misleading or malicious project content into the workflow.

Mitigation: Review generated prompts and proposed changes before applying them, especially when analyzing third-party repositories.

Risk: The skill writes .ralph state and improvement history files in the target project.

Mitigation: Run it in a disposable checkout or review .ralph changes before committing or sharing repository contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hsssgdtc/skills/ralph-evolver)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated improvement instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write .ralph state files in the target repository and may print repository-derived prompt content.]

## Skill Version(s):

1.0.6 (source: frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
