## Description: <br>
Query public open data from Umeå kommun on locations, facilities, demographics, environment, infrastructure, and building permits with geospatial support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Simskii](https://clawhub.ai/user/Simskii) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Umeå municipal open datasets, retrieve records, and answer location, facility, statistics, planning, and nearest-place questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nearest-location lookups may fail because the nearby helper references a distance.jq filter that is not packaged in the artifact. <br>
Mitigation: Confirm the distance.jq helper is supplied or avoid nearby.sh until the package is fixed. <br>
Risk: The bundled shell helpers depend on local curl and jq binaries. <br>
Mitigation: Verify both tools are installed before using the scripts. <br>
Risk: Public municipal datasets may change, be incomplete, or require source review before operational decisions. <br>
Mitigation: Check current API responses and source context before relying on results for planning, safety, or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Simskii/umea-data) <br>
- [Umeå Open Data API](https://opendata.umea.se/api/v2/) <br>
- [Publisher Profile](https://clawhub.ai/user/Simskii) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq for the bundled shell helpers; nearest-location queries also require the packaged distance.jq filter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
