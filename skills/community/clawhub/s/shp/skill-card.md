## Description: <br>
Inspect, explain, validate, and convert ESRI Shapefile datasets, including sidecar files, CRS metadata, DBF encoding, schema limits, multipart geometry issues, and migration guidance to GeoPackage or GeoJSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
GIS developers, data engineers, and analysts use this skill to troubleshoot Shapefile packaging, CRS metadata, DBF encoding, schema limits, multipart geometry issues, and migration choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversion or repair steps can overwrite or separate required Shapefile sidecar files. <br>
Mitigation: Confirm input and output paths, keep the original .shp, .shx, .dbf, and .prj files together, and write changed outputs to a new path unless the user explicitly asks otherwise. <br>
Risk: Missing CRS or encoding metadata can produce misplaced geometries or garbled attributes. <br>
Mitigation: Treat missing .prj and .cpg files as uncertainty, confirm CRS and encoding with the data source when accuracy matters, and document assumptions before conversion. <br>


## Reference(s): <br>
- [Shapefile Patterns](artifact/references/patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/jvy/shp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with checklists and optional command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend safe QGIS handoff commands and favors writing outputs to a new path instead of mutating originals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
