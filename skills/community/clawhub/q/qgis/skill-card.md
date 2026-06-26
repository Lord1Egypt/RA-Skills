## Description: <br>
Run QGIS geospatial processing with qgis_process for repeatable vector and raster workflows, including reprojection, clipping, dissolving, buffering, merging, and raster warping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, GIS analysts, and operators use this skill to plan and run repeatable local QGIS CLI workflows for geospatial data transformation, coordinate system conversion, and batch map data processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QGIS CLI workflows can write or overwrite local geospatial output files. <br>
Mitigation: Confirm input files, output paths, output formats, and overwrite policy before allowing execution. <br>
Risk: Incorrect CRS, units, or distance assumptions can produce misleading geospatial results. <br>
Mitigation: Verify CRS settings and units before processing, and stop for user clarification when CRS is missing or invalid. <br>
Risk: Batch geospatial jobs can amplify an incorrect command across many files. <br>
Mitigation: Review a dry-run plan and process one representative file before scaling to the full batch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jvy/qgis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose qgis_process commands that read and write local GIS files; users should verify inputs, outputs, CRS, units, formats, and overwrite policy before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
