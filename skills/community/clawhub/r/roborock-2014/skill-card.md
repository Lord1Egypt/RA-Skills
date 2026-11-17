## Description:

Guides an agent through installing, configuring, authenticating, troubleshooting, and using roborock-cli to query and control Roborock vacuum devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jru001](https://clawhub.ai/user/jru001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help an agent operate Roborock vacuums with roborock-cli, including setup, authentication, device status checks, cleaning actions, dock actions, DND and volume settings, routine execution, map export, troubleshooting, and script integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes remote uv installer commands and tool installation steps.

Mitigation: Install uv and roborock-cli through trusted, pinned, or verified package channels before use.

Risk: The skill can guide commands that change physical device state, including cleaning, docking, DND, volume, dock actions, and routine execution.

Mitigation: Confirm the exact device, room, routine, and requested action before allowing control commands.

Risk: Roborock authentication files and exported maps can expose sensitive account and home-layout information.

Mitigation: Treat auth cache files, device cache files, and saved map images as sensitive home data and avoid unnecessary sharing or persistence.

## Reference(s):

- [roborock-cli command specification](artifact/references/commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command-output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may authenticate to and control home vacuum devices; exported maps and Roborock auth cache files should be treated as sensitive home data.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
