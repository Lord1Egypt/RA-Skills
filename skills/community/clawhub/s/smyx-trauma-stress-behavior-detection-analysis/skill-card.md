## Description: <br>
Analyzes fixed-camera emergency shelter video to detect visible acute stress behavior signals such as stupor, tremor, unresponsiveness, and hypervigilance, then produces psychological crisis alerts for authorized human responders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External emergency-response teams and authorized psychological-rescue staff use this skill to analyze shelter or temporary-resettlement video, flag visible acute stress behaviors, locate affected people by zone, and generate reviewable crisis alerts with PFA-oriented response guidance. It should support human triage and responder dispatch, not provide clinical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive emergency-shelter video to an external service. <br>
Mitigation: Install only in an authorized emergency-response setting with clear legal authority, notice or consent procedures, and a data-processing agreement that covers video, report, retention, and access controls. <br>
Risk: The skill silently creates or reuses persistent identities and tokens, and history queries may expose prior reports. <br>
Mitigation: Confirm local token storage, automatic account creation, report retention, and history-query permissions before deployment; restrict access to trained and authorized personnel. <br>
Risk: Automated crisis alerts can be wrong or misused as clinical conclusions. <br>
Mitigation: Require human review before escalation or dispatch decisions, present results as visual behavior observations rather than ASD/PTSD diagnoses, and use qualified responders following PFA principles. <br>


## Reference(s): <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-trauma-stress-behavior-detection-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown and JSON-formatted structured analysis reports with observed behavior signals, crisis levels, zone/location markers, recommended response actions, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Historical-report queries can be rendered as Markdown tables; optional file output can save the generated report.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
