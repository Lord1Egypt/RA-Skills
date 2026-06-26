## Description: <br>
Inspects, explains, validates, and plans conversion for ESRI Shapefile datasets, including sidecar files, CRS metadata, DBF encoding, schema limits, multipart geometry, and migration to GeoPackage or GeoJSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, GIS analysts, and agents use this skill to inspect Shapefile packaging, diagnose CRS, encoding, geometry, and DBF schema issues, and plan safe conversion or migration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversion, repair, reprojection, or batch cleanup can alter geospatial data if CRS, encoding, sidecar files, or output paths are wrong. <br>
Mitigation: Confirm the complete sidecar file set, CRS assumptions, encoding, and output path before changes, and keep an untouched copy of the original dataset. <br>
Risk: Guidance-only responses can still be misleading if a missing .prj, ambiguous encoding, or DBF schema limitation is treated as certain. <br>
Mitigation: State assumptions explicitly, distinguish assigning a CRS from reprojecting, and document likely schema or encoding loss before conversion. <br>


## Reference(s): <br>
- [Shapefile Patterns](references/patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/jvy/shapefile) <br>
- [Publisher profile](https://clawhub.ai/user/jvy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional command recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides guidance only; evidence reports no executable code, credential use, persistence, or hidden data access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
