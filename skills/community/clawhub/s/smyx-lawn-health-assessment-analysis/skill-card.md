## Description: <br>
Assesses top-down lawn images or videos to estimate wilting/yellowing, weed coverage, bare soil, and an overall lawn health score with maintenance guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External groundskeepers, turf managers, property owners, and municipal green-space teams use this skill to evaluate drone, fixed-camera, or uploaded top-down lawn imagery and receive visual condition metrics plus care recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded lawn images, videos, or remote URLs are processed by the publisher's cloud service. <br>
Mitigation: Use only imagery appropriate for that service and avoid sensitive property imagery unless the service's retention and account practices are acceptable. <br>
Risk: The skill creates or reuses an internal identity and stores account tokens in a local workspace database. <br>
Mitigation: Review local data handling before installation and remove workspace data or tokens when they are no longer needed. <br>
Risk: Cloud history queries can retrieve reports under the internally managed identity. <br>
Mitigation: Limit use to trusted workspaces and verify the displayed report history belongs to the intended user or environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-lawn-health-assessment-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Usage Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown or JSON analysis report with metrics, recommendations, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud report links and history tables when the user asks for prior lawn health reports.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
