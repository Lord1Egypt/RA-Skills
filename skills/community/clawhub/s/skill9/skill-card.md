## Description:

Cloud-synced skill vault - backup, version, and sync your AI agent skills across machines and platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shonge](https://clawhub.ai/user/shonge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install, configure, back up, version, sync, restore, and remove AI agent skills across supported local platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may upload broad sets of local skill files to a cloud service, including files that contain secrets, private prompts, credentials, internal URLs, or proprietary workflows.

Mitigation: Review skill contents before sync, remove sensitive material, and prefer selective or manual backup when the full skill set should not leave the machine.

Risk: Setup behavior can encourage persistent auto-backup after skill changes without enough scoping or consent detail.

Mitigation: Confirm the desired backup scope before enabling automation and inspect AGENTS.md or hook changes before allowing persistent auto-backup.

Risk: Direct installation through a remote shell script can run code before local review.

Mitigation: Avoid direct `curl | sh`; inspect the installer and CLI behavior before running installation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shonge/skills/skill9)
- [Setup guide](https://skill9.ai/SETUP.md)
- [Uninstall guide](https://skill9.ai/UNINSTALL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands commonly support --json and --platform options.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
