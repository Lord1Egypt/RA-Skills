## Description: <br>
Analyzes UAV farm imagery to compute vegetation indices and produce farm health-index heatmaps, abnormal-zone locations, area estimates, and structured reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agricultural service teams, and precision-agriculture operators use this skill to analyze UAV orthophotos, mosaics, images, or videos for vegetation-index heatmaps, problem-zone coordinates, health ratios, and report links. Results support field monitoring and variable-rate planning, with operational decisions reviewed against field conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private farm imagery or user-provided URLs may be uploaded to a remote service for analysis. <br>
Mitigation: Use only imagery approved for remote processing, confirm data-sharing consent, and review provider retention and deletion controls before production use. <br>
Risk: The skill may create or reuse an internal identity, store authentication tokens locally, and retrieve account-linked history with limited user control. <br>
Mitigation: Review identity handling, token storage, account deletion, and history-access controls before installing, especially on shared systems or regulated deployments. <br>
Risk: Vegetation-index outputs can be mistaken for direct agronomic prescriptions. <br>
Mitigation: Treat outputs as field-management references and validate them with field scouting or qualified agronomy review before operational action. <br>


## Reference(s): <br>
- [API documentation](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-uav-farm-health-index-map-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text reports, with optional saved output files and JSON-style service responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include health-index heatmap URLs, abnormal-zone coordinates, area estimates, crop-coverage statistics, health-ratio summaries, recommendations, and historical report links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
