## Description: <br>
Vienna public transport (Wiener Linien) real-time data. Use when asking about departures, schedules, disruptions, elevator status, or directions in Vienna's public transport (U-Bahn, tram, bus, night bus). Queries stops, lines, and traffic info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjanuschka](https://clawhub.ai/user/hjanuschka) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to look up Vienna public transport departures, stop identifiers, service disruptions, and elevator outages from public Wiener Linien data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound HTTPS requests to wienerlinien.at. <br>
Mitigation: Install and run it only in environments where public Wiener Linien transit lookups and outbound network access to that domain are acceptable. <br>
Risk: The helper scripts depend on curl and jq being present. <br>
Mitigation: Confirm curl and jq are installed before use so API responses can be fetched and parsed as expected. <br>


## Reference(s): <br>
- [Wiener Linien Skill on ClawHub](https://clawhub.ai/hjanuschka/wienerlinien) <br>
- [Wiener Linien Open Data](https://www.wienerlinien.at/open-data) <br>
- [Wiener Linien Real-Time API](https://www.wienerlinien.at/ogd_realtime) <br>
- [Wiener Linien Stops CSV](https://www.wienerlinien.at/ogd_realtime/doku/ogd/wienerlinien-ogd-haltepunkte.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON output from Wiener Linien API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; makes outbound HTTPS requests to wienerlinien.at and should not require credentials or private local data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
