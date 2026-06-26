## Description: <br>
Analyzes fixed-camera videos of an elderly person at rest to estimate respiratory rate and flag elevated tachypnea or dyspnea risk without providing a medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers, elder-care operators, and developers use this skill to submit resting chest or abdomen video for visual respiratory-rate analysis and to list prior cloud reports. It is an assistive monitoring workflow and should not be treated as a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bedroom health video and identifiers are sent to a vendor cloud service. <br>
Mitigation: Use the skill only with consent from the monitored person or legal caregiver, and avoid uploading unnecessary personal identifiers or footage. <br>
Risk: Phone numbers or usernames used as open-id values can become account-linked data with cloud history retrieval. <br>
Mitigation: Protect configuration files and open-id values, use the least-identifying account value available, and review account creation, retention, and deletion controls before deployment. <br>
Risk: Respiratory-rate alerts could be mistaken for clinical diagnosis. <br>
Mitigation: Present outputs as assistive visual measurements and require human or clinical follow-up for warning or critical results. <br>
Risk: The security review notes broader or under-disclosed analysis behavior. <br>
Mitigation: Review the API scope and documentation before installation, and prefer a narrowed release focused on respiratory-rate analysis. <br>


## Reference(s): <br>
- [API documentation](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-elderly-tachypnea-detection-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON respiratory-rate report; history queries are formatted as Markdown tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user open-id plus a local video path or public video URL; cloud history queries return report links when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
