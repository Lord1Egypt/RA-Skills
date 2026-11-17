## Description:

Get real-time commute traffic using TomTom Routing API. Live travel times, delays, and ETAs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vijays365](https://clawhub.ai/user/vijays365)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and automation users use this skill to query TomTom commute routes for distance, live travel time, traffic delay, affected distance, and ETA. It can also support scheduled commute updates and optional email notifications when AgentMail is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted departure time, route name, or recipient values can trigger local code execution through shell-to-python interpolation.

Mitigation: Do not pass untrusted route, departure, or email values until the interpolation bugs are fixed and reviewed.

Risk: Route coordinates are sent to TomTom, and the optional email workflow can send commute details to AgentMail.

Mitigation: Use the skill only for routes and recipients acceptable for those services, and avoid sensitive commute details unless the user has approved that data sharing.

Risk: Runtime requirements are incomplete because python3 is used and AgentMail is optional but not declared in the primary metadata.

Mitigation: Confirm python3 is available, and declare or document AgentMail requirements before enabling the email workflow.

## Reference(s):

- [TomTom Developer Portal](https://developer.tomtom.com)
- [TomTom Routing API calculateRoute endpoint](https://api.tomtom.com/routing/1/calculateRoute/{origin}:{dest}/json)
- [ClawHub skill page](https://clawhub.ai/vijays365/skills/tomtom-traffic-commute)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown usage guidance with shell commands; the traffic script emits JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOMTOM_API_KEY, bash, curl, and python3 at runtime; optional email workflow uses AgentMail environment variables.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
