## Description: <br>
Analyzes home or kindergarten drop-off videos for crying, clinging, and resistance behaviors to estimate a child's separation-anxiety level and return supportive reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as parents, teachers, and care teams use this skill to analyze pre-school drop-off videos or report history and receive behavior observations, anxiety-level labels, and supportive next-step suggestions. The skill is for visual behavior analysis and reminders, not psychological diagnosis or prescription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive child and parent videos, video URLs, user identifiers, and report history may be sent to configured LifeEmergence/SMYX remote services. <br>
Mitigation: Confirm guardian consent before use, avoid bystanders where possible, prefer privacy-preserving capture such as masking when available, and review configured endpoints before deployment. <br>
Risk: Analysis reports may be linked to user identities and local tokens may support later report access. <br>
Mitigation: Use the least-identifying open-id practical for the deployment, protect local configuration and token storage, clear tokens on shared systems, and restrict access to report history. <br>
Risk: Behavioral analysis of crying, clinging, or resistance can be mistaken for a clinical diagnosis. <br>
Mitigation: Present outputs as visual behavior observations and supportive reminders only; require human review and consult a child psychology professional for prolonged or severe concerns. <br>


## Reference(s): <br>
- [Child Separation Anxiety API Documentation](artifact/references/api_doc.md) <br>
- [Common Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown and JSON-like structured text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include behavior metrics, separation-anxiety level, alert text, recommended action, parent tip, report export links, or history report rows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
