## Description:

One-command release pipeline. Bumps version, updates changelog + SKILL.md, publishes to npm + GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use Wip Release to automate package releases, including version bumps, changelog and SKILL.md synchronization, git tagging, npm publishing, GitHub releases, and ClawHub publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish packages and releases, run repository deployment scripts, and use authenticated publishing accounts.

Mitigation: Use it only on trusted repositories, start with dry-run, review configured deploy scripts and website paths, and limit npm and GitHub credentials before non-dry-run releases.

Risk: Release cleanup actions can affect branches, worktrees, and repository state.

Mitigation: Run from clean, backed-up working trees and review repository status before allowing cleanup or publication steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/skills/wip-release)
- [Publisher profile](https://clawhub.ai/user/parkertoddbrooks)
- [Project homepage](https://github.com/wipcomputer/wip-release)
- [npm package](https://www.npmjs.com/package/@wipcomputer/wip-release)
- [README](artifact/README.md)
- [Reference](artifact/REFERENCE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated or updated repository files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can change package metadata, changelogs, tags, releases, npm packages, and ClawHub publication state when run without dry-run.]

## Skill Version(s):

1.9.72 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
