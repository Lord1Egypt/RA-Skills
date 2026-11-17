## Description:

Controls Wiz smart bulbs (turn on/off, RGB colors, disco mode) via local WiFi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canbirlik](https://clawhub.ai/user/canbirlik)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent control Wiz smart bulbs on a local WiFi network, including turning lights on or off, setting RGB colors, and running a temporary disco mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes the state of physical Wiz smart bulbs on the local network.

Mitigation: Use explicit prompts that name this skill and the target bulb before allowing the agent to run control commands.

Risk: The Python dependency is unpinned in requirements.txt.

Mitigation: Review and pin pywizlight to an approved version before installing the skill in a controlled environment.

Risk: Commands require the correct local bulb IP address.

Mitigation: Confirm the target bulb IP on the local network before running on, off, color, or disco actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canbirlik/skills/wiz-light-control)
- [ClawHub publisher profile](https://clawhub.ai/user/canbirlik)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Controls physical Wiz bulb state on the user's local network through the pywizlight dependency.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
