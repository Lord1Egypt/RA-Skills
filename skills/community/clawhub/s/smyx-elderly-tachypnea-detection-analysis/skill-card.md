## Description: <br>
Analyzes fixed-camera video of an elderly person at rest to estimate respiratory rate and return tachypnea or dyspnea risk alerts with structured report output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers, home-care operators, and developers use this skill to analyze elderly resting chest or abdomen video for respiratory-rate estimates, risk flags, structured reports, and report-history lookup. It is an assistive monitoring workflow and should not be treated as a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive in-home health video and report history through a third-party cloud service. <br>
Mitigation: Use only with explicit consent from the monitored person or authorized caregiver, avoid unrelated private media, and confirm the publisher's deletion and retention controls before deployment. <br>
Risk: The skill automatically creates or reuses identity-linked local and cloud state. <br>
Mitigation: Run it in a dedicated environment, review local token and identity storage, and revoke or delete credentials and reports when monitoring is no longer needed. <br>
Risk: Respiratory alerts can be incomplete or misleading if video quality, posture, or scene conditions are poor. <br>
Mitigation: Treat outputs as assistive signals, verify urgent alerts by human contact or clinical follow-up, and do not use the skill as a stand-alone diagnostic system. <br>


## Reference(s): <br>
- [API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON text with optional report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the analysis output to a user-specified file and can list cloud report history.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
