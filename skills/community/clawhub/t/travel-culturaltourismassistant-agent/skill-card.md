## Description:

Travel Agent helps generate cultural tourism monitoring reports, itinerary plans, weather summaries, attraction recommendations, multi-city comparisons, scheduled report setup, and usage guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heart-105](https://clawhub.ai/user/heart-105)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers, tourism operators, and developers can use this skill to draft travel research, destination comparisons, itinerary plans, attraction recommendations, and recurring cultural tourism reports. Outputs should be reviewed before operational or customer-facing use, especially where current travel conditions or third-party delivery channels matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says generated travel data may be fabricated or misleading.

Mitigation: Review report contents against current, trusted travel, weather, transportation, and venue sources before relying on the output.

Risk: The security review flags weak handling of secrets, context logging, and webhook-related delivery paths.

Mitigation: Avoid production API keys and real messaging webhooks until the publisher fixes secret handling and logging concerns.

Risk: The security review flags recurring external pushes to messaging or email systems.

Mitigation: Enable scheduled pushes only for approved destinations and confirm recipients, frequency, and cancellation controls before use.

Risk: The security review flags broken entry-point wiring.

Mitigation: Validate installation and command execution in a non-production environment before depending on the skill.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/heart-105/skills/travel-culturaltourismassistant-agent)
- [OpenClaw travel skill documentation](https://docs.openclaw.ai/skills/travel-ai)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reports with short text status messages and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces travel monitoring reports, itinerary plans, weather summaries, attraction recommendations, multi-city comparisons, scheduled push setup responses, and usage summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
