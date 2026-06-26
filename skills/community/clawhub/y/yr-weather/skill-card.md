## Description: <br>
Fetches current weather conditions and forecasts from MET Norway's yr.no API for user-provided latitude and longitude coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Brandon2255p](https://clawhub.ai/user/Brandon2255p) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve weather forecasts, current conditions, temperature, precipitation, and wind information for specific coordinates. It is suitable when an agent needs a coordinate-based weather lookup rather than city-name geocoding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups disclose the latitude and longitude, and optional altitude, to MET Norway. <br>
Mitigation: Use approximate coordinates when exact location privacy matters. <br>
Risk: Installing from a GitHub pip command can fetch code outside the validated ClawHub artifact. <br>
Mitigation: Install the reviewed ClawHub release artifact, or pin a reviewed GitHub release or commit. <br>


## Reference(s): <br>
- [ClawHub Yr Weather release page](https://clawhub.ai/Brandon2255p/yr-weather) <br>
- [MET Norway Locationforecast API](https://api.met.no/weatherapi/locationforecast/2.0/compact) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text weather summaries with command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires latitude and longitude; optional altitude may be sent with the forecast request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
