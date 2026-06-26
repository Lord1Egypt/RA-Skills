## Description: <br>
Explain and work with the WGS 84 coordinate system for GPS-style longitude/latitude data, including EPSG:4326 usage, axis-order checks, range validation, UTM zone recommendation, and reprojection planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, GIS practitioners, and agents use this skill to validate GPS-style longitude/latitude coordinates, reason about EPSG:4326 usage, choose tuple order, and decide when to keep WGS84 or reproject for mapping and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coordinate tuple order or coordinate system ambiguity can lead to incorrect GIS recommendations. <br>
Mitigation: Confirm the source CRS and tuple order before relying on recommendations for important GIS work. <br>
Risk: Coordinates sourced from mainland China consumer-map systems may use GCJ-02 or BD-09 rather than raw WGS84. <br>
Mitigation: Verify whether China-region coordinates come from WGS84, GCJ-02, or BD-09 before conversion or analysis. <br>
Risk: Using WGS84 degrees directly for distance, area, or buffer analysis can produce misleading results. <br>
Mitigation: Reproject to an appropriate projected CRS, such as a local CRS or UTM zone, before measurement-heavy analysis. <br>


## Reference(s): <br>
- [WGS84 Reference](references/wgs84-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/jvy/wgs84) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include interpreted coordinate order, WGS84 range validity, CRS recommendations, UTM zone and EPSG code, and China mapping offset warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
