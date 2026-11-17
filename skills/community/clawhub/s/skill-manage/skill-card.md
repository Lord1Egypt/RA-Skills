## Description:

Skill Manage helps OpenClaw users list, check, install, update, and uninstall skills from GitHub, SkillHub, Config, or local sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy8663](https://clawhub.ai/user/andy8663)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to manage installed skills, inspect available updates, and run source-appropriate install, update, or uninstall commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uninstall cleanup can delete files beyond the selected skill and may remove configuration files unexpectedly.

Mitigation: Run uninstall with --dry-run first, review every planned path, back up skill configuration files, and avoid --force unless the deletion list is confirmed.

Risk: The release is flagged suspicious by the authoritative security evidence.

Mitigation: Review the script before installation and narrow cleanup behavior to recorded skill-owned paths before trusting routine use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andy8663/skills/skill-manage)
- [Publisher Profile](https://clawhub.ai/user/andy8663)
- [Project Homepage](https://github.com/andy8663/skill-manage)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local shell commands such as git pull, skillhub install, and filesystem cleanup commands when the user runs the provided script.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
