## Description: <br>
Analyzes local or URL-based pet drying box video through a server API to identify observed heat-stress signals such as panting intensity, tongue color, body movement, and risk level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet grooming, veterinary, and pet-drying-box operations teams can use this agent skill to submit drying-box videos for heat-stress warning reports and intervention suggestions. Users can also retrieve historical analysis reports tied to an open-id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local videos or public video URLs are sent to the LifeEmergence cloud service for analysis. <br>
Mitigation: Use only videos that are appropriate for cloud processing and confirm the user is comfortable sharing the content with that service. <br>
Risk: Reports are linked to an open-id, username, or phone-like identifier and can be retrieved later as cloud history. <br>
Mitigation: Use a deliberate identifier, explain that it is used for saved reports, and avoid submitting identifiers that should not be associated with the analysis. <br>
Risk: The skill can create or log into an account and store returned tokens locally for later API calls. <br>
Mitigation: Review bundled configuration and local token storage behavior before installation, isolate the runtime workspace when appropriate, and rotate or revoke tokens after use. <br>
Risk: Heat-stress warnings may be mistaken for veterinary diagnosis or treatment advice. <br>
Mitigation: Present results as observed safety signals only and escalate urgent or unclear cases to a qualified professional. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-pet-drying-box-heat-stress-analysis) <br>
- [API Documentation](artifact/references/api_doc.md) <br>
- [Supplemental API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON text from CLI/API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Historical report queries may include report links returned by the cloud service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact/SKILL.md frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
