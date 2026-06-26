## Description: <br>
Generates a sun path diagram, calculates solar position, performs building shadow analysis, and analyzes thermal comfort. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QROST](https://clawhub.ai/user/QROST) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Architects and designers use this skill to generate solar position, sun path, building shadow, annual sun-hour, terrain shadow, and thermal comfort analyses for site and building studies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs bundled Python analysis scripts locally. <br>
Mitigation: Install and run it in a virtual environment and review the scripts before deployment. <br>
Risk: Generated plots and terrain outputs may contain sensitive site or DEM-derived information. <br>
Mitigation: Write outputs to approved temporary or media directories with unique names and only share images or rasters through Telegram when that disclosure is acceptable. <br>
Risk: Unpinned Python dependencies can change behavior over time. <br>
Mitigation: Pin dependency versions in the deployment environment when reproducible analysis is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QROST/sun-path) <br>
- [Publisher profile](https://clawhub.ai/user/QROST) <br>
- [Project homepage](https://github.com/QROST) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, image files, raster files] <br>
**Output Format:** [Markdown summaries with inline shell commands, generated PNG/JPG plots, optional GeoTIFF terrain-shadow output, and printed numeric analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files should be written under /tmp or OpenClaw media directories when they need to be returned to the user.] <br>

## Skill Version(s): <br>
1.4.1 (source: frontmatter, clawhub.json, server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
