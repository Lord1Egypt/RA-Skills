## Description:

Execute implementation plans by dispatching a fresh subagent per task with two-stage review for mostly independent tasks that need high-quality, fast iteration within a single session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to execute an existing implementation plan by delegating each task to fresh subagents and enforcing spec and code-quality reviews before moving on.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installation command uses npx clawhub@latest, which may install an unpinned package version.

Mitigation: Prefer a pinned or otherwise verified installer version before installing.

Risk: The workflow can make code changes, run tests, create commits, and proceed without human review between tasks.

Mitigation: Review the implementation plan carefully and keep the spec-compliance and code-quality review gates in place before completing each task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/subagent-driven-development-2)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands and review findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the implementation plan and repository tasks.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
