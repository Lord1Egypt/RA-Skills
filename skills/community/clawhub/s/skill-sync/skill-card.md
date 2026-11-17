## Description:

Automatically sync local skills to ClawHub and GitHub by detecting new or modified skills, publishing them, committing changes, and maintaining sync status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this agent skill to scan local skill workspaces, identify skills that need synchronization, publish them to ClawHub, push repository updates, and report sync status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic publishing and Git pushing can expose unintended skill changes or repository contents.

Mitigation: Run only in a controlled skills workspace, review the sync list before execution, and inspect repositories for secrets before publishing or pushing.

Risk: Advertised safety controls are incomplete or not enforced, including dry-run and confirmation behavior.

Mitigation: Avoid unattended cron use until confirmation and dry-run controls are verified or implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyhot/skills/skill-sync)
- [Artifact-declared GitHub repository](https://github.com/sunnyhot/skill-sync)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Console text, Markdown sync reports, JSON status files, and command/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish ClawHub releases, commit and push Git repositories, and write local sync status and log files when executed.]

## Skill Version(s):

1.5.0 (source: server release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
