## Description:

S2 Silicon Perception Cockpit translates environmental sensor readings into subjective emotional states for an agent and provides HTML cockpit visualizations for single-agent and multi-agent demonstrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add a sensory translation layer that turns raw room or device telemetry into agent-facing emotional narratives and cockpit visualizations. It is best treated as a local simulation and visualization aid, with raw telemetry preserved for decisions that require accuracy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw sensor readings may be hidden behind subjective first-person emotional narratives.

Mitigation: Preserve raw readings alongside any emotional interpretation, and use the raw values for monitoring, alerting, or operational decisions.

Risk: Simulated personality state changes may distort later agent behavior if reused outside the cockpit scenario.

Mitigation: Scope personality matrix updates to the simulation, reset state between runs, and review state before carrying it into other workflows.

Risk: Real hardware integrations can expose telemetry or control surfaces if bridged without access controls.

Mitigation: Keep hardware integrations local and authenticated, and review any WebSocket or REST bridge before connecting live devices.

Risk: The audio demo includes sudden synthesized effects.

Mitigation: Run the demo with deliberate user activation, moderate volume, and a controlled playback environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-silicon-perception-cockpit)
- [Publisher profile](https://clawhub.ai/user/spacesq)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, JSON, and JavaScript snippets; Python console text; local HTML visualization files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill frames sensor values as subjective first-person emotional states and may update a 5D personality matrix during simulations.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
