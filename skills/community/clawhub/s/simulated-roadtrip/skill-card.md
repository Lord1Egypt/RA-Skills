## Description:

Generate a narrated road trip with GPS-verified stops and themed descriptions using real Google Maps data, posted in timed updates or chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpaulgrayson](https://clawhub.ai/user/jpaulgrayson)

### License/Terms of Use:


## Use Case:

Agents and their operators use this skill to generate themed, GPS-grounded road-trip stop narratives from an origin, destination, theme, and stop count for chat, social posts, or saved trip data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the entered origin, destination, theme, stop count, and Turai API key to Turai.

Mitigation: Use it only when comfortable with Turai handling those inputs, and avoid private home addresses or sensitive travel plans.

Risk: Drip-feed mode may leave the command running for the selected interval between stops.

Mitigation: Choose short, intentional intervals for interactive use, and avoid unattended drip mode unless the runtime environment is expected to remain active.

## Reference(s):

- [Simulated Roadtrip ClawHub release](https://clawhub.ai/jpaulgrayson/skills/simulated-roadtrip)
- [Turai](https://turai.org)
- [Turai Road Trip API endpoint](https://turai.org/api/agent/roadtrip)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Chat or social-post text, or pretty-printed JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save full trip data to a JSON file and can drip-feed stops over a requested interval.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
