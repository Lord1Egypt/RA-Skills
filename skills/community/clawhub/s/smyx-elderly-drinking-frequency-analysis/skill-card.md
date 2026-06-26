## Description: <br>
Analyzes fixed-camera video of an elderly person's water-cup area to count cup-pickup events and produce directional dehydration-risk reminders based on pickup frequency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, family members, and elder-care operators can use this skill to analyze living-room, kitchen, or care-facility video for cup-pickup frequency, long no-drink intervals, and reminders to encourage hydration. The outputs are behavioral indicators and caregiver prompts, not medical diagnoses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send elder-care home video, public video URLs, and a user identifier such as an open-id, phone number, or username to the provider's cloud service. <br>
Mitigation: Use it only with informed consent from the monitored person or guardian, limit sensitive video sharing, and treat identifiers and video URLs as sensitive data. <br>
Risk: The security review notes under-disclosed account creation, history access, bundled API key handling, and local token storage. <br>
Mitigation: Review the provider's data handling and retention behavior before deployment, protect any local token database, and avoid use where those cloud and storage behaviors are unacceptable. <br>
Risk: Cup-pickup frequency is only an indirect proxy for water intake and can be wrong when cups are empty, handled by someone else, or outside the camera view. <br>
Mitigation: Present results as directional caregiver reminders, combine them with caregiver observation or personal baselines, and seek medical advice when low intake or symptoms persist. <br>


## Reference(s): <br>
- [Elderly Drinking Frequency API Documentation](references/api_doc.md) <br>
- [Common Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON analysis report, with Markdown tables for history queries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open-id/user identifier and either a local video file or public video URL; can optionally save results to an output file.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
