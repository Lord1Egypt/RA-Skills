## Description: <br>
Value Aware Guard monitors value drift and boundary pressure, then suggests or records graduated interventions through a Node.js CLI and proactive-engine signal workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoguoqiang-hub](https://clawhub.ai/user/zhaoguoqiang-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor stated user values, boundary conditions, and proactive-engine signals, then produce guardrail status, reports, reminders, or intervention records. It is most relevant for workflows that need consent-aware support around time, energy, privacy, and decision boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence says the skill may monitor personal patterns over time without enough consent and control safeguards. <br>
Mitigation: Use it only after clear opt-in, make the monitoring scope visible, and provide a simple way to pause monitoring and delete stored observations. <br>
Risk: The release evidence flags possible escalation to high-impact interventions, including restrictive actions or emergency-contact use. <br>
Mitigation: Require explicit user approval for restrictive actions and emergency-contact use, except for narrowly documented emergencies that the user has agreed to in advance. <br>
Risk: Artifact behavior records interventions and publishes proactive signals that may influence later agent behavior. <br>
Mitigation: Review generated intervention records and outbound signals before connecting them to automated workflows, and keep conservative limits on daily interventions and escalation thresholds. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaoguoqiang-hub/value-aware-guard) <br>
- [Boundary Detection Rules](references/boundary-detection-rules.md) <br>
- [Value Drift Formula](references/value-drift-formula.md) <br>
- [Intervention Levels](references/intervention-levels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text and Markdown guidance with command examples and JSON-style status, intervention, and signal records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local guard configuration, user-value, state, intervention, and signal files in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
0.7.0 (source: ClawHub release evidence; artifact package.json reports 0.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
