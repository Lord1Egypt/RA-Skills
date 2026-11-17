## Description:

TripAI is a Ctrip Wendao travel-query skill that handles complex, conversational Chinese requests for hotels, flights, trains, attraction tickets, day trips, and events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trips-ai](https://clawhub.ai/user/trips-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use TripAI to turn natural-language Chinese travel requests into Ctrip Wendao API queries for travel search and planning across hotels, flights, trains, attractions, local activities, and events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed because the skill can store TRIPAI_API_KEY in a plaintext config file.

Mitigation: Prefer a temporary environment variable; if using the config file, restrict it to owner-only permissions and rotate the token if it may have been exposed.

Risk: Personal travel details in user queries are sent to an external Ctrip Wendao service.

Mitigation: Avoid placing sensitive personal information in free-form travel queries and review the request before sending it.

## Reference(s):

- [TripAI Skill on ClawHub](https://clawhub.ai/trips-ai/skills/tripai-skill)
- [Ctrip Wendao OpenClaw](https://www.ctrip.com/wendao/openclaw)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TRIPAI_API_KEY optionally and sends natural-language travel queries to an external Ctrip Wendao service.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
