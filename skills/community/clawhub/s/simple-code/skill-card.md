## Description:

Simple Code guides agents through small coding projects and practical code reviews using start, continue, and review workflows that emphasize planning, readable implementation, verification, and concise reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyharry](https://clawhub.ai/user/hyharry)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Simple Code to create small projects, extend existing code, or review code changes with a simple planning, implementation, verification, and reporting workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit project files, create local .steps notes, initialize git, and make commits.

Mitigation: Invoke it with an explicit mode and project path, and review planned changes and diffs before accepting them.

Risk: Generated coding or review guidance may be incomplete or unsuitable for a specific codebase.

Mitigation: Run available tests, builds, lint checks, or smoke checks before relying on the resulting code changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyharry/skills/simple-code)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with code, shell commands, and file or configuration changes when applied by the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local project edits, .steps notes, git initialization, and commits when the user invokes those workflows.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
