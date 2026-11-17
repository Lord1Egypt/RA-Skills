## Description:

Structured software development workflow for AI-assisted codebases: gated requirement intake with test cases, change impact analysis, typed implementation boundaries, verified delivery, full regression testing, and experience accumulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morelapai](https://clawhub.ai/user/morelapai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use ShipGuard to structure AI-assisted code changes through requirement intake, impact analysis, implementation boundaries, feature QA, regression checks, and lessons capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent project workflow files and reloaded rules can influence future AI sessions.

Mitigation: Review .dev-workflow changes before committing and require approval before adding hard rules or persistent project memory.

Risk: Some changes may be auto-executed based on the agent's own task classification.

Mitigation: Disable or manually control auto-execute behavior for production or shared repositories, especially for critical paths.

## Reference(s):

- [ShipGuard Project Homepage](https://github.com/morelapAI/shipguard)
- [Hard Rules](references/hard-rules.md)
- [Lessons Learned](references/lessons.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured workflow cards and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and maintain project-local .dev-workflow files for requirements, change records, test cases, regression results, lessons, and changelog entries.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
