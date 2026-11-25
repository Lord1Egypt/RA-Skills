## Description:

Build a structured workout and send it to the user's Apple Watch with the Workouter MCP tools. Use when the user wants to create, plan, or send a run, ride, swim, walk, hike, row, elliptical, strength, HIIT, EMOM, circuit, or interval workout to their watch, or asks for "a workout" they can follow on their wrist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workouter-co](https://clawhub.ai/user/workouter-co)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to plan a run, ride, swim, walk, hike, row, gym, or interval workout and send it to an Apple Watch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous workout details or unsupported WorkoutKit goals can produce an inaccurate or unusable plan.

Mitigation: Ask for missing units, interval grouping, or swim pool units; explain unsupported goals and suggest a supported alternative.

Risk: A saved workout may not be confirmed as received by the Apple Watch.

Mitigation: Check delivery status for the same workout and offer its phone handoff link when available; do not create a duplicate to retry delivery.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/workouter-co/skills/workouter)

## Skill Output:

**Output Type(s):** [Workout configuration, Guidance]

**Output Format:** [Structured workout configuration with concise user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-goal and interval workouts; custom workouts are outlined for user agreement before creation.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
