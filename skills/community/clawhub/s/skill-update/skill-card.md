## Description:

Updates installed agent skills safely: version check, diff preview, backup, approval, data migration, and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to update installed skills with previews, backups, explicit approval, data migration checks, and rollback paths. It is especially useful when skill behavior, local edits, or multi-agent installations make a simple update risky.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an unpinned external updater that can modify installed skills and change future agent behavior.

Mitigation: Use a pinned and verified `clawic` CLI or locked local install, review the preview diff, and require explicit approval before applying updates.

Risk: `update --all` can apply changes to multiple skills after a broad request.

Mitigation: Separate major versions, breaking changes, migrations, local edits, and pinned skills from the batch, then require per-skill approval for those cases.

Risk: Data migrations during updates can alter or lose user state if they are based on assumed formats or fail midway.

Mitigation: Back up the skill and its data folder first, read actual user data before mapping, copy and verify instead of moving, and restore from the same backup if migration fails.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/skill-update)
- [Clawic Skill Page](https://clawic.com/skills/skill-update)
- [Publisher Profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, file paths, and update reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backup paths, diff summaries, migration plans, rollback steps, and per-skill update status.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
