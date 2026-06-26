## Description: <br>
TM Soil Moisture Skill analyzes local multi-depth soil temperature and moisture sensor data for Shiny-leaved yellowhorn plantings and provides irrigation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lu87985](https://clawhub.ai/user/lu87985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Farm operators and agricultural support teams use this skill to query device-level soil temperature and moisture readings, compare depth averages across a site, and receive practical irrigation guidance for Shiny-leaved yellowhorn plantings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local agricultural sensor data, including device identifiers, location fields, and device health information. <br>
Mitigation: Install only where read access to the expected local agriculture database is intended, and restrict local file or database permissions to the needed dataset. <br>
Risk: Irrigation recommendations are advisory and may be based mainly on local soil readings with simulated weather data. <br>
Mitigation: Confirm recommendations against current local weather, field observations, and agronomic judgment before taking operational action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lu87985/tm-soil-moisture) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style text with sensor readings, summaries, alerts, and advisory recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include soil temperature and moisture units, device health notes, and irrigation advice based on available local readings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
