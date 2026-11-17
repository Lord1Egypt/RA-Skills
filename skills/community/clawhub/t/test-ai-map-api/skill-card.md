## Description:

Provides direct Baidu Maps Agent Plan calls for place search, directions, geocoding, reverse geocoding, and weather.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxf969175364](https://clawhub.ai/user/zxf969175364)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and map-enabled assistants use this skill to call Baidu Maps Agent Plan APIs for location search, route planning, weather lookup, geocoding, and reverse geocoding through token-authenticated curl requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map searches, route requests, addresses, precise coordinates, and token-authenticated request context are sent to Baidu Maps.

Mitigation: Use the skill only when third-party Baidu Maps processing is acceptable, and avoid exact home, work, or sensitive locations unless the user intentionally provides them.

Risk: The skill requires BAIDU_MAP_AUTH_TOKEN and produces curl commands that include authenticated requests.

Mitigation: Read the token from the environment, avoid exposing it in logs or chat, and review generated shell commands before execution.

Risk: Vague location requests such as near me can lead to incorrect or fabricated coordinates if handled carelessly.

Mitigation: Use only user-provided or reliable-source coordinates; when coordinates are unavailable, clarify with the user or obtain them through geocoding or place lookup first.

## Reference(s):

- [Baidu Maps Open Platform](https://lbs.baidu.com)
- [Baidu Maps Agent Plan Console](https://lbs.baidu.com/apiconsole/agentplan)
- [ClawHub skill page](https://clawhub.ai/zxf969175364/skills/test-ai-map-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with curl command examples and Baidu Maps API request parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and BAIDU_MAP_AUTH_TOKEN; requests may include addresses, route requests, and precise coordinates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
