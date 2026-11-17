## Description:

Recommends a semantic-version bump from a supplied change list or conventional commits before a release is tagged.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill to assess supplied changes, choose a major, minor, or patch bump, and draft a version, tag subject, and changelog bullets before tagging a release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect bump could lead to a misleading release version.

Mitigation: Provide the current version and complete change list, then check the recommendation against team release policy before tagging.

## Reference(s):

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Git documentation](https://git-scm.com/doc)
- [SemVer Bump Advisor on ClawHub](https://clawhub.ai/hmahmadcs/skills/semver-bump-advisor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown with a recommended bump, next version, rationale, optional tag subject, and sample changelog]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Based on user-supplied version and changes; does not create tags or push releases.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
