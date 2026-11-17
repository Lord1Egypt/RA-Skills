## Description:

Generate illustrated travel itinerary map PNGs with cartoon POI icons placed at real geographic coordinates and connected by a numbered route.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kensonh](https://clawhub.ai/user/kensonh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to turn a travel destination, attractions, and optional visit order into an illustrated itinerary map. It supports POI discovery, coordinate collection, map generation, compositing, and delivery of a final travel-map image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel destinations, POIs, and coordinate queries may be shared with web, search, map, or image services.

Mitigation: Avoid private addresses or sensitive travel plans unless the user intends to share them with those services.

Risk: The skill can install the Pillow dependency into the active Python environment.

Mitigation: Review install.sh before running it, use a dry run first, or install Pillow in a dedicated virtual environment with a pinned version.

Risk: Generated maps depend on collected coordinates and generated imagery, so locations or routes may be inaccurate.

Mitigation: Verify coordinates and inspect the final map before relying on it for travel planning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kensonh/skills/travel-map-generator)
- [Coordinate Mapping Reference](references/coordinate-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and generated PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a temporary travel-map workspace, uses POI and viewport metadata, and writes a final map image for the user.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
