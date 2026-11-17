## Description:

Control Sensibo smart AC devices through the Sensibo REST API for power, temperature, mode, fan, sensor readings, schedules, timers, and Climate React automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omere2](https://clawhub.ai/user/omere2)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent control Sensibo-connected AC devices, query room temperature and humidity, and manage device schedules or climate automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to store a Sensibo API key in plaintext, and expanded curl commands could expose the key in logs or chat history.

Mitigation: Store the API key in a protected secret store or environment variable, avoid logging commands with expanded credentials, and rotate the key if exposed.

Risk: The skill can change real AC device state, schedules, timers, Climate React automation, and bulk device settings.

Mitigation: Require explicit user confirmation before deleting schedules, changing automations, setting timers, or applying bulk changes; verify the room and device ID before execution.

Risk: Incorrect target temperatures, modes, or device selections could affect comfort, energy use, or equipment behavior.

Mitigation: Check the selected device, supported AC ranges, requested units, and API success response before treating a change as complete.

## Reference(s):

- [Sensibo API key page](https://home.sensibo.com/me/api)
- [Sensibo API v2 base URL](https://home.sensibo.com/api/v2)
- [ClawHub Sensibo skill page](https://clawhub.ai/omere2/skills/sensibo)
- [Publisher profile](https://clawhub.ai/user/omere2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Sensibo API URLs, JSON request bodies, and confirmation-oriented guidance for real device actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
