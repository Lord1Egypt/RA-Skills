## Description:

Helps agents answer Swiss geography and tourism questions by searching places and addresses, querying elevation and map features, finding points of interest, generating geo.admin.ch map links, and retrieving Swiss public transport and safety-related travel information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbjoern](https://clawhub.ai/user/mbjoern)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to support Swiss travel, mapping, sightseeing, and location lookup workflows. It is useful for answering questions about Swiss places, coordinates, nearby points of interest, public transport, and map layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outdoor hazard, avalanche, flood, and weather outputs may be incomplete, stale, or unsuitable for safety-critical route decisions.

Mitigation: Treat these outputs as informational only and verify current conditions with official real-time bulletins before travel or emergency decisions.

Risk: Tourism and location results depend on external APIs and may vary in coverage, availability, freshness, or accuracy.

Mitigation: Check generated map links, timestamps, and source API results before relying on recommendations or schedules.

## Reference(s):

- [Swisstopo API Reference](references/api.md)
- [geo.admin.ch API](https://api3.geo.admin.ch/)
- [geo.admin.ch Map Viewer](https://map.geo.admin.ch/)
- [transport.opendata.ch API](https://transport.opendata.ch/)
- [MeteoSwiss Open Data](https://www.meteoswiss.admin.ch/services-and-publications/service/open-data.html)
- [SLF Avalanche Bulletin](https://www.slf.ch/de/lawinenbulletin-und-schneesituation.html)
- [BAFU Hydrological Data](https://www.hydrodaten.admin.ch/de/aktuelle-lage)
- [Switzerland Tourism Open Data API](https://opendata.myswitzerland.io/)
- [ClawHub Skill Page](https://clawhub.ai/mbjoern/skills/swiss-geo-and-tourism-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown with inline shell commands, API URLs, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated map links, parsed API response summaries, and references to external Swiss data services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
