## Description:

Use when the user asks to cut a release, tag a version, publish a release, or roll up the changelog. Not for routine merges; releases happen on request, not per feature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining a repository use this skill on explicit request to turn merged work into a validated, versioned release, update the changelog, create a commit and tag, publish a GitHub release, and prepare announcement drafts. It does not post announcements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A requested release can edit repository files, create commits and tags, push them, and publish a GitHub release.

Mitigation: Before execution, confirm the repository, remote, and intended release scope, and verify that the user explicitly requested the release.

## Reference(s):

- [Release Cut on ClawHub](https://clawhub.ai/escoffier-labs/skills/skillet-release-cut)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown release guidance and announcement drafts with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Release actions occur only on request; announcement drafts are not posted.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact declares 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
