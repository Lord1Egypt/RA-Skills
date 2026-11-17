## Description:

Inspect, explain, validate, and convert ESRI Shapefile datasets, including sidecar requirements, CRS detection, field-name and type limits, encoding problems, multipart geometry issues, and migration guidance to GeoPackage or GeoJSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, GIS analysts, and agents use this skill to inspect Shapefile sidecar files, diagnose CRS, encoding, geometry, and schema issues, and plan repairs or migrations to GeoPackage or GeoJSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dataset repairs or conversions can overwrite source files if performed in place.

Mitigation: Write outputs to a new path unless the user explicitly requests overwrite.

Risk: Missing CRS or encoding metadata can lead to incorrect coordinate assignment or garbled attributes.

Mitigation: Confirm .prj, .cpg, or source-provided metadata before assigning CRS, decoding DBF text, or converting formats.

Risk: Shapefile schema limits can truncate field names or lose richer attribute types during conversion.

Mitigation: Identify likely lossy fields before export and prefer GeoPackage when richer schema support is needed.

## Reference(s):

- [Shapefile Patterns](references/patterns.md)
- [ClawHub skill page](https://clawhub.ai/jvy/skills/shapefile)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with optional inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on inspection, troubleshooting, conversion planning, and safer output-path recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
