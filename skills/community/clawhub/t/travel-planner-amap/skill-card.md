## Description: <br>
Generates personalized travel itineraries using Amap REST API data for routes, points of interest, restaurants, hotels, weather, costs, and packing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bifang988](https://clawhub.ai/user/bifang988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect trip details, query Amap and weather sources, and produce a structured travel plan with transport guidance, daily itinerary, restaurants, lodging, packing notes, and budget estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip locations, dates, route queries, and preferences may be sent to Amap and weather search providers. <br>
Mitigation: Avoid exact home addresses when city-level input is enough and tell users when external travel or weather services are being queried. <br>
Risk: The required AMAP_KEY could be over-permissioned or stored insecurely. <br>
Mitigation: Use a restricted, temporary AMAP_KEY with only needed services enabled; avoid saving it permanently in shell profile files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bifang988/travel-planner-amap) <br>
- [Amap developer console](https://lbs.amap.com) <br>
- [Amap geocoding API endpoint](https://restapi.amap.com/v3/geocode/geo) <br>
- [Amap driving directions API endpoint](https://restapi.amap.com/v3/direction/driving) <br>
- [Amap transit directions API endpoint](https://restapi.amap.com/v3/direction/transit/integrated) <br>
- [Amap place text search API endpoint](https://restapi.amap.com/v3/place/text) <br>
- [Amap place around search API endpoint](https://restapi.amap.com/v3/place/around) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown itinerary with inline shell and Python command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AMAP_KEY as a required environment variable and may include live route, POI, weather, lodging, dining, and budget details.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
