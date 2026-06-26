## Description: <br>
Guide UPI payments launch from setup through sandbox testing to go-live readiness with detailed checklists, test matrix, gates, and rollback planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anugotta](https://clawhub.ai/user/anugotta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product, operations, finance, and compliance teams use this skill to coordinate UPI payment launch readiness from provider selection through sandbox validation, go-live gates, and incident rollback planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operational guidance could be mistaken for approval to launch production payments. <br>
Mitigation: Require current RBI, NPCI, provider, legal, compliance, and internal go-live approvals before production traffic. <br>
Risk: Launch notes or local memory files could capture payment credentials or customer data. <br>
Mitigation: Keep credentials only in a secret manager and avoid storing secrets or customer data in local notes. <br>
Risk: Referenced companion skills may introduce separate behavior or risk. <br>
Mitigation: Review companion skills before invoking them in a launch workflow. <br>


## Reference(s): <br>
- [UPI Go Live Checklist on ClawHub](https://clawhub.ai/anugotta/upi-go-live-checklist) <br>
- [RBI Digital Payment Authentication Directions](https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown checklists and structured task lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs identify current phase, completed work, missing tasks, blockers, owners, due dates, and next milestone.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
