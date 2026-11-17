## Description:

Generates predictive 4D timeline tracks from natural-language smart-home intents, using active device mounts to schedule keyframes across the 6-Element Spatial Matrix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home automation builders use this skill to turn routine descriptions into scheduled device keyframes for simulated or controlled S2 environments. It is suited to prototyping timeline-based orchestration across lights, audio, HVAC, visual displays, robots, and related home devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated schedules are unvalidated and may later drive real-world smart-home automation.

Mitigation: Prefer simulation or sandbox use unless a separate executor validates every device, action, value, and schedule before execution.

Risk: Sensitive actions such as heaters, locks, high-volume audio, robots, or medication workflows can affect safety if executed without confirmation.

Mitigation: Require explicit confirmation for sensitive actions and reject unsupported devices, actions, values, or schedules.

Risk: Microphone, mmWave, behavioral, and elder-care scenarios can involve privacy-sensitive data.

Mitigation: Require explicit consent, clear retention controls, and privacy review before use in those environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-timeline-orchestrator)
- [Space2.world](https://space2.world)

## Skill Output:

**Output Type(s):** [text, json, configuration]

**Output Format:** [Console text and JSON timeline tracks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated scheduled_tracks entries to s2_timeline_data/rendered_tracks.json when timeline generation succeeds.]

## Skill Version(s):

1.0.0 (source: release metadata, manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
