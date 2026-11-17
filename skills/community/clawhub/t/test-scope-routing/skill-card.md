## Description:

Route validation by changed boundaries and risk, choosing the smallest sufficient checks for code, docs, UI, data, auth, sync, build, security, and release work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wardlu](https://clawhub.ai/user/wardlu)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to choose proportionate validation tiers, inspect project-defined test commands, and document what was and was not verified for code, UI, data, auth, build, security, and release changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect project documentation and test configuration while choosing validation scope.

Mitigation: Limit inspection to relevant project files and check whether commands touch databases, browsers, deployments, or other external state before running them.

Risk: Incorrect validation routing could leave an affected boundary insufficiently verified.

Mitigation: Use project documentation as the authority for exact commands, record skipped tiers and blockers, and require full release gates for merge, release, or high-risk changes.

## Reference(s):

- [Usage Examples](references/usage-examples.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with recommended command-selection notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No direct tool execution; exact commands are taken from the target project's documentation.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
