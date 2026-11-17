## Description:

Generate a minimalist terrain-style animated driving route video (MP4) from a list of stops (cities/POIs) without Remotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack4world](https://clawhub.ai/user/jack4world)

### License/Terms of Use:


## Use Case:

External users, developers, and content producers use this skill to generate animated route-map videos from stop lists or existing GPX/KML tracks. It is useful when a route should follow roads where OSRM geometry is available, or use supplied track geometry directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Route coordinates may be sent to public OSRM routing and OpenTopoMap tile services.

Mitigation: Avoid sensitive routes or use supplied GPX/KML track geometry when road-following is not required, and review map-service exposure before rendering.

Risk: Unpinned Python dependencies and FFmpeg behavior can vary across environments.

Mitigation: Install in a fresh virtual environment and pin dependencies for reproducible or higher-assurance use.

Risk: Rendered frames and cached map tiles can leave local artifacts containing route imagery.

Mitigation: Run the skill in a dedicated working folder and remove frames/ and .tile-cache/ after the MP4 is produced when the route is sensitive.

## Reference(s):

- [stops.schema.json](references/stops.schema.json)
- [OSRM public route service endpoint](https://router.project-osrm.org/route/v1/driving/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown with JSON and bash examples; generated MP4 files when the script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script may also create local frames/ and .tile-cache/ directories during rendering.]

## Skill Version(s):

0.2.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
