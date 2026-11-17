## Description:

Predict Animal Crossing New Horizons turnip prices using the game's exact algorithm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicholasjackson](https://clawhub.ai/user/nicholasjackson)

### License/Terms of Use:


## Use Case:

External Animal Crossing players use this skill to estimate likely turnip price patterns, decide when to sell, and visualize future price ranges from their known weekly prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional reminder setup can create persistent scheduled jobs that send messages through the user's OpenClaw identity.

Mitigation: Enable reminders only when needed, review generated crontab entries before installation, and verify removal from crontab when disabling reminders.

Risk: Broad package installation commands may require elevated privileges or system package managers.

Mitigation: Review install commands before running them and install dependencies in an environment appropriate for the user's system.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicholasjackson/skills/turnip-prophet)
- [Publisher profile](https://clawhub.ai/user/nicholasjackson)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON summaries, shell commands, and generated chart file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and jq; optional chart generation uses matplotlib.]

## Skill Version(s):

1.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
