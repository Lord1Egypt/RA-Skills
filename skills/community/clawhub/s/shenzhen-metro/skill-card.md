## Description:

Shenzhen Metro helps agents answer questions about Shenzhen subway lines, stations, fares, schedules, transfers, crowding, nearby amenities, discounts, accessibility, and related travel details using bundled unofficial test data and optional Amap lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mickey406](https://clawhub.ai/user/mickey406)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for Shenzhen Metro route, station, fare, schedule, transfer, crowding, and amenity information. Important trips should be verified against official Shenzhen Metro sources because the bundled data is unofficial and provided for test use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled transit data is unofficial, unverified, and may be stale or incorrect for time-sensitive trips.

Mitigation: Verify important trips, schedules, and fare details with official Shenzhen Metro sources before relying on the answer.

Risk: The optional Amap API feature can expose a real API key if the key is saved in shared project files or pasted into logs, commits, or support messages.

Mitigation: Store real API keys outside shared artifacts and avoid sharing authenticated URLs or committed key values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mickey406/skills/shenzhen-metro)
- [Amap place text API endpoint](https://restapi.amap.com/v3/place/text?city=深圳&keywords=车公庙站&key=YOUR_API_KEY)
- [Bundled Shenzhen Metro facts](artifact/data/metro_facts.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text answers, with optional shell command examples for Amap API calls and configuration guidance for API keys.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may combine bundled offline facts with optional Amap API lookups when the user configures an API key.]

## Skill Version(s):

3.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
