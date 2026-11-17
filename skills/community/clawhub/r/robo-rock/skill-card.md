## Description:

Control Roborock robot vacuums with CLI commands for status checks, cleaning, maps, consumables, and settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dru-ca](https://clawhub.ai/user/dru-ca)

### License/Terms of Use:


## Use Case:

People who manage Roborock or compatible Xiaomi robot vacuums use this skill to have an agent provide and run commands for cleaning, docking, room selection, map access, consumable checks, and device settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can control physical vacuum behavior, including starting, stopping, docking, room cleaning, consumable resets, and settings changes.

Mitigation: Require user confirmation before executing commands that move the device, alter device state, reset maintenance counters, or change settings.

Risk: Account login, device IDs, maps, and home-layout data may expose private household information.

Mitigation: Authenticate only through the CLI prompt, do not paste credentials into chat, and treat device IDs, maps, and exported images as private data.

Risk: The skill depends on the unpinned third-party python-roborock CLI package.

Mitigation: Install only from trusted package sources, review the installed package before use, and keep the dependency updated according to local policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dru-ca/skills/robo-rock)
- [python-roborock](https://github.com/humbertogontijo/python-roborock)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the roborock CLI and a Roborock/Xiaomi account; commands should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
