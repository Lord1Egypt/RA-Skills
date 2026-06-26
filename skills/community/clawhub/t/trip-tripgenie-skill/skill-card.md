## Description: <br>
Use for any travel question: hotels, flights, trains, attractions, destinations, and travel tips worldwide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trips-ai](https://clawhub.ai/user/trips-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel agents use TripGenie to answer travel questions, search flights, and summarize travel-related results from Trip.com APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel queries, itinerary details, and API credentials are sent to Trip.com for processing. <br>
Mitigation: Confirm Trip.com is an acceptable processor, set TRIPGENIE_API_KEY as an environment variable, avoid pasting keys into chat, and avoid unnecessary sensitive personal details. <br>
Risk: External API responses may include promotional content, links, or details that are not appropriate to relay verbatim. <br>
Mitigation: Summarize and filter API responses before presenting results to users. <br>


## Reference(s): <br>
- [TripGenie Skill Page](https://clawhub.ai/trips-ai/trip-tripgenie-skill) <br>
- [TripGenie Homepage](https://www.trip.com/tripgenie) <br>
- [TripGenie OpenClaw Setup](https://www.trip.com/tripgenie/openclaw) <br>
- [TripGenie API Endpoint](https://tripgenie-openclaw-prod.trip.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and summarized travel results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRIPGENIE_API_KEY plus curl and jq; API responses should be summarized or filtered before presentation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
