## Description: <br>
Wind rose, wind speed/direction at a site; supports site and urban wind assessment (data only; detailed CFD is out of scope). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QROST](https://clawhub.ai/user/QROST) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, architects, and site analysts use this skill to fetch current or recent wind speed and direction and generate wind rose diagrams for a specified latitude and longitude. It supplies site wind data for assessment context; detailed CFD or pedestrian comfort simulation remains out of scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python scripts and depends on third-party Python packages. <br>
Mitigation: Install dependencies in a virtual environment or use a pinned dependency set when supply-chain reproducibility matters. <br>
Risk: Queried latitude and longitude values are sent to Open-Meteo. <br>
Mitigation: Avoid using sensitive private coordinates unless disclosure to the weather API is acceptable. <br>
Risk: The skill provides wind data only and does not perform CFD or pedestrian comfort simulation. <br>
Mitigation: Use the generated wind data as context or input for specialist CFD, wind-tunnel, or urban wind assessment tools. <br>


## Reference(s): <br>
- [Wind & Site ClawHub listing](https://clawhub.ai/QROST/wind-site) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>
- [Open-Meteo Historical Weather API](https://archive-api.open-meteo.com/v1/archive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown text with optional PNG image output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses latitude, longitude, optional days range, and optional PNG output path.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
