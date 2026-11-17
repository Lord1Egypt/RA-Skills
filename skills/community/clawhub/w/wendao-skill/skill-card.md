## Description:

Ctrip Wendao travel assistant for hotel, flight, train, attraction, and itinerary queries, returning Markdown responses from the Wendao service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trips-ai](https://clawhub.ai/user/trips-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel assistants use this skill to ask natural-language travel planning and booking questions, including hotels, flights, trains, attractions, and itineraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel queries and the Wendao API token are sent to Ctrip.

Mitigation: Confirm users are comfortable sharing travel queries with Ctrip and configure the token as WENDAO_API_KEY rather than pasting it into chat.

Risk: The documented command writes responses to a fixed temporary file.

Mitigation: On shared systems, display the response directly or use a unique restricted temporary file and remove it after use.

Risk: Responses from the external travel service may include links, marketing text, or inaccurate travel information.

Mitigation: Review or filter returned Markdown according to the deployment's content and travel-advice policy before showing it to end users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/trips-ai/skills/wendao-skill)
- [Ctrip Wendao OpenClaw Page](https://www.ctrip.com/wendao/openclaw)
- [Ctrip Wendao Skill API Endpoint](https://wendao-skill-prod.ctrip.com/skill/query)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and WENDAO_API_KEY; API responses are intended to be displayed as Markdown.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
