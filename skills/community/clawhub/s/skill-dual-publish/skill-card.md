## Description:

Publishes workspace skills to both GitHub and ClawHub after new or updated SKILL.md files are prepared.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spikesubingrui-design](https://clawhub.ai/user/spikesubingrui-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare and run a dual-publish workflow for workspace skills, including checks for SKILL.md metadata, authentication, repository ownership, visibility, slug, and version.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to run a powerful publishing script that pushes content publicly and edits local configuration.

Mitigation: Use it only when intentional, verify the external script contents and checksum, run a dry run, confirm owner, visibility, slug, version, and file set, and approve AGENTS.md or SKILL.md edits separately.

Risk: The artifact contains a skill-publish versus skill-dual-publish identity mismatch.

Mitigation: Resolve the package name, ClawHub slug, homepage, and release metadata before relying on the publish workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spikesubingrui-design/skills/skill-dual-publish)
- [Project homepage](https://github.com/spikesubingrui-design/skill-dual-publish)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose publication commands and checklist items that should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
