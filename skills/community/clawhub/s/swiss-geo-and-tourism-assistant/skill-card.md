## Description: <br>
Helps answer questions about Swiss places, coordinates, elevation, points of interest, public transport, map links, weather, hazards, and tourism data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MBjoern](https://clawhub.ai/user/MBjoern) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travelers use this skill to look up Swiss locations, elevation, map layers, urban points of interest, public transport connections, weather, hazards, and tourism options. <br>

### Deployment Geography for Use: <br>
Switzerland <br>

## Known Risks and Mitigations: <br>
Risk: Location, address, and travel-plan queries may be sent to referenced public APIs. <br>
Mitigation: Avoid entering sensitive private addresses or detailed personal travel plans unless the user is comfortable sharing them with those services. <br>
Risk: Weather, avalanche, flood, hiking, and other hazard information may be incomplete, stale, or unsuitable for safety-critical decisions. <br>
Mitigation: Verify safety-critical conditions with official sources before acting on the results. <br>
Risk: Approximate coordinate conversion and third-party data can produce imprecise location or elevation results. <br>
Mitigation: Use official transformation services and source maps when precision matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MBjoern/swiss-geo-and-tourism-assistant) <br>
- [Swisstopo API reference](references/api.md) <br>
- [geo.admin.ch API documentation](https://api3.geo.admin.ch/) <br>
- [transport.opendata.ch API](https://transport.opendata.ch/) <br>
- [MeteoSwiss Open Data](https://www.meteoswiss.admin.ch/services-and-publications/service/open-data.html) <br>
- [SLF avalanche bulletin](https://www.slf.ch/de/lawinenbulletin-und-schneesituation.html) <br>
- [BAFU hydrological data](https://www.hydrodaten.admin.ch/de/aktuelle-lage) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Markdown] <br>
**Output Format:** [Markdown with inline curl and Python command examples, API URLs, and map links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Swiss geodata, transport, weather, hazard, and POI APIs; MySwitzerland API examples require MYSWITZERLAND_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
