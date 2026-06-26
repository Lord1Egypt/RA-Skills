## Description: <br>
Use this skill when a supply chain analyst, procurement manager, or sourcing team needs to assess a supplier's risk profile. Produces a scored five-dimension risk scorecard, a Low/Medium/High/Critical tier rating, and a prioritized mitigation action plan for procurement review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Supply chain analysts, procurement managers, and sourcing teams use this skill to assess supplier risk for onboarding, annual review, disruption response, or leadership review. It produces a five-dimension scorecard, tier rating, top risk flags, mitigation actions, and evidence gaps for procurement decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the scorecard as legal, sanctions, or compliance clearance. <br>
Mitigation: Present the scorecard as decision support and escalate sanctioned entities or material regulatory violations to legal and procurement leadership. <br>
Risk: Supplier materials may include unnecessary personal data, credentials, or raw internal exports. <br>
Mitigation: Use only business-relevant fields, avoid credentials and internal exports, and do not quote or retain personal employee data. <br>
Risk: Missing evidence can lead to overconfident supplier scores. <br>
Mitigation: Score conservatively, cite supplied evidence, and label each assumption in the evidence-gap section. <br>


## Reference(s): <br>
- [Supplier Risk Scorecard on ClawHub](https://clawhub.ai/archlab-space/supplier-risk-scorecard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown scorecard with tables and a prioritized action plan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires supplier name and country before final scoring; flags evidence gaps and assumptions.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and artifact changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
