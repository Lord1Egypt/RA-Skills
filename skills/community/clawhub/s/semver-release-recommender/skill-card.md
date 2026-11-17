## Description:

Analyze repository changes from the last release to the current revision and recommend the correct semantic version bump.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nick2bad4u](https://clawhub.ai/user/nick2bad4u)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to inspect repository changes since the last release and produce an evidence-based patch, minor, or major version recommendation before tagging or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default workflow can run an untrusted repository-controlled Python helper when the helper path is resolved from the project being analyzed.

Mitigation: Use the manual Git inspection workflow or verify that any helper script resolves from a trusted installed skill directory before execution.

## Reference(s):

- [Source repository](https://github.com/Nick2bad4u/semver-release-recommender)
- [ClawHub skill listing](https://clawhub.ai/nick2bad4u/skills/semver-release-recommender)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown recommendation with concise rationale, checks, and residual risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a recommended semantic version bump, confidence level, release range, next version, reviewed evidence, and residual risk.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
