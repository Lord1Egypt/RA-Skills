## Description:

Guides repository maintainers through writing changelogs and release notes, publishing releases, and updating past release notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT-0

## Use Case:

Repository maintainers use this skill to prepare consistent changelogs and concise GitHub release notes, follow a reviewed tagging and publication workflow, and correct stale release links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release commands can publish tags and GitHub releases to the wrong repository or version.

Mitigation: Confirm the owner, repository, version, branch, and GitHub authentication context before running publication commands.

Risk: Editing previous release notes or replacing outdated links can change public guidance.

Mitigation: Review proposed edits and verify release-note links and commands against the intended tagged release before publishing.

## Reference(s):

- [Release-writing skill on ClawHub](https://clawhub.ai/worldwonderer/skills/release-writing)
- [Changelog and release-note templates](references/templates.md)
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Changelog and release-note formats include version labels, upgrade guidance, and tagged source links.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
