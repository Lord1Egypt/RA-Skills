## Description: <br>
Detects people, vehicles, non-motorized vehicles, pets, and parcels in surveillance images or videos and returns structured object-detection reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and security operations teams use this skill to analyze surveillance images, video files, or media URLs for common object categories and to retrieve prior object-detection reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Surveillance images, videos, or media URLs are processed by configured LifeEmergence cloud services. <br>
Mitigation: Review endpoint configuration, processing and retention terms, and authorization requirements before use. <br>
Risk: The skill silently creates or reuses identity state and stores tokens and report history in the workspace data directory. <br>
Mitigation: Run the skill in an isolated workspace and define token deletion, revocation, and data cleanup procedures before deployment. <br>
Risk: Object-detection output is intended for security management reference and may be incomplete or incorrect. <br>
Mitigation: Require human review before using results for operational response or enforcement decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-basic-object-detection-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [API Documentation](references/api_doc.md) <br>
- [Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands] <br>
**Output Format:** [Markdown or JSON object-detection reports, with optional saved text output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report links and cloud-fetched history tables; JSON detail is the default output level.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
