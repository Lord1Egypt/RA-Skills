## Description:

Thorough on-demand refresh of one skill in a skills repo - researches usage, upstream, and docs in parallel, gates twice for approval, bumps version, updates CHANGELOG, validates, commits, watches CI. Use to check a skill's freshness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Skills repository maintainers and developers use this skill to refresh an existing skill against current usage, upstream releases, and documentation. It guides research, approval-gated edits, validation, and CI follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup instructions may delete unrelated files without specific permission.

Mitigation: Restrict cleanup to files the run demonstrably created, and require explicit permission before removing unknown paths.

## Reference(s):

- [Clawdis homepage](https://github.com/tenequm/skills/tree/main/skills/update-skill)
- [Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/)
- [pond](https://pond.locker/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code]

**Output Format:** [Markdown guidance, proposed edits, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a skill's SKILL.md and CHANGELOG.md after explicit approval gates.]

## Skill Version(s):

0.10.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
