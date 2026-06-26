## Description: <br>
Using fixed home cameras in bedroom and dining areas, this skill analyzes multi-day behavior patterns for older adults or solo-living people and reports long immobility and appetite-change markers as behavioral observations, not medical diagnoses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, caregivers, community doctors, and developers use this skill to analyze 24-hour or longer home-camera footage for behavior reports about prolonged bed time, reduced eating activity, and related alerts. The output is intended to support human follow-up and care coordination, not to diagnose depression or prescribe treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive bedroom and dining-area camera footage or URLs and sends analysis requests to a vendor cloud service. <br>
Mitigation: Use only with explicit informed consent from the monitored person, confirm the deployment is appropriate for the care setting, and avoid submitting footage unless the privacy and vendor-cloud data flow are acceptable. <br>
Risk: The skill may silently create or reuse a cloud-linked identity and local tokens for analysis and history queries. <br>
Mitigation: Review local token storage and identity-linking behavior before deployment, and restrict history-report queries to cases where retrieving cloud records is intended. <br>
Risk: Behavioral markers such as long immobility or appetite change can be mistaken for a medical diagnosis. <br>
Mitigation: Present outputs as behavioral observations only and require family, caregiver, community doctor, or qualified clinician review for interpretation and follow-up. <br>


## Reference(s): <br>
- [API interface documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-depression-behavioral-markers-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style structured analysis reports, with shell command examples for execution and history queries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include behavior metrics, risk-signal levels, recommended follow-up actions, cloud report links, and history-query tables.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
