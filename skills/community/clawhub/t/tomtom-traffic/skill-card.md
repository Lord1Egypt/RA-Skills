## Description:

Provides real-time traffic data, route calculation, and departure planning using the TomTom Traffic API for commute and meeting alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkimnw-code](https://clawhub.ai/user/jkimnw-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to check current commute traffic, calculate traffic-aware routes, and plan departure times for meetings using a configured TomTom API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured route coordinates are shared with TomTom when traffic or routing checks are run.

Mitigation: Install only when that data sharing is acceptable, and review the configured locations before use.

Risk: The skill relies on a TOMTOM_API_KEY from the environment.

Mitigation: Store the key outside source files and rotate it if it is exposed.

Risk: Default Seattle and Bellevue locations may not match the user's commute or meeting context.

Mitigation: Edit the configured locations, buffers, and time zone before using it for personal departure planning.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jkimnw-code/skills/tomtom-traffic)
- [Publisher Profile](https://clawhub.ai/user/jkimnw-code)
- [TomTom Developer Portal](https://developer.tomtom.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI text with route summaries, traffic delays, congestion alerts, and departure-time guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOMTOM_API_KEY and sends configured route coordinates to TomTom APIs when invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
