## Description:

Repo Runner helps an agent bootstrap and run a GitHub project locally by following project documentation while applying safeguards for untrusted install and run steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyl-hub](https://clawhub.ai/user/zyl-hub)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when they give an agent a GitHub repository or local project folder and want it to identify documented setup, dependency, environment, and run steps before executing them locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may help run commands from untrusted repositories, including install or startup commands documented by the project.

Mitigation: Review every command before execution and use an isolated container or disposable workspace without secrets.

Risk: Repository setup may request environment variables or credentials.

Mitigation: Do not expose real .env values or host credentials to projects you do not trust; provide required values out-of-band only after review.

Risk: Remote execution patterns such as curl|bash can bypass normal review.

Mitigation: Avoid curl|bash and similar remote execution patterns unless the user explicitly approves after inspecting the command source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zyl-hub/skills/repo-runner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command snippets and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes exact commands run, local URLs or ports, next steps, and known caveats when available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
