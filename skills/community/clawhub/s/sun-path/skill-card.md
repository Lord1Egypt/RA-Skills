## Description:

Generates a sun path diagram, calculates solar position, performs building shadow analysis, and analyzes thermal comfort.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qrost](https://clawhub.ai/user/qrost)

### License/Terms of Use:

MIT

## Use Case:

Architects, designers, and environmental analysis practitioners use this skill to calculate solar position, generate sun path and comfort charts, model building shadows, estimate annual sun and shadow hours, and compute terrain shadow from DEM data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python dependencies and local file outputs can introduce dependency and file-output hygiene risks.

Mitigation: Install the skill in an isolated Python environment, pin or review dependencies before use, and write outputs to unique files in allowed media directories.

Risk: DEM inputs and output paths may expose sensitive local files or generate results intended for chat sharing.

Mitigation: Treat DEM and output paths as user-controlled inputs and avoid running the skill on sensitive private files unless the generated results are intended to be shared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qrost/skills/sun-path)
- [Project homepage](https://github.com/QROST)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, textual analysis, and generated image or raster file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PNG, JPG, or GeoTIFF outputs through local Python scripts when an agent executes the skill.]

## Skill Version(s):

1.4.1 (source: frontmatter, clawhub.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
