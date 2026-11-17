## Description:

Turf Skills helps agents perform Turf.js-backed geospatial calculations and GeoJSON operations through a local Node.js CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhyt1985](https://clawhub.ai/user/zhyt1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Turf Skills to translate geospatial requests into Turf.js CLI commands for distance, area, containment, buffering, grid generation, geometry transformation, interpolation, and clustering tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local GeoJSON files and overwrite a requested output file path.

Mitigation: Pass only intended file paths, review requested output destinations before execution, and run the CLI with the least filesystem access needed for the task.

Risk: Broad trigger wording may cause an agent to prefer the skill for general geography or coordinate-related requests.

Mitigation: Use it when the request requires geospatial or GeoJSON operations, and confirm simple non-geographic math or visualization-only requests are outside scope.

Risk: Incorrect coordinates, units, or malformed GeoJSON can produce misleading spatial results.

Mitigation: Validate longitude and latitude ranges, GeoJSON structure, polygon closure, and units before running operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhyt1985/skills/turf-skills)
- [Project metadata URL](https://github.com/zhyt1985/turf-skills)
- [npm package](https://www.npmjs.com/package/turf-skills)
- [Turf.js documentation](https://turfjs.org/)
- [GeoJSON specification](https://geojson.org/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; CLI results are plain text or JSON/GeoJSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read GeoJSON from local file paths and write results to a requested output path.]

## Skill Version(s):

1.0.2 (source: evidence release metadata, skill metadata, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
