## Description: <br>
Search the Recreation Information Database (RIDB) for campgrounds and recreation facilities near a location, including geocoded city names or latitude/longitude coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanrea](https://clawhub.ai/user/seanrea) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agents use this skill to find federal campgrounds, recreation areas, and reservable facilities near a specified location or coordinate pair. It helps discover facility IDs and metadata before checking availability or booking through recreation.gov. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location names or coordinates entered for searches are sent to external services for geocoding and facility lookup. <br>
Mitigation: Avoid using sensitive private locations when that matters to the user's threat model, or provide only locations the user is comfortable sharing with OpenStreetMap Nominatim and RIDB. <br>
Risk: The skill requires an RIDB API key for facility searches. <br>
Mitigation: Provide the key through the documented environment variable or command option and avoid exposing it in shared logs, prompts, or committed files. <br>


## Reference(s): <br>
- [RIDB API Notes](references/api-notes.md) <br>
- [RIDB Portal](https://ridb.recreation.gov) <br>
- [RIDB API Key Profile](https://ridb.recreation.gov/profile) <br>
- [Recreation.gov](https://www.recreation.gov) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Human-readable text or JSON from a Python CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an RIDB API key; location-name searches send the entered location to OpenStreetMap Nominatim for geocoding.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
