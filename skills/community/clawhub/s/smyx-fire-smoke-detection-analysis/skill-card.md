## Description: <br>
Detects fire and smoke in video scenes, supporting video stream and image analysis for fire early warning scenarios such as security surveillance, forest fire prevention, and industrial parks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams can use this skill to submit surveillance images, videos, or media URLs to a cloud service for fire and smoke detection reports. It can also retrieve prior detection reports for the configured user identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends surveillance images, videos, media URLs, user identifiers, and report-history requests to a third-party cloud service. <br>
Mitigation: Use only with media and identifiers approved for that service, and review organizational privacy requirements before deployment. <br>
Risk: The evidence reports a bundled api-key and local SQLite token storage. <br>
Mitigation: Remove or rotate bundled credentials before use, and review local token persistence with the publisher. <br>
Risk: The evidence reports unrelated health-analysis artifacts and mismatched documentation in the package. <br>
Mitigation: Review the included documentation and scripts before installing, and confirm the cloud endpoints and report behavior with the publisher. <br>
Risk: Fire and smoke detection is an auxiliary warning signal and may be incorrect or incomplete. <br>
Mitigation: Require human confirmation and follow the applicable emergency response plan when alarms or high-risk reports are produced. <br>


## Reference(s): <br>
- [Fire and smoke detection API documentation](references/api_doc.md) <br>
- [Common analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [ClawHub release page](https://clawhub.ai/18072937735/smyx-fire-smoke-detection-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Markdown, JSON, Files] <br>
**Output Format:** [Markdown or JSON fire and smoke detection reports, with optional output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include fire and smoke detection status, risk level, warning text, region details, timestamps, and links to stored report images.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
