## Description:

Creates a new AI Skill inside an existing WeChat mini-program project by clarifying requirements, designing interfaces, generating code with wxa-skills-generate, and validating it with wxa-skills-validate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binggg](https://clawhub.ai/user/binggg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add a custom AI capability to an existing mp-skills mini-program project. It guides requirement clarification, interface design, code generation, validation, and registration of the generated skill package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run and trust an unpinned external npm CLI that can modify the project.

Mitigation: Use a pinned or locally locked mp-skills version, verify the package source, run it in a version-controlled project, and inspect generated files and app.json diffs before committing or deploying.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a skills/{skill-name}/ package and app.json registration guidance for an existing mp-skills project.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
