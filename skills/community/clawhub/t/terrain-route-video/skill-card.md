## Description: <br>
Generates minimalist terrain-style MP4 route videos from stops or GPX/KML tracks using road-following geometry, terrain tiles, Matplotlib rendering, and FFmpeg encoding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack4world](https://clawhub.ai/user/jack4world) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and mapping-focused users use this skill to generate animated route-map videos for driving routes or existing GPX/KML tracks. It is suited to route visualization workflows that need an MP4 export with a fly-follow camera, route drawing, labels, and terrain basemap styling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route coordinates and map tile areas can be sent to public OSRM and OpenTopoMap services during rendering. <br>
Mitigation: Avoid sensitive home or work routes unless public service disclosure is acceptable, or adapt the workflow to approved private routing and tile services. <br>
Risk: The FFmpeg encoding command overwrites the selected MP4 output path. <br>
Mitigation: Choose output paths deliberately and run the skill in a fresh working folder before rendering. <br>
Risk: The script creates local frame and tile-cache files in the current working folder. <br>
Mitigation: Use an isolated project folder or virtual environment and clean generated `frames/` and `.tile-cache/` data after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jack4world/terrain-route-video) <br>
- [stops.schema.json](references/stops.schema.json) <br>
- [OSRM route API](https://router.project-osrm.org/route/v1/driving/) <br>
- [JSON Schema draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown runbook with JSON input examples and shell commands; execution produces an MP4 video plus local frames and tile cache files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a 1600x900, 30 FPS, 12-second MP4 with route animation, labels, and terrain basemap styling.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
