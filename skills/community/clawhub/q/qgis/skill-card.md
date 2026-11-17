## Description:

Run QGIS geospatial processing with qgis_process for repeatable vector and raster workflows, including reprojection, clipping, dissolving, buffering, merging, and raster warping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and GIS practitioners use this skill to inspect QGIS processing algorithms and run reproducible local geospatial transformations on vector and raster files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QGIS processing commands can transform or overwrite local geospatial datasets when paths or parameters are wrong.

Mitigation: Review input paths, output paths, CRS settings, output formats, and overwrite policy before approving commands; prefer new output paths and dry-run plans for batch work.

Risk: Distance, area, or raster operations can produce misleading results when CRS units are misunderstood or missing.

Mitigation: Confirm the intended CRS and whether units are degrees or projected units before running processing algorithms.

## Reference(s):

- [QGIS Geospatial on ClawHub](https://clawhub.ai/jvy/skills/qgis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run plans, explicit qgis_process commands, output path summaries, CRS notes, and verification guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
