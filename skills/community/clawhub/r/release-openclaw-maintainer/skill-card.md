## Description:

Prepare, publish, recover, or verify OpenClaw beta, stable, and extended-stable releases, including approved backports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Release operators and OpenClaw maintainers use this skill to prepare, validate, publish, recover, and verify beta, stable, or extended-stable releases and approved backports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A failed worktree setup could cause Git cleanup to hard reset the original checkout, and security analysis was incomplete with one component only partially inspected.

Mitigation: Review setup and cleanup behavior before installation, confirm reset commands can affect only an isolated worktree, and complete review of the partially inspected component.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hillstreet-ph/skills/release-openclaw-maintainer)
- [Regular release](references/regular-release.md)
- [Release validation and confidence](references/validation.md)
- [Backport discovery](references/backport-discovery.md)
- [Extended-stable backport preparation](references/extended-stable-backports.md)
- [Extended-stable publication](references/extended-stable-publish.md)
- [Publication recovery](references/publication-recovery.md)
- [Platform publication](references/platform-publication.md)
- [Stable main closeout](references/stable-main-closeout.md)
- [First-package registry preparation](references/first-package.md)
- [Release preparation](references/preparation.md)
- [Release handoff template](references/release-handoff-template.md)

## Skill Output:

**Output Type(s):** [Shell commands, Release guidance, Markdown handoff records, Release evidence and artifacts]

**Output Format:** [Markdown guidance and handoff records with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the selected release phase; publication artifacts require explicit authorization and complete release evidence.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
