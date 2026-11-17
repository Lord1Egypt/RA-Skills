## Description:

Inspect, explain, validate, and convert ESRI Shapefile datasets, including `.shp/.shx/.dbf/.prj` sidecar requirements, CRS detection, field-name/type limits, encoding problems, multipart geometry issues, and migration guidance to GeoPackage or GeoJSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, GIS practitioners, and data engineers use this skill to inspect Shapefile sidecar completeness, diagnose CRS, DBF encoding, schema, and geometry issues, and plan safer migration to GeoPackage or GeoJSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested qgis commands for conversion or repair could alter real datasets or produce incorrect outputs if run without review.

Mitigation: Review generated commands before execution and prefer writing to new output paths instead of mutating source files in place.

Risk: Missing CRS or encoding metadata can lead to misplaced features or garbled attribute text if guessed incorrectly.

Mitigation: Confirm sidecar files, CRS source, and encoding evidence before assigning CRS values or converting datasets.

## Reference(s):

- [Shapefile Patterns](references/patterns.md)
- [ClawHub skill page](https://clawhub.ai/jvy/skills/shp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route deterministic conversion or repair execution to qgis and should prefer new output paths for dataset safety.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
