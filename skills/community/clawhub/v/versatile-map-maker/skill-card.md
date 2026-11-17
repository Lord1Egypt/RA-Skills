## Description:

Create editable SVG maps for choropleths, categorical region maps, point/label overlays, and custom or historical boundary overlays from Highcharts maps or user-provided GeoJSON/TopoJSON/shapefile-derived data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and map-making agents use this skill to create editable region maps, choropleths, categorical maps, and boundary overlays from built-in public map data or supplied geospatial geometry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce unsafe SVG output from unvalidated style JSON, GeoJSON, or SVG inputs.

Mitigation: Review before installing or using with untrusted files, and only process style JSON, GeoJSON, and SVG inputs from trusted sources until SVG color validation and sanitization are added.

Risk: The skill recommends unpinned package-manager execution.

Mitigation: Use pinned dependencies or a locked environment and avoid running unpinned npx commands.

## Reference(s):

- [Data Sources](artifact/references/data-sources.md)
- [Geometry Inputs](artifact/references/geometry-inputs.md)
- [Styling And Accessibility](artifact/references/styling.md)
- [Technique Notes And Worked Examples](artifact/references/technique.md)
- [Natural Earth Rivers And Lake Centerlines](https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_rivers_lake_centerlines.geojson)
- [Natural Earth Europe Rivers](https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_rivers_europe.geojson)
- [ClawHub Skill Page](https://clawhub.ai/stanestane/skills/versatile-map-maker)

## Skill Output:

**Output Type(s):** [files, markdown, shell commands, configuration, guidance]

**Output Format:** [Editable SVG files, optional PNG previews, generated data/configuration files, and concise Markdown delivery notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify map source, granularity, data source, geometry precision, and any unmatched or missing data.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
