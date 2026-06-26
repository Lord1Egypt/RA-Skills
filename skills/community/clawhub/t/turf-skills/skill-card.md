## Description: <br>
Turf Skills helps agents run Turf.js spatial analysis for GeoJSON processing, coordinate calculations, geometry measurement, spatial queries, transformations, grids, interpolation, and clustering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhyt1985](https://clawhub.ai/user/zhyt1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, GIS analysts, and Claude Code users use this skill to translate geospatial requests into Turf.js CLI operations and to process GeoJSON data for measurement, spatial query, transformation, grid generation, interpolation, and clustering workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File input and output options can read unintended GeoJSON files or overwrite an important output file if paths are incorrect. <br>
Mitigation: Check --file, --file2, and --output paths before running the CLI. <br>
Risk: Broad geospatial trigger wording may cause the skill to be selected for coordinate-like tasks that are not geographic analysis. <br>
Mitigation: Use the skill for GeoJSON, GIS, map, GPS, and geographic-coordinate work, and avoid it for general math, CSS, canvas, or non-geographic coordinates. <br>
Risk: Invalid coordinates, malformed GeoJSON, or missing required action parameters can produce errors or misleading geospatial results. <br>
Mitigation: Validate longitude, latitude, polygon closure, required action inputs, and units before processing. <br>


## Reference(s): <br>
- [Turf Skills Project](https://github.com/zhyt1985/turf-skills) <br>
- [Turf Skills on npm](https://www.npmjs.com/package/turf-skills) <br>
- [Turf.js Documentation](https://turfjs.org/) <br>
- [GeoJSON](https://geojson.org/) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhyt1985/turf-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline shell commands and JSON or GeoJSON examples; CLI results are JSON, GeoJSON, or scalar text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read GeoJSON inputs from --file and --file2 and may write results to --output.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence, package.json, SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
