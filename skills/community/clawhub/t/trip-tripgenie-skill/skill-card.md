## Description:

Use for any travel question -- hotels, flights, trains, attractions, destinations, and travel tips worldwide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trips-ai](https://clawhub.ai/user/trips-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use TripGenie to answer travel questions, search flight options, and summarize Trip.com travel API responses for hotels, flights, trains, attractions, destinations, and travel tips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel questions, itinerary details, and API tokens are sent to Trip.com.

Mitigation: Enable the skill only when Trip.com is an acceptable data processor, prefer TRIPGENIE_API_KEY over pasted keys, and avoid including unnecessary personal details in prompts.

Risk: API responses are third-party content that may include promotional links or unnecessary details.

Mitigation: Summarize and filter TripGenie responses before presenting them to users instead of relaying raw API output.

Risk: Automatic invocation can send travel queries more often than intended.

Mitigation: Disable or limit automatic invocation when case-by-case control is required.

## Reference(s):

- [TripGenie homepage](https://www.trip.com/tripgenie)
- [TripGenie OpenClaw setup](https://www.trip.com/tripgenie/openclaw)
- [ClawHub TripGenie skill page](https://clawhub.ai/trips-ai/skills/trip-tripgenie-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown guidance with inline bash command examples and summarized text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRIPGENIE_API_KEY, curl, and jq; API responses should be summarized and filtered before being presented to users.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
