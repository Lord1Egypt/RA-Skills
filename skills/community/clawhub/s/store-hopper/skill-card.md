## Description: <br>
A one-day shop-hopping planner that combines weather lookup, guide search, page extraction, and route planning to build efficient city itineraries without lodging recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziyou979](https://clawhub.ai/user/ziyou979) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to plan a one-day route for food, coffee, dessert, check-in spots, or mixed local exploration after confirming the city, preferences, timing, and optional start point. It gathers weather and guide signals, extracts details from selected pages, chooses points of interest, and presents a practical itinerary with transport estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send city names, route locations, URLs, and guide-search terms to external weather, search, map, and page-extraction services. <br>
Mitigation: Confirm user inputs before running scripts, avoid home or work addresses and sensitive URLs, and prefer broad areas or public landmarks when precise locations are unnecessary. <br>
Risk: The fetch workflow includes anti-bot browser tooling and third-party relay services for page extraction. <br>
Mitigation: Use fetch only for public pages the user is comfortable querying, review target URLs before extraction, and disable relay or anti-bot paths in environments where that behavior is not acceptable. <br>
Risk: The weather helper may append newly discovered city codes to a local data file. <br>
Mitigation: Run the skill in a workspace where local file changes are expected and review any city-code updates before retaining or publishing them. <br>
Risk: Search results, weather data, geocoding, route estimates, and cost estimates can be incomplete or inaccurate. <br>
Mitigation: Treat the generated itinerary as planning guidance, cross-check key venue and transit details, and present prices and timing as estimates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziyou979/store-hopper) <br>
- [Publisher profile](https://clawhub.ai/user/ziyou979) <br>
- [City codes](data/city-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown itinerary with helper shell commands and JSON-producing script outputs during execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final responses include weather context, route stops, timing, transport estimates, cost estimates, and practical tips.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
