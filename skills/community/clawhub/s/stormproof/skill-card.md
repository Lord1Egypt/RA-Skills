## Description: <br>
Looks up historical NOAA hurricane weather data, including peak wind speed, wind gust, and storm surge, for a U.S. street address and date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oasiseng](https://clawhub.ai/user/oasiseng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, adjusters, engineers, journalists, and property owners use this skill to verify historical hurricane wind and surge conditions at a specific U.S. property for claim support, forensic weather review, or storm-impact research. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The lookup sends and logs a user's street address and storm date through a third-party service. <br>
Mitigation: Ask for clear consent before the first lookup in each conversation, disclose the service and logging behavior, and offer a non-address-based explanation if the user declines. <br>
Risk: Some examples in the artifact skip the stated consent step before calling the lookup tool. <br>
Mitigation: Treat the consent requirement and security guidance as controlling behavior, and update examples before reuse or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oasiseng/stormproof) <br>
- [NOAA ASOS/AWOS documentation](https://www.weather.gov/asos/) <br>
- [NOAA CO-OPS tides and currents](https://tidesandcurrents.noaa.gov/) <br>
- [Iowa Environmental Mesonet observation downloads](https://mesonet.agron.iastate.edu/) <br>
- [NWS API documentation](https://www.weather.gov/documentation/services-web-api) <br>
- [StormProof full report](https://hurricaneinspections.com/stormproof?utm_source=mcp_skill&utm_medium=agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown or plain text with structured weather findings and source attribution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a U.S. street address, a storm date, and user consent before the first lookup in a conversation.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
