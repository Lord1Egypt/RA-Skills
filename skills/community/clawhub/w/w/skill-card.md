## Description:

Provides weather information, word learning, Wikipedia and web search, writing assistance, workout planning, weight tracking, and hydration reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this Python skill pack to answer everyday requests for weather, word definitions, wiki or web lookup, writing suggestions, workout plans, and simple personal trackers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup and search inputs may be sent to third-party services, and weight or workout data is handled by in-memory trackers.

Mitigation: Avoid sensitive locations, search terms, or health data unless the deployment has acceptable privacy controls and clear user disclosure.

Risk: The security guidance flags HTTP weather calls, placeholder API keys, unencoded request parameters, missing timeouts, and an unpinned requests dependency.

Mitigation: Use HTTPS, load API keys from the environment, encode request parameters, set request timeouts, and pin dependency versions before deployment.

Risk: Writing and workout responses are generic helper outputs and may be incomplete or unsuitable for a user's specific needs.

Mitigation: Review outputs before relying on them, and do not treat workout suggestions as professional medical or fitness advice.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hgta23/skills/w)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Plain text and simple structured text returned by Python methods]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses in-memory logs and plans; some lookup functions require network access and external API keys.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
