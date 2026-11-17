## Description:

Explains and works with WGS 84 coordinate data, including EPSG:4326 usage, axis-order checks, range validation, UTM zone recommendations, and reprojection planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, GIS practitioners, and data engineers use this skill to validate GPS-style longitude/latitude pairs, resolve WGS84/EPSG:4326 usage questions, choose an appropriate projected CRS, and identify common coordinate-order or China map-offset risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coordinate pairs may be interpreted in the wrong axis order when both longitude-latitude and latitude-longitude ranges are numerically valid.

Mitigation: Confirm the source system's expected order and report ambiguity when the values alone cannot determine order.

Risk: WGS84 coordinates can be unsuitable for distance, area, buffer, or engineering workflows that require projected units.

Mitigation: Recommend a projected CRS such as an appropriate UTM zone or local mandated CRS for measurement-focused analysis.

Risk: Coordinates from mainland-China consumer map sources may use GCJ-02 or BD-09 rather than raw WGS84.

Mitigation: Warn users to verify the source coordinate system before treating those points as EPSG:4326.

## Reference(s):

- [WGS84 Reference](references/wgs84-reference.md)
- [ClawHub WGS84 Skill Page](https://clawhub.ai/jvy/skills/wgs84)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Configuration]

**Output Format:** [Markdown with JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include coordinate validity results, inferred coordinate order, CRS recommendations, UTM zone and EPSG code, or China offset-risk warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
