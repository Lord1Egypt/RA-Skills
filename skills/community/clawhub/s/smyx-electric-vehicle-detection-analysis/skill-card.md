## Description: <br>
Automatically detects electric motorcycles and e-bikes in restricted areas from video streams, images, local files, or media URLs, then reports counts, violation levels, alerts, and management suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and safety operations teams use this skill to analyze surveillance footage or images for e-bike and electric motorcycle activity in restricted areas. It supports park, community, campus, parking-lot, institutional, and road safety management workflows where results should be reviewed by humans before enforcement decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Surveillance images, videos, or media URLs are sent to a vendor cloud service for analysis. <br>
Mitigation: Use only footage that is appropriate for vendor processing, and confirm retention, access, and privacy terms before analyzing sensitive locations or identifiable people. <br>
Risk: The skill may silently create or reuse an identity and associate reports with that identity. <br>
Mitigation: Review identity association behavior before deployment and avoid shared environments where report history could expose another user's analysis records. <br>
Risk: Service tokens may be stored locally after login. <br>
Mitigation: Run the skill in a controlled environment, protect local storage, and rotate or clear credentials according to the vendor's operational guidance. <br>
Risk: Detection outputs are safety-management aids and may be incomplete or inaccurate. <br>
Mitigation: Require human review before enforcement, escalation, or operational decisions based on detected violations. <br>


## Reference(s): <br>
- [Electric Vehicle Detection API Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/guide.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-electric-vehicle-detection-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON analysis reports with optional saved output files and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include detected e-bike counts, violation severity, warnings, management suggestions, history lists, and report export links.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
