## Description: <br>
Detects fall events in short videos or public video URLs and returns structured report information for home or care-facility safety monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers, care-facility operators, and safety-monitoring agents use this skill to analyze fall-detection videos, trigger alert-oriented reporting, and query prior cloud-hosted detection reports. Results are intended as safety-warning support and should be confirmed by a responsible person when an alert is raised. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive home or care-facility videos and identifiers such as username, phone number, or open-id may be sent to the Life Emergence cloud service. <br>
Mitigation: Confirm backend ownership, data retention, deletion, consent, and access-control policies before deployment, and avoid sending videos that exceed the intended monitoring purpose. <br>
Risk: Report-history and export workflows may expose personal fall-detection reports if user identifiers or report links are mishandled. <br>
Mitigation: Restrict report access by user, protect open-id values, and review generated report links before sharing outputs outside the care workflow. <br>
Risk: The evidence notes a bundled hardcoded api-key and local token database as deployment concerns. <br>
Mitigation: Replace bundled credentials with environment-managed secrets, rotate keys before production use, and review local token storage against organizational policy. <br>


## Reference(s): <br>
- [Fall Detection Video Analysis API Documentation](references/api_doc.md) <br>
- [ClawHub Skill Release Page](https://clawhub.ai/18072937735/smyx-fall-detection-video-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with shell command examples and JSON-style structured analysis or report lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open-id and accepts either a local video path or a public video URL; historical reports are queried from cloud APIs.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; SKILL.md frontmatter states 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
