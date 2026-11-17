## Description:

Fetch and generate an image of the current weather radar combined with a base map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaosconst](https://clawhub.ai/user/chaosconst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create animated weather radar GIFs for a requested city or coordinate pair using public radar and map tiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generating radar imagery contacts RainViewer and OpenStreetMap, which can disclose the approximate requested location through API and tile requests.

Mitigation: Use only locations appropriate to share with those services, and avoid sensitive coordinates in higher-control environments.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Pin requests and Pillow versions before deployment in controlled environments.

Risk: The script writes a GIF to a user-specified output path.

Mitigation: Run the skill in a sandbox with only the intended output directory writable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chaosconst/skills/weather-radar)
- [RainViewer Public Weather Maps API](https://api.rainviewer.com/public/weather-maps.json)
- [OpenStreetMap Tile Endpoint](https://tile.openstreetmap.org/{zoom}/{x}/{y}.png)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated GIF file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a 768x768 animated GIF composed from a 3x3 tile grid; requires requests and Pillow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
