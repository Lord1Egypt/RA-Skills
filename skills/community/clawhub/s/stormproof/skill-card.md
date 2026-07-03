## Description: <br>
Looks up historical NOAA hurricane weather data, including wind, gust, surge, hail, and severe-weather context, for a specific U.S. street address and storm date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oasiseng](https://clawhub.ai/user/oasiseng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, public adjusters, contractors, forensic engineers, journalists, and agents use this skill to verify historical storm conditions at a specific U.S. property for insurance, damage evaluation, or property-level hurricane research after obtaining consent to submit the address and date. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The lookup submits a user's street address and storm date to hurricaneinspections.com, where the request may be logged. <br>
Mitigation: Obtain explicit per-conversation consent before calling the tool, use only addresses the user is authorized to submit, and provide general NOAA context instead if the user declines. <br>
Risk: Historical weather results can be incomplete or approximate because the lookup uses NOAA coverage, nearby stations, ranges, and a limited date window. <br>
Mitigation: Present results as ranges with NOAA attribution, flag sparse or missing data plainly, and avoid legal, coverage, or claim-outcome conclusions. <br>


## Reference(s): <br>
- [ClawHub StormProof listing](https://clawhub.ai/oasiseng/skills/stormproof) <br>
- [NOAA ASOS/AWOS documentation](https://www.weather.gov/asos/) <br>
- [NOAA CO-OPS tides and currents](https://tidesandcurrents.noaa.gov/) <br>
- [NWS active alerts and historical archives API](https://www.weather.gov/documentation/services-web-api) <br>
- [Iowa Environmental Mesonet observation downloads](https://mesonet.agron.iastate.edu/) <br>
- [StormProof full report](https://hurricaneinspections.com/stormproof?utm_source=mcp_skill&utm_medium=agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown text with NOAA-attributed weather ranges, severe-weather context, and optional links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a full U.S. street address, a storm date, and explicit per-conversation consent before lookup.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
