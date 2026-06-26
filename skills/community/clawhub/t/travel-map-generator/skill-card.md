## Description: <br>
Generates illustrated travel itinerary maps with cartoon point-of-interest icons placed at real geographic coordinates and connected by a numbered route. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kensonh](https://clawhub.ai/user/kensonh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a destination and attractions into an illustrated itinerary map. It supports point-of-interest discovery, coordinate collection, map and icon generation, route compositing, and delivery of a final PNG. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destination and attraction details may be shared with search, maps/browser, and image-generation services during normal use. <br>
Mitigation: Use only non-sensitive travel details or run the workflow in an environment approved for those external services. <br>
Risk: The installer can replace an existing installation at the selected assistant skill path. <br>
Mitigation: Review the install target first and use the dry-run option before installing over a previous copy. <br>
Risk: Map coordinates, generated imagery, and route placement may be inaccurate or visually misleading. <br>
Mitigation: Verify coordinates against a trusted map source and inspect the generated PNG before relying on it for trip planning. <br>


## Reference(s): <br>
- [Coordinate Mapping Reference](artifact/references/coordinate-mapping.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kensonh/travel-map-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell commands; final artifact is a PNG image.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses web search, maps/browser access, and image generation during normal operation; writes temporary workspace files and a final travel-map PNG.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
