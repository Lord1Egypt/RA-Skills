## Description: <br>
Analyzes infant sleep monitoring videos for prone sleeping, head covering, and mouth or nose occlusion, then returns risk alerts and report information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and caregivers use this skill through an agent to submit infant sleep monitoring videos or public video URLs for asphyxia-risk analysis. The skill can also retrieve cloud-hosted historical alert reports for a provided open-id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive infant monitoring videos and user identifiers through cloud services with unclear privacy and retention controls. <br>
Mitigation: Review the service terms before use, avoid phone numbers as open-id values when an opaque identifier is available, and confirm how uploaded media, reports, accounts, and tokens can be deleted or rotated. <br>
Risk: The security scan verdict is suspicious because the skill sends child video, identifiers, account data, and stored tokens to external services. <br>
Mitigation: Install only after a security review, restrict use to trusted environments, and use least-privilege credentials or throwaway identifiers where possible. <br>
Risk: Asphyxia alerts are safety-critical and may be incomplete, delayed, or incorrect. <br>
Mitigation: Use the skill only as an auxiliary monitoring aid; maintain adult supervision and seek medical help when a high-risk condition is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-infant-suffocation-warning-analysis) <br>
- [Skill API Documentation](references/api_doc.md) <br>
- [Common Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands] <br>
**Output Format:** [Markdown reports and structured JSON from CLI/API analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk level, detected posture and occlusion signals, safety notes, report export links, and historical report lists.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
