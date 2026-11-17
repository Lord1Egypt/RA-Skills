## Description:

Use when starting a new .NET/Blazor/Angular MVP project in an empty repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to bootstrap a new MVP repository with a .NET, Blazor, or Angular stack, project structure, agent harness files, documentation, and local build checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create project structure, install framework packages, run builds, create local documentation, add repo-local agent harness files, and create commits.

Mitigation: Use it only in a new repository where those changes are expected, review generated files before relying on them, and confirm stack choices before execution.

Risk: Parts of the interaction and confirmations are written in Portuguese, which can lead to misunderstanding if the user does not read Portuguese.

Mitigation: Ask for English confirmations or translation before approving stack decisions or repository changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afonsoft/skills/scaffold-mvp)
- [Publisher profile](https://clawhub.ai/user/afonsoft)
- [Source metadata URL](https://github.com/afonsoft/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create repository structure, documentation, configuration files, lockfiles, local stubs, and initial commits after user approval.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata; artifact frontmatter lists 2.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
