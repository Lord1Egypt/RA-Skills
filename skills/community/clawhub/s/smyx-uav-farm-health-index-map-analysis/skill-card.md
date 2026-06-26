## Description: <br>
Analyzes UAV orthophotos or mosaics from multispectral or high-resolution RGB imagery to compute vegetation indices and produce a red/yellow/green farm health-index heatmap with abnormal zone coordinates and area estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agricultural service providers, farm operators, and research teams use this skill to submit UAV farm imagery or query prior reports, then receive vegetation-index maps and abnormal-zone measurements for field monitoring. The outputs are intended as index-based assessment results, not prescriptive fertilizer or pesticide recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends farm imagery, geolocation-like operational data, and a user identifier to LifeEmergence/Open API services. <br>
Mitigation: Install only when the publisher and API services are trusted for this data, and avoid submitting sensitive farm imagery or identifiers unless the deployment has approved that data flow. <br>
Risk: The security review notes under-disclosed account login, local token storage, and required credentials. <br>
Mitigation: Use a dedicated non-sensitive open-id, do not reuse an API key as a user identifier, and review credential and token handling before production use. <br>
Risk: Bundled documentation includes mismatched human-health analysis material that may confuse reviewers or operators. <br>
Mitigation: Review or remove mismatched documentation before deployment so operators understand the UAV farm health-index workflow and its limits. <br>
Risk: Vegetation-index outputs may be mistaken for direct agronomic prescriptions. <br>
Mitigation: Treat outputs as field-monitoring signals and abnormal-zone measurements, and confirm any operational decisions with field inspection and qualified agronomic review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-uav-farm-health-index-map-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON-backed analysis results and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include heatmap URLs, mean vegetation index values, abnormal-zone polygons and areas, crop coverage ratios, health distribution statistics, and historical report tables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
